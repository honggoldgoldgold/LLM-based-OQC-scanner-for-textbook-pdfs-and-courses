"""Coerce one public source argument into an ordered path tuple."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

from .errors import InvalidSource


def coerce_source_paths(
    source: str | Path | Sequence[str | Path],
) -> tuple[Path, ...]:
    """Return a nonempty ordered tuple of paths without touching the filesystem."""
    if isinstance(source, (str, Path)):
        paths = (Path(source),)
    else:
        try:
            paths = tuple(Path(item) for item in source)
        except (TypeError, ValueError) as error:
            raise InvalidSource(
                "Every recognition source must be a filesystem path.",
                code="SOURCE_INVALID",
            ) from error
    if not paths:
        raise InvalidSource(
            "recognize() requires at least one source path.",
            code="SOURCE_INVALID",
        )
    return paths
