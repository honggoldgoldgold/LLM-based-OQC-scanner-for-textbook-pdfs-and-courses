"""
Board markdown merge utilities.

The merge is intentionally conservative:
1. Keep first occurrence of each non-trivial line.
2. Use fuzzy matching only inside a recent sliding window.
3. Never drop content when the frame structure cannot be detected reliably.
"""

from __future__ import annotations

import logging
import re
from collections import OrderedDict
from difflib import SequenceMatcher

logger = logging.getLogger(__name__)

_FRAME_ID_RE = re.compile(r"(board_\d+_\d+s)", flags=re.IGNORECASE)
_FRAME_TIME_RE = re.compile(r"\[\s*时间\s*[:：]\s*(\d{1,3}:\d{2})\s*\]")

# 新格式: <!-- meta:frame id=board_001_030s time=00:30 -->
_FRAME_META_RE = re.compile(
    r"^<!--\s*meta:frame\s+id=(\S+?)(?:\s+time=(\d{1,3}:\d{2}))?\s*-->$"
)
# 旧格式: 以 # 开头并包含 board_xxx_xxxs 和 [时间: XX:XX]
_FRAME_HEADER_LEGACY_RE = re.compile(r"^#")

_LATEX_NORMALIZE = [
    (r"\leqslant", r"\leq"),
    (r"\geqslant", r"\geq"),
    (r"\Rightarrow", r"\implies"),
    (r"\Leftarrow", r"\impliedby"),
    (r"\langle", r"<"),
    (r"\rangle", r">"),
    (r"\quad", " "),
    (r"\qquad", " "),
    (r"\,", ""),
    (r"\;", ""),
    (r"\!", ""),
    (r"\ ", ""),
]

_FUZZY_WINDOW = 1000


def normalize_line(line: str) -> str:
    """对行文本进行归一化：去除 LaTeX 间隔命令、空格和美元符号。

    Args:
        line: 原始行文本。

    Returns:
        归一化后的字符串，用于模糊匹配比较。
    """
    s = line.strip()
    if not s:
        return ""
    for old, new in _LATEX_NORMALIZE:
        s = s.replace(old, new)
    s = re.sub(r"\s+", "", s)
    s = s.replace("$", "")
    return s


def _is_trivial(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return True
    core = re.sub(r"[\s$]", "", stripped)
    return len(core) < 4


def _time_to_seconds(time_str: str) -> int:
    minutes, seconds = time_str.split(":")
    return int(minutes) * 60 + int(seconds)


def _parse_frame_header(line: str) -> tuple[str, str] | None:
    """解析帧标记行，支持新旧两种格式。

    新格式: <!-- meta:frame id=board_001_030s time=00:30 -->
    旧格式: # board_001_030s [时间: 00:30]

    Returns:
        (frame_id, time_str) 或 None。
    """
    stripped = line.strip()

    # 新格式
    m = _FRAME_META_RE.match(stripped)
    if m:
        frame_id = m.group(1)
        # 去掉可能的 .jpg 后缀作为 frame_id（兼容原有逻辑）
        frame_id_match = _FRAME_ID_RE.search(frame_id)
        time_str = m.group(2)
        if frame_id_match and time_str:
            return frame_id_match.group(1), time_str
        if frame_id_match:
            return frame_id_match.group(1), "00:00"
        return None

    # 旧格式
    if not stripped.startswith("#"):
        return None

    frame_match = _FRAME_ID_RE.search(stripped)
    time_match = _FRAME_TIME_RE.search(stripped)
    if not frame_match or not time_match:
        return None

    return frame_match.group(1), time_match.group(1)


def _fuzzy_match_window(
    norm: str,
    recent_keys: list[str],
    threshold: float,
) -> str | None:
    if not norm or not recent_keys:
        return None

    norm_len = len(norm)
    len_ratio_min = threshold / (2.0 - threshold)
    window = recent_keys[-_FUZZY_WINDOW:] if len(recent_keys) > _FUZZY_WINDOW else recent_keys

    for key in reversed(window):
        key_len = len(key)
        if key_len == 0:
            continue
        if min(norm_len, key_len) / max(norm_len, key_len) < len_ratio_min:
            continue
        if SequenceMatcher(None, norm, key).ratio() >= threshold:
            return key
    return None


def _parse_frames(md_text: str) -> list[dict]:
    frames: list[dict] = []
    current: dict | None = None

    for raw_line in md_text.splitlines():
        header = _parse_frame_header(raw_line)
        if header is not None:
            if current is not None:
                frames.append(current)

            frame_id, time_str = header
            current = {
                "frame_id": frame_id,
                "time_str": time_str,
                "time_seconds": _time_to_seconds(time_str),
                "frame_idx": len(frames),
                "header": raw_line,
                "lines": [],
            }
            continue

        if current is not None:
            current["lines"].append(raw_line)

    if current is not None:
        frames.append(current)

    return frames


def _detect_segments(
    seen_lines: OrderedDict,
    gap_frames: int = 5,
) -> list[list[tuple[str, dict]]]:
    segments: list[list[tuple[str, dict]]] = []
    current_seg: list[tuple[str, dict]] = []
    prev_order = -1

    for line_text, info in seen_lines.items():
        order_idx = info["order_idx"]
        if current_seg and (order_idx - prev_order) > gap_frames:
            segments.append(current_seg)
            current_seg = []
        current_seg.append((line_text, info))
        prev_order = order_idx

    if current_seg:
        segments.append(current_seg)

    return segments


def merge_board_md(
    md_text: str,
    *,
    similarity_threshold: float = 0.85,
    segment_gap_frames: int = 5,
) -> str:
    """保守合并板书识别结果，去除帧间重复内容。

    流程: 按时间排序帧 → 逐行精确/模糊去重 → 按 gap 分段 → 生成分段 Markdown。

    Args:
        md_text: 原始拼接的 Markdown 文本（含帧标题）。
        similarity_threshold: 模糊匹配阈值 (0~1)，越高越严格。
        segment_gap_frames: 分段间隔帧数。

    Returns:
        合并后的 Markdown 字符串。
    """
    frames = _parse_frames(md_text)
    if not frames:
        logger.warning("[MERGE] 未检测到可识别的帧标题结构，返回原文")
        return md_text

    frames = sorted(frames, key=lambda frame: (frame["time_seconds"], frame["frame_idx"]))
    for order_idx, frame in enumerate(frames):
        frame["order_idx"] = order_idx

    total_lines_raw = sum(len(frame["lines"]) for frame in frames)

    seen: OrderedDict[str, dict] = OrderedDict()
    exact_seen: set[str] = set()
    recent_keys: list[str] = []

    for frame in frames:
        for raw_line in frame["lines"]:
            if _is_trivial(raw_line):
                continue

            norm = normalize_line(raw_line)
            if not norm or norm in exact_seen:
                continue

            matched_key = _fuzzy_match_window(norm, recent_keys, similarity_threshold)
            if matched_key is not None:
                continue

            exact_seen.add(norm)
            recent_keys.append(norm)
            seen[norm] = {
                "original": raw_line.strip(),
                "frame_idx": frame["frame_idx"],
                "order_idx": frame["order_idx"],
                "frame_id": frame["frame_id"],
                "time_str": frame["time_str"],
                "time_seconds": frame["time_seconds"],
            }

    segments = _detect_segments(seen, gap_frames=segment_gap_frames)

    parts: list[str] = []
    for seg_i, seg in enumerate(segments):
        if not seg:
            continue

        first_time = seg[0][1]["time_str"]
        last_time = seg[-1][1]["time_str"]
        parts.append(f"<!-- meta:segment index={seg_i + 1} time={first_time}~{last_time} -->")
        parts.append("")

        for _norm, info in seg:
            parts.append(info["original"])

        parts.append("")

    merged_text = "\n".join(parts).rstrip() + "\n"
    unique_count = len(seen)
    logger.info(
        "[MERGE] 板书合并: %d 帧, %d 原始行 -> %d 唯一行 (%d 段, 压缩率 %.0f%%)",
        len(frames),
        total_lines_raw,
        unique_count,
        len(segments),
        (1 - unique_count / max(total_lines_raw, 1)) * 100,
    )
    return merged_text


def verify_no_loss(
    original_md: str,
    merged_md: str,
    *,
    similarity_threshold: float = 0.85,
) -> dict:
    """验证合并后是否有内容丢失。

    遍历原始帧中的每一行非平凡内容，检查是否在合并结果中找到精确或模糊匹配。

    Args:
        original_md: 合并前的原始 Markdown。
        merged_md: 合并后的 Markdown。
        similarity_threshold: 模糊匹配阈值。

    Returns:
        包含 total、matched、lost_count、lost_lines 的验证报告字典。
    """
    merged_exact: set[str] = set()
    # 按长度分桶，加速模糊匹配时的候选筛选
    merged_by_len: dict[int, list[str]] = {}
    for line in merged_md.splitlines():
        if _is_trivial(line):
            continue
        norm = normalize_line(line)
        if norm:
            merged_exact.add(norm)
            merged_by_len.setdefault(len(norm), []).append(norm)

    frames = _parse_frames(original_md)
    total = 0
    matched = 0
    lost: list[dict] = []
    len_ratio_min = similarity_threshold / (2.0 - similarity_threshold)

    for frame in frames:
        for raw_line in frame["lines"]:
            if _is_trivial(raw_line):
                continue

            norm = normalize_line(raw_line)
            if not norm:
                continue

            total += 1
            if norm in merged_exact:
                matched += 1
                continue

            # 模糊匹配：只在长度相近的桶内搜索
            found = False
            norm_len = len(norm)
            min_len = int(norm_len * len_ratio_min)
            max_len = int(norm_len / len_ratio_min) + 1 if len_ratio_min > 0 else norm_len * 3

            for bucket_len in range(min_len, max_len + 1):
                candidates = merged_by_len.get(bucket_len)
                if not candidates:
                    continue
                for merged_norm in candidates:
                    if SequenceMatcher(None, norm, merged_norm).ratio() >= similarity_threshold:
                        found = True
                        break
                if found:
                    break

            if found:
                matched += 1
            else:
                lost.append({
                    "line": raw_line.strip(),
                    "frame": frame["frame_id"],
                    "time": frame["time_str"],
                })

    return {
        "total_original_lines": total,
        "matched_lines": matched,
        "possibly_lost": lost,
        "loss_rate": (total - matched) / max(total, 1),
    }
