"""短视频知识识别处理器。

Pipeline:
    1. 场景切换检测（PySceneDetect / TransNetV2，自适应阈值）
    2. 帧截取（每段中点 + 终点前 0.2s）
    3. LLM 画面识别（无记忆系统，侧重画面描述）
    4. 热词提取（vision model 直接从帧图像提取可见术语）
    5. 音频提取 + ASR（使用热词增强）
    6. 输出用户结果并清理中间产物
"""

from __future__ import annotations

import logging
import os
import shutil
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Optional

import cv2

from OCRLLM.config import AppConfig
from OCRLLM.core.video_capture import open_video_capture
from OCRLLM.core.document_model import SourceType
from OCRLLM.core.task_runner import CancelledError
from OCRLLM.core.utils import batch_list, ensure_dir, strip_md_fence
from OCRLLM.core.incremental_writer import IncrementalMDWriter
from OCRLLM.imaging.shot_detector import detect_shots, SceneSegment, ShotDetectionResult
from OCRLLM.imaging.audio_extractor import extract_audio
from OCRLLM.processors.base import BaseProcessor
from OCRLLM import prompts

logger = logging.getLogger(__name__)


class ShortVideoProcessor(BaseProcessor):
    """短视频知识内容识别处理器。"""

    processor_key = "social_short"
    display_name = "短视频知识识别"
    supported_extensions = (".mp4", ".avi", ".mkv", ".mov", ".flv", ".wmv")
    source_type = SourceType.SOCIAL_VIDEO

    def process(
        self,
        video_path: str,
        output_dir: Optional[str] = None,
        *,
        title: str = "",
        danmaku_texts: Optional[list[str]] = None,
        comment_texts: Optional[list[str]] = None,
        prompt_template: Optional[str] = None,
    ) -> str:
        """处理短视频 → Markdown。

        Args:
            video_path: 本地视频文件路径。
            output_dir: 输出目录（默认同目录）。
            title: 视频标题（用于输出命名/展示）。
            danmaku_texts: 兼容保留参数，当前不参与热词提取。
            comment_texts: 兼容保留参数，当前不参与热词提取。
            prompt_template: 自定义画面识别提示词模板。

        Returns:
            输出 Markdown 文件路径。
        """
        video_path = os.path.abspath(video_path)
        if not os.path.isfile(video_path):
            raise FileNotFoundError(f"视频文件不存在: {video_path}")

        stem = Path(video_path).stem
        if not output_dir:
            output_dir = os.path.join(os.path.dirname(video_path), f"{stem}_短视频识别")
        ensure_dir(output_dir)

        total_phases = 6
        self._report(0, total_phases, "开始短视频处理")

        # ── Phase 1: 场景切换检测 ──
        self._report(1, total_phases, "检测场景切换点...")
        detection = detect_shots(video_path, self.cfg)
        segments = detection.segments
        logger.info(
            "场景检测完成: %d 个切换点, %d 个片段, 阈值=%.3f, 迭代=%d",
            len(detection.cuts), len(segments),
            detection.threshold_used, detection.iterations_used,
        )

        if not segments:
            logger.warning("未检测到场景片段")
            return ""

        # ── Phase 2: 帧截取 ──
        self._report(2, total_phases, "截取关键帧...")
        frames_dir = os.path.join(output_dir, "frames")
        ensure_dir(frames_dir)
        frame_map = self._extract_frames(video_path, segments, frames_dir, detection.fps)

        # ── Phase 3: LLM 画面识别 ──
        self._report(3, total_phases, "LLM 识别画面内容...")
        scene_md = self._recognize_scenes(segments, frame_map, detection.fps, prompt_template)
        
        # 添加社交视频标题元数据标记
        video_title = title or stem
        scene_md_with_meta = f"<!-- meta:social_video title={video_title} -->\n\n{scene_md}"
        
        visual_output_path = os.path.join(output_dir, f"{stem}_识别.md")
        Path(visual_output_path).write_text(scene_md_with_meta, encoding="utf-8")

        # ── Phase 4: 热词提取 ──
        self._report(4, total_phases, "提取专业术语热词...")
        hotwords = self._extract_hotwords(frame_map)
        if hotwords:
            logger.info("热词提取: %d 个热词（仅用于 ASR 增强）", len(hotwords))

        # ── Phase 5: 音频提取 + ASR ──
        self._report(5, total_phases, "音频提取与语音识别...")
        self._extract_and_transcribe_audio(video_path, output_dir, stem, hotwords=hotwords)

        # ── Phase 6: 输出整理 ──
        self._report(6, total_phases, "整理用户输出...")
        self._cleanup_intermediate_files(output_dir, stem, frames_dir)
        self._report_content(scene_md, "短视频图片识别结果")

        logger.info("短视频处理完成: %s", visual_output_path)
        return visual_output_path

    # ── Phase 2: 帧截取 ──

    def _extract_frames(
        self,
        video_path: str,
        segments: list[SceneSegment],
        frames_dir: str,
        fps: float,
    ) -> dict[int, list[str]]:
        """截取每个片段的中点帧和终点前帧。

        Returns:
            {segment_index: [mid_frame_path, end_frame_path], ...}
        """
        cap = open_video_capture(video_path)
        if not cap.isOpened():
            raise RuntimeError(f"无法打开视频: {video_path}")

        frame_map: dict[int, list[str]] = {}

        try:
            for seg in segments:
                self._check_cancelled()
                paths: list[str] = []

                for label, frame_idx in [("mid", seg.mid_frame), ("end", seg.end_offset_frame)]:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
                    ret, frame = cap.read()
                    if not ret:
                        logger.warning("无法读取帧 %d (segment %d)", frame_idx, seg.index)
                        continue

                    ts = frame_idx / fps if fps > 0 else 0
                    filename = f"scene_{seg.index:03d}_{label}_{int(ts)}s.jpg"
                    filepath = os.path.join(frames_dir, filename)
                    cv2.imwrite(filepath, frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
                    paths.append(filepath)

                frame_map[seg.index] = paths
        finally:
            cap.release()

        logger.info("截取 %d 个片段共 %d 帧", len(frame_map), sum(len(v) for v in frame_map.values()))
        return frame_map

    # ── Phase 3: LLM 画面识别 ──

    def _recognize_scenes(
        self,
        segments: list[SceneSegment],
        frame_map: dict[int, list[str]],
        fps: float,
        prompt_template: Optional[str] = None,
    ) -> str:
        """并行调用 LLM 识别每个场景的帧。无记忆系统。"""
        results: dict[int, str] = {}
        workers = min(self.cfg.concurrency.llm_parallel_requests, len(segments))
        template = prompt_template or prompts.SHORT_VIDEO_RECOGNIZE

        def _recognize_one(seg: SceneSegment) -> tuple[int, str]:
            self._check_cancelled()
            paths = frame_map.get(seg.index, [])
            if not paths:
                return seg.index, ""

            image_names = ", ".join(Path(p).stem for p in paths)
            start_ts = f"{int(seg.start_time) // 60}:{int(seg.start_time) % 60:02d}"
            end_ts = f"{int(seg.end_time) // 60}:{int(seg.end_time) % 60:02d}"
            time_range = f"{start_ts}~{end_ts}"

            prompt = template.format(
                scene_id=str(seg.index),
                time_range=time_range,
                image_names=image_names,
            )

            with self.api_pool.get_client() as client:
                result = client.chat_with_images(prompt, paths)

            return seg.index, strip_md_fence(result)

        with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
            futures = {}
            for seg in segments:
                self._check_cancelled()
                future = pool.submit(_recognize_one, seg)
                futures[future] = seg.index
                self._sleep(self.cfg.concurrency.llm_request_stagger_seconds)

            for future in self._iter_completed_futures(set(futures)):
                seg_idx, text = future.result()
                results[seg_idx] = text

        # 按场景顺序拼接，每个场景添加元数据标记
        parts: list[str] = []
        for seg in sorted(segments, key=lambda s: s.index):
            text = results.get(seg.index, "")
            if text:
                # 格式化时间戳成 M:SS~M:SS 格式
                start_ts = f"{int(seg.start_time) // 60}:{int(seg.start_time) % 60:02d}"
                end_ts = f"{int(seg.end_time) // 60}:{int(seg.end_time) % 60:02d}"
                # 添加场景元数据标记
                scene_marker = f"<!-- meta:scene id={seg.index} time={start_ts}~{end_ts} -->"
                parts.append(f"{scene_marker}\n\n{text}")

        return "\n\n".join(parts)

    # ── Phase 4: 热词提取 ──

    def _extract_hotwords(
        self,
        frame_map: dict[int, list[str]],
    ) -> list[str]:
        """从所有帧图像中直接提取可见的专业术语热词。

        使用 vision model 批量扫描帧截图，提取画面中可见的英文单词、
        品牌名、专有名词、URL 关键词和技术术语，用于 ASR 热词增强。
        """
        # 收集所有帧路径
        all_paths: list[str] = []
        for paths in frame_map.values():
            all_paths.extend(paths)
        if not all_paths:
            return []

        # 分批处理（每批最多 8 张图片）
        batches = batch_list(all_paths, 8)
        workers = min(self.cfg.concurrency.llm_parallel_requests, len(batches))
        hotwords: list[str] = []

        def _extract_batch(batch_paths: list[str]) -> list[str]:
            self._check_cancelled()
            try:
                with self.api_pool.get_client() as client:
                    result = client.chat_with_images(
                        prompts.EXTRACT_HOTWORDS_FROM_FRAMES,
                        batch_paths,
                    )
                return [
                    line.strip() for line in strip_md_fence(result).strip().splitlines()
                    if line.strip() and len(line.strip()) >= 2
                ]
            except Exception as exc:
                logger.warning("帧热词提取批次失败: %s", exc)
                return []

        with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
            futures = []
            for batch in batches:
                self._check_cancelled()
                futures.append(pool.submit(_extract_batch, batch))
                self._sleep(self.cfg.concurrency.llm_request_stagger_seconds)

            for future in self._iter_completed_futures(set(futures)):
                hotwords.extend(future.result())

        # 去重（保持顺序，大小写不敏感）+ 过滤噪声
        _GENERIC = {
            "search", "filter", "export", "view", "submit", "cancel", "close",
            "star", "fork", "code", "action", "status", "class", "online",
            "profile", "alert", "design", "preview", "overview", "settings",
            "home", "about", "contact", "help", "sign in", "sign up", "login",
            "logout", "dashboard", "back", "next", "previous", "edit", "delete",
            "save", "add", "remove", "open", "share", "download", "upload",
        }
        seen: set[str] = set()
        unique: list[str] = []
        for hw in hotwords:
            hw_stripped = hw.strip().strip("-•·*")
            if not hw_stripped or len(hw_stripped) < 2:
                continue
            # 过滤过长条目（>40字符）
            if len(hw_stripped) > 40:
                continue
            hw_lower = hw_stripped.lower()
            if hw_lower in seen or hw_lower in _GENERIC:
                continue
            seen.add(hw_lower)
            unique.append(hw_stripped)
        # 限制总量（前 80 个）
        unique = unique[:80]
        logger.info("帧热词提取: %d 个（来自 %d 帧, %d 批）", len(unique), len(all_paths), len(batches))
        return unique

    # ── Phase 5: 音频 + ASR ──

    def _extract_and_transcribe_audio(
        self,
        video_path: str,
        output_dir: str,
        stem: str,
        *,
        hotwords: Optional[list[str]] = None,
    ) -> str:
        """提取音频并进行 ASR 转写。"""
        audio_path = os.path.join(output_dir, f"{stem}.mp3")

        try:
            extract_audio(
                video_path,
                audio_path,
                cancel_event=self.reporter.cancel_event,
            )
        except Exception as exc:
            logger.warning("音频提取失败: %s — 跳过 ASR", exc)
            return ""

        if not os.path.isfile(audio_path):
            return ""

        # 使用 AudioProcessor 进行 ASR
        try:
            from OCRLLM.processors.audio import AudioProcessor
            audio_proc = AudioProcessor(
                cfg=self.cfg,
                llm=self.llm,
                reporter=self.reporter,
                tracker=self.tracker,
                api_pool=self.api_pool,
            )
            asr_output = audio_proc.process(
                audio_path,
                hotwords=hotwords or None,
                output_path=os.path.join(output_dir, f"{stem}_录音识别.md"),
            )
            if isinstance(asr_output, str) and os.path.isfile(asr_output):
                return Path(asr_output).read_text(encoding="utf-8")
            return ""
        except Exception as exc:
            logger.warning("ASR 转写失败: %s", exc)
            return ""

    def _cleanup_intermediate_files(self, output_dir: str, stem: str, frames_dir: str) -> None:
        """清理短视频中间产物，仅保留用户可见的两份 Markdown。"""
        cleanup_targets = [
            os.path.join(output_dir, f"{stem}.mp3"),
            os.path.join(output_dir, f"{stem}_热词表.txt"),
        ]

        for path in cleanup_targets:
            if os.path.exists(path):
                try:
                    os.remove(path)
                    logger.info("已清理中间文件: %s", path)
                except Exception as exc:
                    logger.warning("清理中间文件失败: %s — %s", path, exc)

        if os.path.isdir(frames_dir):
            try:
                shutil.rmtree(frames_dir)
                logger.info("已清理帧目录: %s", frames_dir)
            except Exception as exc:
                logger.warning("清理帧目录失败: %s — %s", frames_dir, exc)
