"""Reject image groups that exceed caller execution policy."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

from .errors import InvalidSource
from .config import Config
from .resolve_effective_image_limit import resolve_effective_image_limit


def validate_execution_image_count(
    source_paths: Sequence[Path],
    *,
    config: Config,
) -> None:
    """Fail before file access when a request exceeds its configured image cap."""
    image_count = len(source_paths)
    maximum_image_count, limit_source = resolve_effective_image_limit(config)
    if image_count > maximum_image_count:
        raise InvalidSource(
            "The image group exceeds the configured per-request image limit.",
            code="SOURCE_TOO_LARGE",
            details={
                "image_count": image_count,
                "maximum_image_count": maximum_image_count,
                "limit_source": limit_source,
            },
        ) from None
