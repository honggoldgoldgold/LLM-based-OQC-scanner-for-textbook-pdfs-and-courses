"""Decode and validate one immutable PNG or JPEG byte buffer."""

from __future__ import annotations

import warnings
from io import BytesIO
from typing import Any

from ..errors import DependencyMissing, InvalidSource
from ..validate_source import MAX_SOURCE_BYTES
from .decoded_image_info import DecodedImageInfo


MAX_IMAGE_PIXELS = 24_000_000
_EXPECTED_FORMAT_BY_SUFFIX = {
    ".png": "PNG",
    ".jpg": "JPEG",
    ".jpeg": "JPEG",
}


def decode_image_bytes(image_bytes: bytes, *, suffix: str) -> DecodedImageInfo:
    """Verify and fully load exact bounded bytes twice, then close Pillow."""
    if type(image_bytes) is not bytes or not image_bytes:
        raise InvalidSource(
            "The image byte buffer is empty or invalid.",
            code="SOURCE_INVALID",
        ) from None
    if len(image_bytes) > MAX_SOURCE_BYTES:
        raise InvalidSource(
            "The image byte buffer exceeds the 25 MiB safety limit.",
            code="SOURCE_TOO_LARGE",
        ) from None
    if type(suffix) is not str:
        raise InvalidSource(
            "The image suffix is invalid.",
            code="SOURCE_INVALID",
        ) from None
    expected_format = _EXPECTED_FORMAT_BY_SUFFIX.get(suffix.casefold())
    if expected_format is None:
        raise InvalidSource(
            "The image suffix is not valid for PNG/JPEG decoding.",
            code="SOURCE_INVALID",
        ) from None

    image_module, unidentified_image_error = _load_pillow()
    bomb_warning = image_module.DecompressionBombWarning
    bomb_error = image_module.DecompressionBombError
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", bomb_warning)
            with image_module.open(BytesIO(image_bytes)) as image:
                info = _inspect_image(image, expected_format=expected_format)
                image.verify()

            with image_module.open(BytesIO(image_bytes)) as image:
                loaded_info = _inspect_image(image, expected_format=expected_format)
                image.load()
    except (bomb_warning, bomb_error) as error:
        raise InvalidSource(
            "The image exceeds safe decompression limits.",
            code="SOURCE_TOO_LARGE",
        ) from error
    except unidentified_image_error as error:
        raise InvalidSource(
            "The image bytes are corrupt or are not a recognized image.",
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
            "The image bytes could not be decoded completely.",
            code="SOURCE_INVALID",
        ) from error

    if info != loaded_info:
        raise InvalidSource(
            "The image metadata changed while its bytes were decoded.",
            code="SOURCE_INVALID",
        ) from None
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
    if (
        not isinstance(width, int)
        or not isinstance(height, int)
        or width <= 0
        or height <= 0
    ):
        raise InvalidSource(
            "The image has invalid dimensions.",
            code="SOURCE_INVALID",
        )

    pixel_count = width * height
    if pixel_count > MAX_IMAGE_PIXELS:
        raise InvalidSource(
            "The image exceeds the 24,000,000-pixel safety limit.",
            code="SOURCE_TOO_LARGE",
            details={
                "pixel_count": pixel_count,
                "maximum_pixel_count": MAX_IMAGE_PIXELS,
            },
        )

    image_format = image.format
    if image_format != expected_format:
        raise InvalidSource(
            "The decoded image format does not match its file extension.",
            code="SOURCE_INVALID",
            details={
                "decoded_format": image_format,
                "expected_format": expected_format,
            },
        )
    return DecodedImageInfo(format=image_format, width=width, height=height)
