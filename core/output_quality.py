"""Shared checks for generated Markdown outputs before marking tasks complete."""

from __future__ import annotations

import re


_HTML_COMMENT_RE = re.compile(r"<!--.*?-->", flags=re.DOTALL)
_MARKDOWN_NOISE_RE = re.compile(r"[\s#>*_`~\-\[\](){}|:：,，.。;；!！?？/\\]+")
_FAILURE_MARKERS = ("识别失败", "OCR 失败")


def visible_text_char_count(markdown: str) -> int:
    """Count user-visible content characters, excluding metadata and failure comments."""
    without_comments = _HTML_COMMENT_RE.sub("", markdown or "")
    compact = _MARKDOWN_NOISE_RE.sub("", without_comments)
    return len(compact)


def failed_placeholder_quality_reason(
    markdown: str,
    *,
    expected_units: int,
    unit_name: str,
    min_chars_per_unit: int = 60,
    min_total_chars: int = 400,
) -> str | None:
    """Return a reason when failure placeholders dominate a generated output."""
    if not any(marker in (markdown or "") for marker in _FAILURE_MARKERS):
        return None
    minimum = max(min_total_chars, max(1, expected_units) * min_chars_per_unit)
    visible_chars = visible_text_char_count(markdown)
    if visible_chars < minimum:
        return (
            f"包含识别失败占位，且有效正文过少: {visible_chars} 字，"
            f"{expected_units} {unit_name}最低期望 {minimum} 字"
        )
    return None
