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
    ) -> str:
        """处理社交媒体长视频 URL。

        Args:
            url: 视频页面 URL（B站/YouTube 等）。
            output_dir: 输出根目录。
            phases: 要执行的阶段列表（传给 VideoProcessor）。
            skip_audio: 跳过音频阶段。
            part_indices: B站分P选择（从1开始），None=全部。
            download_result: 已有的下载结果（避免重复下载）。

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

        # ── Step 2: 逐 Part 处理 ──
        if download_result.is_playlist and download_result.parts:
            return self._process_multi_parts(download_result, output_dir, phases, skip_audio)
        else:
            return self._process_single_video(download_result, output_dir, phases, skip_audio)

    def _process_single_video(
        self,
        dl: DownloadResult,
        output_dir: str,
        phases: Optional[list[int]],
        skip_audio: bool,
    ) -> str:
        """处理单个视频文件。"""
        if not dl.video_path or not os.path.isfile(dl.video_path):
            raise FileNotFoundError(f"下载的视频文件不存在: {dl.video_path}")

        self._report(1, 3, f"处理视频: {dl.title}")
        result_path = self._run_video_processor(dl.video_path, output_dir, phases, skip_audio)
        return self._normalize_user_outputs(dl.video_path, output_dir, result_path)

    def _process_multi_parts(
        self,
        dl: DownloadResult,
        output_dir: str,
        phases: Optional[list[int]],
        skip_audio: bool,
    ) -> str:
        """逐 Part 处理 B站分P 等 playlist。"""
        valid_parts = [p for p in dl.parts if p.video_path and os.path.isfile(p.video_path)]
        if not valid_parts:
            raise FileNotFoundError(f"Playlist 中无有效视频文件: {dl.title}")

        total = len(valid_parts)
        for idx, part in enumerate(valid_parts):
            self._check_cancelled()
            self._report(idx, total, f"处理分P {part.index}/{total}: {part.title}")

            safe_name = re.sub(r'[<>:"/\\|?*]', '_', f"P{part.index}_{part.title}")[:80]
            part_output = os.path.join(output_dir, safe_name)
            ensure_dir(part_output)

            try:
                result_path = self._run_video_processor(part.video_path, part_output, phases, skip_audio)
                self._normalize_user_outputs(part.video_path, part_output, result_path)
                logger.info("分P %d/%d 处理完成: %s", part.index, total, part.title)
            except Exception as exc:
                logger.error("分P %d 处理失败: %s — %s", part.index, part.title, exc)

        self._report(total, total, "全部分P处理完成")
        return output_dir

    def _run_video_processor(
        self,
        video_path: str,
        output_dir: str,
        phases: Optional[list[int]],
        skip_audio: bool,
    ) -> str:
        """创建 VideoProcessor 并执行处理。"""
        from OCRLLM.processors.video import VideoProcessor

        proc = VideoProcessor(
            cfg=self.cfg,
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
        )

    def _normalize_user_outputs(self, video_path: str, output_dir: str, result_path: str) -> str:
        """将长视频最终板书稿规范为 _识别.md，仅保留统一命名。"""
        stem = Path(video_path).stem
        target_path = os.path.join(output_dir, f"{stem}_识别.md")

        if result_path and os.path.isfile(result_path) and os.path.abspath(result_path) != os.path.abspath(target_path):
            os.replace(result_path, target_path)
            logger.info("长视频图片识别结果已规范命名: %s", target_path)
        elif os.path.isfile(target_path):
            logger.info("长视频图片识别结果已存在: %s", target_path)

        legacy_board_path = os.path.join(output_dir, f"{stem}_板书识别_合并.md")
        if os.path.isfile(legacy_board_path) and os.path.abspath(legacy_board_path) != os.path.abspath(target_path):
            try:
                os.remove(legacy_board_path)
            except OSError:
                pass

        return target_path if os.path.isfile(target_path) else result_path
