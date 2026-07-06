"""
长视频教学处理器 — 复用现有录课视频 Pipeline。

用于 B站课程视频（含分P）、YouTube 教学视频等。
下载后每个 part 独立地走 VideoProcessor 的 5 阶段 Pipeline。
支持 B站分P 选择和断点续传。
"""

from __future__ import annotations

import logging
import os
import re
from pathlib import Path
from typing import Optional

from OCRLLM.config import AppConfig
from OCRLLM.core.document_model import SourceType
from OCRLLM.core.utils import ensure_dir
from OCRLLM.processors.base import BaseProcessor
from OCRLLM.processors.social.downloader import (
    DownloadResult,
    DownloadPart,
    download_media,
    is_social_url,
)

logger = logging.getLogger(__name__)


class SocialLongVideoProcessor(BaseProcessor):
    """社交媒体长视频教学处理器（复用 VideoProcessor Pipeline）。"""

    processor_key = "social_long"
    display_name = "社交媒体长视频识别"
    supported_extensions = ()  # URL 输入，不走扩展名匹配
    source_type = SourceType.SOCIAL_VIDEO

    def process(
        self,
        url: str,
        output_dir: Optional[str] = None,
        *,
        phases: Optional[list[int]] = None,
        skip_audio: bool = False,
        part_indices: Optional[list[int]] = None,
        download_result: Optional[DownloadResult] = None,
        prompt_template: Optional[str] = None,
        resume: bool = True,
    ) -> str:
        """处理社交媒体长视频 URL。

        Args:
            url: 视频页面 URL（B站/YouTube 等）。
            output_dir: 输出根目录。
            phases: 要执行的阶段列表（传给 VideoProcessor）。
            skip_audio: 跳过音频阶段。
            part_indices: B站分P选择（从1开始），None=全部。
            download_result: 已有的下载结果（避免重复下载）。
            prompt_template: 自定义板书/课件识别提示词模板。
            resume: 允许每个分P复用已完成的下载和识别产物。

        Returns:
            输出目录路径。
        """
        if not output_dir:
            output_dir = os.path.join(self.cfg.paths.output_dir, "social_长视频")
        ensure_dir(output_dir)

        # ── Step 1: 下载 ──
        self._report(0, 3, "下载视频...")
        if download_result is None:
            dl_dir = os.path.join(output_dir, "_downloads")
            download_result = download_media(
                url, dl_dir, self.cfg,
                part_indices=part_indices,
            )

        title = download_result.title
        logger.info("下载完成: %s (platform=%s, parts=%d)", title, download_result.platform, len(download_result.parts) or 1)
        self._write_social_context(download_result, output_dir)

        # ── Step 2: 逐 Part 处理 ──
        if download_result.is_playlist and download_result.parts:
            return self._process_multi_parts(download_result, output_dir, phases, skip_audio, prompt_template, resume)
        else:
            return self._process_single_video(download_result, output_dir, phases, skip_audio, prompt_template, resume)

    def _process_single_video(
        self,
        dl: DownloadResult,
        output_dir: str,
        phases: Optional[list[int]],
        skip_audio: bool,
        prompt_template: Optional[str],
        resume: bool,
    ) -> str:
        """处理单个视频文件。"""
        if not dl.video_path or not os.path.isfile(dl.video_path):
            raise FileNotFoundError(f"下载的视频文件不存在: {dl.video_path}")

        self._report(1, 3, f"处理视频: {dl.title}")
        stem = Path(dl.video_path).stem
        expect_audio = self._expects_audio_output(phases, skip_audio)
        if self._recognition_outputs_complete(output_dir, stem, expect_audio):
            logger.info("识别结果已存在，跳过处理: %s", output_dir)
            return output_dir
        result = self._run_video_processor(dl.video_path, output_dir, phases, skip_audio, prompt_template, resume)
        self._collect_recognition_outputs(dl.video_path, output_dir, result, expect_audio)
        return output_dir

    def _process_multi_parts(
        self,
        dl: DownloadResult,
        output_dir: str,
        phases: Optional[list[int]],
        skip_audio: bool,
        prompt_template: Optional[str],
        resume: bool,
    ) -> str:
        """逐 Part 处理 B站分P 等 playlist。"""
        valid_parts = [p for p in dl.parts if p.video_path and os.path.isfile(p.video_path)]
        if not valid_parts:
            raise FileNotFoundError(f"Playlist 中无有效视频文件: {dl.title}")

        total = len(valid_parts)
        failures: list[str] = []
        expect_audio = self._expects_audio_output(phases, skip_audio)
        for idx, part in enumerate(valid_parts):
            self._check_cancelled()
            self._report(idx, total, f"处理分P {part.index}/{total}: {part.title}")

            safe_name = re.sub(r'[<>:"/\\|?*]', '_', f"P{part.index}_{part.title}")[:80]
            part_output = os.path.join(output_dir, safe_name)
            ensure_dir(part_output)
            stem = Path(part.video_path).stem
            if self._recognition_outputs_complete(part_output, stem, expect_audio):
                logger.info("分P %d 识别结果已存在，跳过处理: %s", part.index, part.title)
                continue

            try:
                result = self._run_video_processor(part.video_path, part_output, phases, skip_audio, prompt_template, resume)
                self._collect_recognition_outputs(part.video_path, part_output, result, expect_audio)
                logger.info("分P %d/%d 处理完成: %s", part.index, total, part.title)
            except Exception as exc:
                logger.error("分P %d 处理失败: %s — %s", part.index, part.title, exc)
                failures.append(f"P{part.index} {part.title}: {exc}")

        self._report(total, total, "全部分P处理完成")
        if failures:
            raise RuntimeError("部分分P处理失败:\n" + "\n".join(failures))
        return output_dir

    def _run_video_processor(
        self,
        video_path: str,
        output_dir: str,
        phases: Optional[list[int]],
        skip_audio: bool,
        prompt_template: Optional[str],
        resume: bool,
    ) -> dict:
        """创建 VideoProcessor 并执行处理。"""
        from OCRLLM.processors.video import VideoProcessor

        proc = VideoProcessor(
            cfg=self._video_processor_config(),
            llm=self.llm,
            reporter=self.reporter,
            tracker=self.tracker,
            api_pool=self.api_pool,
        )
        return proc.process(
            video_path,
            output_dir=output_dir,
            phases=phases,
            skip_audio=skip_audio,
            prompt_template=prompt_template,
            resume=resume,
        )

    def _video_processor_config(self) -> AppConfig:
        """Return a video config tuned for long social-course stability."""
        concurrency_updates: dict[str, float | int] = {}
        video_updates: dict[str, bool] = {}
        max_parallel = max(1, int(self.cfg.social.long_video_llm_parallel_requests))
        if int(self.cfg.concurrency.llm_parallel_requests) > max_parallel:
            concurrency_updates["llm_parallel_requests"] = max_parallel

        min_stagger = max(0.0, float(self.cfg.social.long_video_llm_request_stagger_seconds))
        if float(self.cfg.concurrency.llm_request_stagger_seconds) < min_stagger:
            concurrency_updates["llm_request_stagger_seconds"] = min_stagger

        if self.cfg.video.extract_hotwords_with_text_model:
            video_updates["extract_hotwords_with_text_model"] = False

        if not concurrency_updates and not video_updates:
            return self.cfg

        text_hotwords_enabled = video_updates.get(
            "extract_hotwords_with_text_model",
            self.cfg.video.extract_hotwords_with_text_model,
        )
        logger.info(
            "social_long video processor stability config: parallel=%s, stagger=%s, text_hotwords=%s",
            concurrency_updates.get("llm_parallel_requests", self.cfg.concurrency.llm_parallel_requests),
            concurrency_updates.get("llm_request_stagger_seconds", self.cfg.concurrency.llm_request_stagger_seconds),
            text_hotwords_enabled,
        )
        config_updates = {}
        if concurrency_updates:
            config_updates["concurrency"] = concurrency_updates
        if video_updates:
            config_updates["video"] = video_updates
        return self.cfg.with_updates(**config_updates)

    @staticmethod
    def _expects_audio_output(phases: Optional[list[int]], skip_audio: bool) -> bool:
        return not skip_audio and (phases is None or 5 in phases)

    @staticmethod
    def _recognition_outputs_complete(output_dir: str, stem: str, expect_audio: bool) -> bool:
        board_path = os.path.join(output_dir, f"{stem}_板书识别.md")
        if not (os.path.isfile(board_path) and os.path.getsize(board_path) > 0):
            return False
        transcript_path = os.path.join(output_dir, f"{stem}_录音识别.md")
        return not expect_audio or (os.path.isfile(transcript_path) and os.path.getsize(transcript_path) > 0)

    def _collect_recognition_outputs(
        self,
        video_path: str,
        output_dir: str,
        result: dict,
        expect_audio: bool,
    ) -> dict[str, str]:
        """Validate the two user-facing Markdown outputs and remove transient merged board drafts."""
        stem = Path(video_path).stem
        if not isinstance(result, dict):
            raise TypeError(f"VideoProcessor.process() must return a result dict, got {type(result).__name__}")

        board_path = str(result.get("board_md") or os.path.join(output_dir, f"{stem}_板书识别.md"))
        transcript_path = str(result.get("transcript_md") or os.path.join(output_dir, f"{stem}_录音识别.md"))

        if not (os.path.isfile(board_path) and os.path.getsize(board_path) > 0):
            raise FileNotFoundError(f"图片/板书识别 Markdown 缺失或为空: {board_path}")
        if expect_audio and not (os.path.isfile(transcript_path) and os.path.getsize(transcript_path) > 0):
            raise FileNotFoundError(f"录音识别 Markdown 缺失或为空: {transcript_path}")

        legacy_board_path = os.path.join(output_dir, f"{stem}_板书识别_合并.md")
        if os.path.isfile(legacy_board_path) and os.path.abspath(legacy_board_path) != os.path.abspath(board_path):
            try:
                os.remove(legacy_board_path)
            except OSError:
                pass

        return {"board_md": board_path, "transcript_md": transcript_path}

    def _write_social_context(self, dl: DownloadResult, output_dir: str) -> str | None:
        if not (dl.comment_texts or dl.danmaku_texts or any(part.danmaku_texts for part in dl.parts)):
            return None

        context_path = os.path.join(output_dir, "bilibili_social_context.md")
        lines = [
            f"# {dl.title} social context",
            "",
            f"- Platform: {dl.platform}",
            f"- BVID: {dl.bvid or 'unknown'}",
            f"- AID: {dl.aid or 'unknown'}",
            f"- Parts: {len(dl.parts) or 1}",
            "",
        ]
        resource_urls = sorted(set(re.findall(r"https?://\S+", "\n".join(dl.comment_texts))))
        if resource_urls:
            lines.extend(["## Resource links from comments", ""])
            lines.extend(f"- {url}" for url in resource_urls)
            lines.append("")
        if dl.description:
            lines.extend(["## Description", "", dl.description.strip(), ""])
        if dl.comment_texts:
            lines.extend(["## Shared comments", ""])
            lines.extend(f"{idx}. {text}" for idx, text in enumerate(dl.comment_texts, start=1))
            lines.append("")
        parts = dl.parts or [DownloadPart(index=1, title=dl.title, video_path=dl.video_path, duration=dl.duration, danmaku_texts=dl.danmaku_texts)]
        lines.extend(["## Danmaku by part", ""])
        for part in parts:
            lines.extend([f"### P{part.index} {part.title}", ""])
            danmaku = part.danmaku_texts or ([] if len(parts) > 1 else dl.danmaku_texts)
            if danmaku:
                lines.extend(f"- {text}" for text in danmaku)
            else:
                lines.append("- No danmaku captured.")
            lines.append("")
        Path(context_path).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
        logger.info("社交上下文已写入: %s", context_path)
        return context_path
