"""Read one bounded image path once and validate those exact bytes."""

from __future__ import annotations

from pathlib import Path

from ..errors import InvalidSource
from ..validate_source import MAX_SOURCE_BYTES
from .decode_image_bytes import decode_image_bytes
from .decoded_image_info import DecodedImageInfo


def decode_image(source: str | Path) -> DecodedImageInfo:
    """Read one path once, then verify and fully decode the captured bytes."""
    source_path = Path(source)
    image_bytes = _read_image_bytes_bounded(source_path)
    return decode_image_bytes(image_bytes, suffix=source_path.suffix)


def _read_image_bytes_bounded(source_path: Path) -> bytes:
    try:
        with source_path.open("rb") as source_stream:
            image_bytes = source_stream.read(MAX_SOURCE_BYTES + 1)
    except FileNotFoundError:
        raise InvalidSource(
            "The image source is no longer available.",
            code="SOURCE_NOT_FOUND",
        ) from None
    except ValueError:
        raise InvalidSource(
            "The image source path is invalid.",
            code="SOURCE_INVALID",
        ) from None
    except MemoryError:
        raise InvalidSource(
            "The image source could not be read within safe memory limits.",
            code="SOURCE_TOO_LARGE",
        ) from None
    except OSError:
        raise InvalidSource(
            "The image source could not be read.",
            code="SOURCE_UNREADABLE",
        ) from None

    if not image_bytes:
        raise InvalidSource(
            "The image source is empty.",
            code="SOURCE_INVALID",
        ) from None
    if len(image_bytes) > MAX_SOURCE_BYTES:
        raise InvalidSource(
            "The image source exceeds the 25 MiB safety limit.",
            code="SOURCE_TOO_LARGE",
        ) from None
    return image_bytes
