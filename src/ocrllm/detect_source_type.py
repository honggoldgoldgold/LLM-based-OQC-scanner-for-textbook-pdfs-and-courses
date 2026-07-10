"""Detect the canonical media type from one authorized source suffix."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from .errors import UnsupportedFormat


IMAGE_EXTENSIONS = frozenset({".png", ".jpg", ".jpeg"})


def detect_source_type(source: str | Path) -> Literal["image"]:
    """Return ``image`` for an authorized Phase 0 image suffix.

    Detection deliberately does not touch the filesystem or inspect content.
    ``validate_source`` and ``decode_image`` own those responsibilities.
    """
    suffix = Path(source).suffix.casefold()
    if suffix in IMAGE_EXTENSIONS:
        return "image"

    if not suffix:
        message = "The recognition source has no file extension."
    else:
        message = "The recognition source extension is not supported."
    raise UnsupportedFormat(
        message,
        details={"extension": suffix or None},
    )
