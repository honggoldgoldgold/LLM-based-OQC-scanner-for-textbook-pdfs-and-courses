"""
短视频识别结果合并 — 场景描述 + ASR 文本按时间对齐。
"""

from __future__ import annotations

import re
import logging
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)

_SCENE_PATTERN = re.compile(
    r"<!--\s*meta:scene\s+id=(\S+)\s+time=(\S+)\s*-->",
    re.MULTILINE,
)

_TIME_RANGE_PATTERN = re.compile(r"(\d{1,3}:\d{2})~(\d{1,3}:\d{2})")
_SEGMENT_MARKER_PATTERN = re.compile(
    r"<!--\s*meta:segment\s+index=\d+(?:\s+time=\d{1,3}:\d{2}~\d{1,3}:\d{2})?\s*-->",
    re.MULTILINE,
)


@dataclass
class SceneBlock:
    """单个场景识别结果块。"""
    scene_id: str
    time_range: str   # "MM:SS~MM:SS"
    start_sec: float
    end_sec: float
    content: str      # LLM 识别的 Markdown 内容


def _time_to_sec(t: str) -> float:
    """将 MM:SS 或 H:MM:SS 格式转为秒数。"""
    parts = t.split(":")
    if len(parts) == 2:
        return int(parts[0]) * 60 + int(parts[1])
    elif len(parts) == 3:
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    return 0.0


def _sec_to_time(sec: float) -> str:
    """秒数 → MM:SS 格式。"""
    m = int(sec) // 60
    s = int(sec) % 60
    return f"{m}:{s:02d}"


def parse_scene_blocks(md_text: str) -> list[SceneBlock]:
    """从 LLM 输出的 Markdown 中解析场景块。"""
    blocks: list[SceneBlock] = []
    parts = _SCENE_PATTERN.split(md_text)

    # parts 格式: [prefix, scene_id_1, time_1, content_1, scene_id_2, time_2, content_2, ...]
    i = 1
    while i + 2 < len(parts):
        scene_id = parts[i]
        time_range = parts[i + 1]
        content = parts[i + 2].strip()
        i += 3

        m = _TIME_RANGE_PATTERN.search(time_range)
        start_sec = _time_to_sec(m.group(1)) if m else 0
        end_sec = _time_to_sec(m.group(2)) if m else 0

        blocks.append(SceneBlock(
            scene_id=scene_id,
            time_range=time_range,
            start_sec=start_sec,
            end_sec=end_sec,
            content=content,
        ))

    return blocks


def parse_asr_segments(asr_text: str) -> list[tuple[float, float, str]]:
    """解析 ASR 输出的时间戳文本。

    支持格式:
      <!-- meta:segment index=N time=MM:SS~MM:SS -->
      或简单的纯文本（视为单一段落）

    Returns:
        [(start_sec, end_sec, text), ...]
    """
    seg_pattern = re.compile(
        r"<!--\s*meta:segment\s+index=\d+\s+time=(\d{1,3}:\d{2})~(\d{1,3}:\d{2})\s*-->",
        re.MULTILINE,
    )
    parts = seg_pattern.split(asr_text)

    if len(parts) <= 1:
        # 无时间戳：移除 segment 注释后整段作为单一 segment
        cleaned = _SEGMENT_MARKER_PATTERN.sub("", asr_text)
        cleaned = re.sub(r"\n{3,}", "\n\n", cleaned).strip()
        if not cleaned:
            return []
        return [(0, float("inf"), cleaned)]

    segments: list[tuple[float, float, str]] = []
    i = 1
    while i + 2 < len(parts):
        start = _time_to_sec(parts[i])
        end = _time_to_sec(parts[i + 1])
        text = parts[i + 2].strip()
        if text:
            segments.append((start, end, text))
        i += 3

    return segments


def merge_scenes_and_asr(
    scene_md: str,
    asr_text: str,
    *,
    title: str = "",
) -> str:
    """合并场景识别和 ASR 文本，按时间对齐输出。

    当 ASR 只有一个覆盖整段视频的 segment 时，将完整转写放在文档末尾
    而非重复附加到每个场景。

    Args:
        scene_md: 短视频 LLM 识别输出（包含 <!-- meta:scene ... --> 标记）。
        asr_text: ASR 转写文本（可能包含时间戳段落）。
        title: 视频标题。

    Returns:
        合并后的 Markdown 文本。
    """
    scenes = parse_scene_blocks(scene_md)
    asr_segments = parse_asr_segments(asr_text)

    # 判断 ASR 是否为单一大段（无法按场景对齐）
    single_bulk_asr = (
        len(asr_segments) == 1
        and (asr_segments[0][1] == float("inf")
             or asr_segments[0][1] >= (scenes[-1].end_sec if scenes else 0))
    )

    lines: list[str] = []
    if title:
        lines.append(f"<!-- meta:social_video title={title} -->")
        lines.append("")

    for scene in scenes:
        lines.append(f"<!-- meta:scene id={scene.scene_id} time={scene.time_range} -->")
        lines.append("")

        # 场景画面描述
        if scene.content:
            lines.append(scene.content)
            lines.append("")

        # 只在 ASR 有多段时才按场景内联语音
        if not single_bulk_asr:
            matched_asr: list[str] = []
            for asr_start, asr_end, asr_content in asr_segments:
                if asr_start < scene.end_sec and asr_end > scene.start_sec:
                    matched_asr.append(asr_content)
            if matched_asr:
                lines.append("> **语音内容：**")
                for asr_line in matched_asr:
                    lines.append(f"> {asr_line}")
                lines.append("")

    # 单一大段 ASR：放在文档末尾
    if single_bulk_asr and asr_segments:
        lines.append("---")
        lines.append("")
        lines.append("## 语音转写")
        lines.append("")
        lines.append(asr_segments[0][2])
        lines.append("")

    return "\n".join(lines)
