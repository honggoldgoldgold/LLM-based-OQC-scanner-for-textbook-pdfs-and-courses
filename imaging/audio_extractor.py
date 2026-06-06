"""
从视频中提取音频（ffmpeg）。
"""

from __future__ import annotations

import os
import logging
import subprocess
from pathlib import Path
from threading import Event
from typing import Optional

from OCRLLM.core.utils import ensure_dir, get_ffmpeg, run_subprocess_cancellable

logger = logging.getLogger(__name__)


def extract_audio(
    video_path: str,
    output_path: str = None,
    cancel_event: Optional[Event] = None,
) -> str:
    """从视频提取音频为 MP3。"""
    if output_path is None:
        stem = Path(video_path).stem
        out_dir = os.path.join(os.path.dirname(video_path), "extracted_audio")
        ensure_dir(out_dir)
        output_path = os.path.join(out_dir, f"{stem}.mp3")

    if os.path.exists(output_path):
        logger.info("[AUDIO_EXTRACT] 已存在: %s", output_path)
        return output_path

    ffmpeg = get_ffmpeg()
    cmd = [
        ffmpeg, "-i", video_path,
        "-vn", "-ac", "1", "-acodec", "libmp3lame",
        "-ab", "32k", "-ar", "16000", "-y",
        output_path,
    ]

    logger.info("[AUDIO_EXTRACT] 执行: %s", " ".join(cmd))
    result = run_subprocess_cancellable(cmd, cancel_event=cancel_event, timeout=600)
    if result.returncode != 0:
        stderr = (result.stderr if isinstance(result.stderr, str)
                  else (result.stderr or b"").decode("utf-8", errors="replace"))
        # ffmpeg stderr 开头是长版本横幅；取尾部才能看到真正的错误信息
        raise RuntimeError(
            f"ffmpeg 失败 (rc={result.returncode}): ...{stderr[-800:]}"
        )

    logger.info("[AUDIO_EXTRACT] 完成: %s", output_path)
    return output_path
