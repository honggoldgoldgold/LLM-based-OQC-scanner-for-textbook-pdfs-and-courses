"""Build and size one preflighted DashScope image request."""

from __future__ import annotations

import base64
import json
from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any

from ...errors import InvalidSource
from ...imaging.decode_image_bytes import decode_image_bytes
from ...imaging.decoded_image_info import DecodedImageInfo
from ...raise_if_cancelled import raise_if_cancelled
from ...validate_image_group import MAX_AGGREGATE_PIXELS

if TYPE_CHECKING:
    from .provider_settings import DashScopeSettings


MAX_DATA_URL_UTF8_BYTES = 10_000_000
MAX_SERIALIZED_REQUEST_UTF8_BYTES = 20_971_520
MAX_HIGH_RESOLUTION_PIXELS = 16_777_216
MIN_IMAGE_DIMENSION_EXCLUSIVE = 10
MAX_IMAGE_ASPECT_RATIO = 200
MAX_IMAGE_LONG_SIDE = 7_680
MAX_COMPLETION_TOKENS = 16_384

_MIME_TYPE_BY_DECODED_FORMAT = {
    "JPEG": "image/jpeg",
    "PNG": "image/png",
}


@dataclass(frozen=True, slots=True, kw_only=True)
class DashScopeImageRequest:
    """Hold immutable request values without exposing source content in repr."""

    _model: str = field(repr=False)
    _data_urls: tuple[str, ...] = field(repr=False)
    _prompt: str = field(repr=False)
    _enable_thinking: bool = field(repr=False)
    _vl_high_resolution_images: bool = field(repr=False)
    serialized_byte_count: int

    @property
    def kwargs(self) -> dict[str, Any]:
        """Return fresh containers for ``chat.completions.create``."""
        return _build_openai_create_kwargs(
            model=self._model,
            data_urls=self._data_urls,
            prompt=self._prompt,
            enable_thinking=self._enable_thinking,
            vl_high_resolution_images=self._vl_high_resolution_images,
        )


def build_dashscope_image_request(
    image_paths: Sequence[Path],
    *,
    prompt: str,
    model: str,
    settings: DashScopeSettings,
    cancellation: object | None = None,
) -> DashScopeImageRequest:
    """Read ordered snapshots and return one request after all local preflight."""
    raise_if_cancelled(cancellation)
    source_paths = _coerce_snapshot_paths(image_paths)
    data_urls: list[str] = []
    aggregate_pixels = 0
    for image_index, source_path in enumerate(source_paths):
        raise_if_cancelled(cancellation)
        data_url, pixel_count = _build_data_url(
            source_path,
            image_index=image_index,
            high_resolution=settings.vl_high_resolution_images,
        )
        raise_if_cancelled(cancellation)
        aggregate_pixels += pixel_count
        if aggregate_pixels > MAX_AGGREGATE_PIXELS:
            raise InvalidSource(
                "The final provider image group exceeds the aggregate pixel limit.",
                code="SOURCE_TOO_LARGE",
                details={
                    "aggregate_pixel_count": aggregate_pixels,
                    "maximum_aggregate_pixel_count": MAX_AGGREGATE_PIXELS,
                },
            ) from None
        data_urls.append(data_url)

    immutable_data_urls = tuple(data_urls)
    serialized_byte_count = _serialized_wire_body_byte_count(
        model=model,
        data_urls=immutable_data_urls,
        prompt=prompt,
        enable_thinking=settings.enable_thinking,
        vl_high_resolution_images=settings.vl_high_resolution_images,
    )
    if serialized_byte_count > MAX_SERIALIZED_REQUEST_UTF8_BYTES:
        raise InvalidSource(
            "The image request exceeds the 20 MiB provider payload limit.",
            code="SOURCE_TOO_LARGE",
            details={
                "serialized_byte_count": serialized_byte_count,
                "maximum_serialized_byte_count": MAX_SERIALIZED_REQUEST_UTF8_BYTES,
            },
        ) from None

    return DashScopeImageRequest(
        _model=model,
        _data_urls=immutable_data_urls,
        _prompt=prompt,
        _enable_thinking=settings.enable_thinking,
        _vl_high_resolution_images=settings.vl_high_resolution_images,
        serialized_byte_count=serialized_byte_count,
    )


def _coerce_snapshot_paths(image_paths: Sequence[Path]) -> tuple[Path, ...]:
    if isinstance(image_paths, (str, bytes, Path)):
        raise InvalidSource(
            "The provider image request requires an ordered image group.",
            code="SOURCE_INVALID",
        ) from None
    try:
        source_paths = tuple(Path(source) for source in image_paths)
    except Exception:
        raise InvalidSource(
            "The provider image request contains an invalid snapshot path.",
            code="SOURCE_INVALID",
        ) from None
    if not source_paths:
        raise InvalidSource(
            "The provider image request requires at least one image.",
            code="SOURCE_INVALID",
        ) from None
    return source_paths


def _build_data_url(
    source_path: Path,
    *,
    image_index: int,
    high_resolution: bool,
) -> tuple[str, int]:
    byte_size = _snapshot_byte_size(source_path)
    maximum_possible_source_bytes = _maximum_source_bytes_for_any_supported_data_url()
    if byte_size > maximum_possible_source_bytes:
        _raise_data_url_too_large(
            image_index=image_index,
            source_byte_count=byte_size,
            prefix=_shortest_supported_data_url_prefix(),
        )

    source_bytes = _read_snapshot_bytes(
        source_path,
        maximum_source_bytes=maximum_possible_source_bytes,
    )
    if len(source_bytes) != byte_size:
        del source_bytes
        raise InvalidSource(
            "A validated image snapshot changed during provider preflight.",
            code="SOURCE_INVALID",
            details={"image_index": image_index},
        ) from None
    decoded = decode_image_bytes(source_bytes, suffix=source_path.suffix)
    _validate_dashscope_dimensions(
        decoded,
        image_index=image_index,
        high_resolution=high_resolution,
    )

    mime_type = _MIME_TYPE_BY_DECODED_FORMAT.get(decoded.format)
    if mime_type is None:
        raise InvalidSource(
            "The decoded image format is not valid for a provider request.",
            code="SOURCE_INVALID",
            details={"image_index": image_index},
        ) from None

    prefix = f"data:{mime_type};base64,"
    maximum_source_bytes = _maximum_source_bytes_for_data_url(prefix)
    if byte_size > maximum_source_bytes:
        _raise_data_url_too_large(
            image_index=image_index,
            source_byte_count=byte_size,
            prefix=prefix,
        )

    try:
        encoded = base64.b64encode(source_bytes).decode("ascii")
        data_url = f"{prefix}{encoded}"
        data_url_byte_count = len(data_url)
    except MemoryError:
        raise InvalidSource(
            "The image could not be encoded within safe memory limits.",
            code="SOURCE_TOO_LARGE",
            details={"image_index": image_index},
        ) from None
    finally:
        del source_bytes
    if data_url_byte_count > MAX_DATA_URL_UTF8_BYTES:
        raise InvalidSource(
            "An encoded image exceeds the provider data-URL limit.",
            code="SOURCE_TOO_LARGE",
            details={
                "image_index": image_index,
                "data_url_byte_count": data_url_byte_count,
                "maximum_data_url_byte_count": MAX_DATA_URL_UTF8_BYTES,
            },
        ) from None
    return data_url, decoded.pixel_count


def _snapshot_byte_size(source_path: Path) -> int:
    try:
        return source_path.stat().st_size
    except FileNotFoundError:
        raise InvalidSource(
            "A validated image snapshot is no longer available.",
            code="SOURCE_NOT_FOUND",
        ) from None
    except ValueError:
        raise InvalidSource(
            "A validated image snapshot path is invalid.",
            code="SOURCE_INVALID",
        ) from None
    except OSError:
        raise InvalidSource(
            "A validated image snapshot cannot be inspected.",
            code="SOURCE_UNREADABLE",
        ) from None


def _read_snapshot_bytes(
    source_path: Path,
    *,
    maximum_source_bytes: int,
) -> bytes:
    try:
        with source_path.open("rb") as source_stream:
            source_bytes = source_stream.read(maximum_source_bytes + 1)
    except FileNotFoundError:
        raise InvalidSource(
            "A validated image snapshot is no longer available.",
            code="SOURCE_NOT_FOUND",
        ) from None
    except ValueError:
        raise InvalidSource(
            "A validated image snapshot path is invalid.",
            code="SOURCE_INVALID",
        ) from None
    except MemoryError:
        raise InvalidSource(
            "The image could not be read within safe memory limits.",
            code="SOURCE_TOO_LARGE",
        ) from None
    except OSError:
        raise InvalidSource(
            "A validated image snapshot cannot be read.",
            code="SOURCE_UNREADABLE",
        ) from None

    if len(source_bytes) > maximum_source_bytes:
        del source_bytes
        raise InvalidSource(
            "An encoded image exceeds the provider data-URL limit.",
            code="SOURCE_TOO_LARGE",
            details={"maximum_data_url_byte_count": MAX_DATA_URL_UTF8_BYTES},
        ) from None
    return source_bytes


def _maximum_source_bytes_for_data_url(prefix: str) -> int:
    remaining_bytes = MAX_DATA_URL_UTF8_BYTES - len(prefix.encode("utf-8"))
    if remaining_bytes < 4:
        return 0
    return (remaining_bytes // 4) * 3


def _maximum_source_bytes_for_any_supported_data_url() -> int:
    return max(
        _maximum_source_bytes_for_data_url(f"data:{mime_type};base64,")
        for mime_type in _MIME_TYPE_BY_DECODED_FORMAT.values()
    )


def _shortest_supported_data_url_prefix() -> str:
    return min(
        (f"data:{mime_type};base64," for mime_type in _MIME_TYPE_BY_DECODED_FORMAT.values()),
        key=lambda prefix: len(prefix.encode("utf-8")),
    )


def _raise_data_url_too_large(
    *,
    image_index: int,
    source_byte_count: int,
    prefix: str,
) -> None:
    predicted_byte_count = len(prefix.encode("utf-8")) + 4 * (
        (source_byte_count + 2) // 3
    )
    raise InvalidSource(
        "An encoded image exceeds the provider data-URL limit.",
        code="SOURCE_TOO_LARGE",
        details={
            "image_index": image_index,
            "data_url_byte_count": predicted_byte_count,
            "maximum_data_url_byte_count": MAX_DATA_URL_UTF8_BYTES,
        },
    ) from None


def _validate_dashscope_dimensions(
    decoded: DecodedImageInfo,
    *,
    image_index: int,
    high_resolution: bool,
) -> None:
    if (
        decoded.width <= MIN_IMAGE_DIMENSION_EXCLUSIVE
        or decoded.height <= MIN_IMAGE_DIMENSION_EXCLUSIVE
    ):
        raise InvalidSource(
            "A provider image must be greater than 10 pixels in each dimension.",
            code="SOURCE_INVALID",
            details={
                "image_index": image_index,
                "width": decoded.width,
                "height": decoded.height,
            },
        ) from None

    short_side = min(decoded.width, decoded.height)
    long_side = max(decoded.width, decoded.height)
    if long_side > MAX_IMAGE_ASPECT_RATIO * short_side:
        raise InvalidSource(
            "A provider image exceeds the 200:1 aspect-ratio limit.",
            code="SOURCE_INVALID",
            details={
                "image_index": image_index,
                "width": decoded.width,
                "height": decoded.height,
            },
        ) from None

    if long_side > MAX_IMAGE_LONG_SIDE:
        raise InvalidSource(
            "A provider image exceeds the 8K longest-side limit.",
            code="SOURCE_TOO_LARGE",
            details={
                "image_index": image_index,
                "long_side": long_side,
                "maximum_long_side": MAX_IMAGE_LONG_SIDE,
            },
        ) from None

    if high_resolution and decoded.pixel_count > MAX_HIGH_RESOLUTION_PIXELS:
        raise InvalidSource(
            "A high-resolution provider image exceeds its pixel limit.",
            code="SOURCE_TOO_LARGE",
            details={
                "image_index": image_index,
                "pixel_count": decoded.pixel_count,
                "maximum_pixel_count": MAX_HIGH_RESOLUTION_PIXELS,
            },
        ) from None


def _build_openai_create_kwargs(
    *,
    model: str,
    data_urls: tuple[str, ...],
    prompt: str,
    enable_thinking: bool,
    vl_high_resolution_images: bool,
) -> dict[str, Any]:
    return {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    *(
                        {"type": "image_url", "image_url": {"url": data_url}}
                        for data_url in data_urls
                    ),
                    {"type": "text", "text": prompt},
                ],
            }
        ],
        "temperature": 0,
        "max_completion_tokens": MAX_COMPLETION_TOKENS,
        "extra_body": {
            "enable_thinking": enable_thinking,
            "vl_high_resolution_images": vl_high_resolution_images,
        },
    }


def _serialized_wire_body_byte_count(
    *,
    model: str,
    data_urls: tuple[str, ...],
    prompt: str,
    enable_thinking: bool,
    vl_high_resolution_images: bool,
) -> int:
    wire_body = _build_openai_create_kwargs(
        model=model,
        data_urls=data_urls,
        prompt=prompt,
        enable_thinking=enable_thinking,
        vl_high_resolution_images=vl_high_resolution_images,
    )
    extra_body = wire_body.pop("extra_body")
    wire_body.update(extra_body)
    try:
        serialized = json.dumps(
            wire_body,
            ensure_ascii=False,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    except MemoryError:
        raise InvalidSource(
            "The image request could not be sized within safe memory limits.",
            code="SOURCE_TOO_LARGE",
        ) from None
    except (OverflowError, TypeError, ValueError):
        raise InvalidSource(
            "The image request could not be serialized safely.",
            code="SOURCE_INVALID",
        ) from None
    return len(serialized)
