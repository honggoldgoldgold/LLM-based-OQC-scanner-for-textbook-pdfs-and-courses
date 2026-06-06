"""
LLM OCR response quality validation.

The validator runs before model text is treated as recognized markdown. It
rejects provider/API error payloads that can arrive with HTTP 200 and would
otherwise poison output files and resume checkpoints.
"""

from __future__ import annotations

import json
import re
from collections.abc import Iterable
from typing import Any


_HTML_RE = re.compile(r"<\s*(?:!doctype\s+html|html|body)\b", re.IGNORECASE)
_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
_STRUCTURAL_MARKER_RE = re.compile(
    r"<!--\s*meta:(?:frame\s+id=\S+|page\s+number=\d+)\b.*?-->",
    re.IGNORECASE | re.DOTALL,
)

_API_ERROR_KEYWORDS = (
    "insufficient_user_quota",
    "insufficient_quota",
    "quota_exceeded",
    "FreeAllocationQuotaExceeded",
    "AllocationQuota.FreeTierOnly",
    "FreeTierOnly",
    "invalid_api_key",
    "invalid_request_error",
    "rate_limit_exceeded",
    "billing_not_active",
    "account_deactivated",
    "用户额度不足",
    "账户额度不足",
    "额度不足",
    "余额不足",
    "欠费",
)


def validate_ocr_response(text: str, min_chars: int = 20) -> tuple[bool, str]:
    """Return whether an OCR LLM response is safe to write as markdown."""
    raw = "" if text is None else str(text)
    stripped = raw.strip()
    if not stripped:
        return False, "response is empty"

    if _HTML_RE.search(stripped):
        return False, "HTML error page detected"

    json_error = _json_error_reason(stripped)
    if json_error:
        return False, json_error

    keyword = _first_api_error_keyword(stripped)
    if keyword:
        return False, f"API error keyword detected: {keyword}"

    if _STRUCTURAL_MARKER_RE.search(stripped):
        return True, ""

    meaningful = _COMMENT_RE.sub("", stripped).strip()
    meaningful_chars = len(re.sub(r"\s+", "", meaningful))
    if meaningful_chars < max(0, min_chars):
        return False, f"response too short after comments: {meaningful_chars} chars"

    return True, ""


def ensure_valid_ocr_response(text: str, validation_cfg: Any, context: str):
    """Raise if configured OCR response validation rejects the text."""
    if validation_cfg is not None and not getattr(validation_cfg, "enabled", True):
        return
    min_chars = getattr(validation_cfg, "min_chars", 20)
    ok, reason = validate_ocr_response(text, min_chars=min_chars)
    if not ok:
        raise RuntimeError(f"{context} 响应质量验证失败: {reason}")


def _first_api_error_keyword(text: str) -> str | None:
    lower_text = text.lower()
    for keyword in _API_ERROR_KEYWORDS:
        if keyword.lower() in lower_text:
            return keyword
    return None


def _json_error_reason(text: str) -> str | None:
    if not text.lstrip().startswith("{"):
        return None
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return None
    if not isinstance(payload, dict):
        return None

    flattened = list(_flatten_json(payload))
    keys = {key.lower() for key, _value in flattened}
    values = [str(value) for _key, value in flattened if isinstance(value, (str, int, float))]

    has_error_shape = "error" in keys and ({"code", "message"} & keys)
    api_keyword = _first_api_error_keyword("\n".join(values))
    if has_error_shape or api_keyword:
        detail = api_keyword or _first_present_value(payload, ("code", "message", "type")) or "error"
        return f"JSON API error response detected: {detail}"
    return None


def _flatten_json(value: Any, prefix: str = "") -> Iterable[tuple[str, Any]]:
    if isinstance(value, dict):
        for key, child in value.items():
            key_text = str(key)
            yield key_text, child
            yield from _flatten_json(child, key_text)
    elif isinstance(value, list):
        for child in value:
            yield from _flatten_json(child, prefix)


def _first_present_value(payload: Any, names: tuple[str, ...]) -> str | None:
    wanted = {name.lower() for name in names}
    for key, value in _flatten_json(payload):
        if key.lower() in wanted and value not in (None, ""):
            return str(value)
    return None
