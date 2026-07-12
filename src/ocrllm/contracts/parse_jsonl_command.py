"""Decode one strict JSONL worker command record."""

from __future__ import annotations

import json
from typing import Any

from ocrllm.errors import OCRLLMError

from .parse_worker_command import parse_worker_command
from .worker_command import WorkerCommand


class _DuplicateJSONKey(ValueError):
    pass


def parse_jsonl_command(line: object) -> WorkerCommand:
    """Parse one JSON object, rejecting duplicate keys and non-finite numbers."""

    if not isinstance(line, str) or not line.strip():
        raise _invalid_json_command()
    try:
        value = json.loads(
            line,
            object_pairs_hook=_build_object_without_duplicate_keys,
            parse_constant=_reject_json_constant,
        )
    except (json.JSONDecodeError, TypeError, ValueError):
        raise _invalid_json_command() from None
    return parse_worker_command(value)


def _build_object_without_duplicate_keys(
    pairs: list[tuple[str, Any]],
) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise _DuplicateJSONKey
        result[key] = value
    return result


def _reject_json_constant(_: str) -> None:
    raise ValueError("non-finite JSON number")


def _invalid_json_command() -> OCRLLMError:
    return OCRLLMError("Worker command is invalid JSON.", code="COMMAND_INVALID")
