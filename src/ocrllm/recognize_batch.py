"""Recognize independent requests in caller order."""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from pathlib import Path
from typing import TYPE_CHECKING

from .config import Config
from .errors import ConfigError
from .recognize import recognize

if TYPE_CHECKING:
    from .result import RecognitionResult


def recognize_batch(
    sources: Iterable[str | Path | Sequence[str | Path]],
    *,
    config: Config | None = None,
) -> list[RecognitionResult]:
    """Return one result per independent source using fail-fast semantics."""
    if config is None:
        cfg = Config()
    elif isinstance(config, Config):
        cfg = config
    else:
        raise ConfigError("config must be a Config instance", code="CONFIG_INVALID")
    return [recognize(source, config=cfg) for source in sources]
