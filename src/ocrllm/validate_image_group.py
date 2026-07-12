"""Validate all byte, count, decode, and pixel limits for one image group."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

from .errors import InvalidSource
from .image_group_limits import (
    MAX_AGGREGATE_PIXELS,
    MAX_AGGREGATE_SOURCE_BYTES,
    MAX_IMAGE_GROUP_COUNT,
)
from .imaging.decode_image import DecodedImageInfo, decode_image
from .validate_source import validate_source


def validate_image_group(sources: Sequence[str | Path]) -> tuple[DecodedImageInfo, ...]:
    """Validate one ordered image group before any provider can be called."""
    source_paths = tuple(Path(source) for source in sources)
    if not source_paths:
        raise InvalidSource(
            "Image recognition requires at least one source.",
            code="SOURCE_INVALID",
        )
    if len(source_paths) > MAX_IMAGE_GROUP_COUNT:
        raise InvalidSource(
            "An image group exceeds the 10-image safety limit.",
            code="SOURCE_TOO_LARGE",
            details={
                "image_count": len(source_paths),
                "maximum_image_count": MAX_IMAGE_GROUP_COUNT,
            },
        )

    byte_sizes = tuple(validate_source(source_path) for source_path in source_paths)
    aggregate_bytes = sum(byte_sizes)
    if aggregate_bytes > MAX_AGGREGATE_SOURCE_BYTES:
        raise InvalidSource(
            "The image group exceeds the 100 MiB aggregate source limit.",
            code="SOURCE_TOO_LARGE",
            details={
                "aggregate_byte_size": aggregate_bytes,
                "maximum_aggregate_byte_size": MAX_AGGREGATE_SOURCE_BYTES,
            },
        )

    decoded_images: list[DecodedImageInfo] = []
    aggregate_pixels = 0
    for source_path in source_paths:
        decoded_image = decode_image(source_path)
        aggregate_pixels += decoded_image.pixel_count
        if aggregate_pixels > MAX_AGGREGATE_PIXELS:
            raise InvalidSource(
                "The image group exceeds the 64,000,000-pixel aggregate safety limit.",
                code="SOURCE_TOO_LARGE",
                details={
                    "aggregate_pixel_count": aggregate_pixels,
                    "maximum_aggregate_pixel_count": MAX_AGGREGATE_PIXELS,
                },
            )
        decoded_images.append(decoded_image)
    return tuple(decoded_images)
