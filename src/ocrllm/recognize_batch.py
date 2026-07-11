"""Recognize independent requests in caller order."""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from pathlib import Path
from typing import TYPE_CHECKING

from .config import Config
from .recognize import recognize
from .validate_config import validate_config

if TYPE_CHECKING:
    from .result import RecognitionResult


def recognize_batch(
    sources: Iterable[str | Path | Sequence[str | Path]],
    *,
    config: Config | None = None,
) -> list[RecognitionResult]:
    """Return one result per independent source using fail-fast semantics."""
    cfg = validate_config(config)
    return [recognize(source, config=cfg) for source in sources]
