"""Validate the media type of one ordered recognition-source group."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import Literal

from .detect_source_type import detect_source_type
from .errors import InvalidSource


def validate_same_type_group(sources: Sequence[str | Path]) -> Literal["image"]:
    """Return the one canonical media type for a nonempty ordered group.

    Phase 0 authorizes image groups only, so any unsupported member is rejected
    by ``detect_source_type``. The caller's order is never changed.
    """
    if not sources:
        raise InvalidSource(
            "Recognition requires at least one source.",
            code="SOURCE_INVALID",
        )

    media_types = tuple(detect_source_type(source) for source in sources)
    first_media_type = media_types[0]
    if any(media_type != first_media_type for media_type in media_types[1:]):
        raise InvalidSource(
            "All sources in one recognize() call must have the same media type.",
            code="SOURCE_INVALID",
        )
    return first_media_type
