"""Describe one fully decoded image without retaining its pixel buffer."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DecodedImageInfo:
    """Small validated metadata retained after Pillow closes the image."""

    format: str
    width: int
    height: int

    @property
    def pixel_count(self) -> int:
        """Return the decoded width-by-height pixel count."""
        return self.width * self.height
