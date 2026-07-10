"""Decode and validate one Phase 0 image with a lazy Pillow import."""

from __future__ import annotations

import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..errors import DependencyMissing, InvalidSource


MAX_IMAGE_PIXELS = 24_000_000
_EXPECTED_FORMAT_BY_SUFFIX = {
    ".png": "PNG",
    ".jpg": "JPEG",
    ".jpeg": "JPEG",
}


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


def decode_image(source: str | Path) -> DecodedImageInfo:
    """Verify and fully load one bounded PNG or JPEG, then close it.

    Pillow is imported only when this function is called. Its process-global
    decompression-bomb threshold is never changed; warnings are promoted only
    inside a local warnings context.
    """
    image_module, unidentified_image_error = _load_pillow()
    source_path = Path(source)
    expected_format = _EXPECTED_FORMAT_BY_SUFFIX.get(source_path.suffix.casefold())
    if expected_format is None:
        raise InvalidSource(
            "The image source suffix is not valid for Phase 0 decoding.",
            code="SOURCE_INVALID",
        )

    bomb_warning = image_module.DecompressionBombWarning
    bomb_error = image_module.DecompressionBombError
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", bomb_warning)
            with image_module.open(source_path) as image:
                info = _inspect_image(image, expected_format=expected_format)
                image.verify()

            with image_module.open(source_path) as image:
                loaded_info = _inspect_image(image, expected_format=expected_format)
                image.load()
    except (bomb_warning, bomb_error) as error:
        raise InvalidSource(
            "The image exceeds safe decompression limits.",
            code="SOURCE_TOO_LARGE",
        ) from error
    except unidentified_image_error as error:
        raise InvalidSource(
            "The image source is corrupt or is not a recognized image.",
            code="SOURCE_INVALID",
        ) from error
    except InvalidSource:
        raise
    except MemoryError as error:
        raise InvalidSource(
            "The image could not be decoded within safe memory limits.",
            code="SOURCE_TOO_LARGE",
        ) from error
    except Exception as error:
        raise InvalidSource(
            "The image source could not be decoded completely.",
            code="SOURCE_INVALID",
        ) from error

    if info != loaded_info:
        raise InvalidSource(
            "The image metadata changed while it was being decoded.",
            code="SOURCE_INVALID",
        )
    return loaded_info


def _load_pillow() -> tuple[Any, type[BaseException]]:
    try:
        from PIL import Image, UnidentifiedImageError
    except (ImportError, OSError) as error:
        raise DependencyMissing(
            "Image validation requires the optional 'image' extra.",
            details={"extra": "image"},
        ) from error
    return Image, UnidentifiedImageError


def _inspect_image(image: Any, *, expected_format: str) -> DecodedImageInfo:
    width, height = image.size
    if not isinstance(width, int) or not isinstance(height, int) or width <= 0 or height <= 0:
        raise InvalidSource(
            "The image has invalid dimensions.",
            code="SOURCE_INVALID",
        )

    pixel_count = width * height
    if pixel_count > MAX_IMAGE_PIXELS:
        raise InvalidSource(
            "The image exceeds the 24,000,000-pixel safety limit.",
            code="SOURCE_TOO_LARGE",
            details={"pixel_count": pixel_count, "maximum_pixel_count": MAX_IMAGE_PIXELS},
        )

    image_format = image.format
    if image_format != expected_format:
        raise InvalidSource(
            "The decoded image format does not match its file extension.",
            code="SOURCE_INVALID",
            details={"decoded_format": image_format, "expected_format": expected_format},
        )
    return DecodedImageInfo(format=image_format, width=width, height=height)
