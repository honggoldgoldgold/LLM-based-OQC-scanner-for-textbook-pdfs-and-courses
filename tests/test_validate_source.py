from __future__ import annotations

import builtins
import importlib
import warnings
from pathlib import Path

import pytest

from ocrllm.errors import DependencyMissing, InvalidSource, UnsupportedFormat
from ocrllm.imaging.decode_image import (
    MAX_IMAGE_PIXELS,
    DecodedImageInfo,
    decode_image,
)
from ocrllm.validate_image_group import (
    MAX_AGGREGATE_PIXELS,
    MAX_AGGREGATE_SOURCE_BYTES,
    MAX_IMAGE_GROUP_COUNT,
    validate_image_group,
)
from ocrllm.validate_source import MAX_SOURCE_BYTES, validate_source
from write_test_image import write_test_image


@pytest.mark.parametrize(
    ("suffix", "expected_format"),
    [(".png", "PNG"), (".jpg", "JPEG"), (".jpeg", "JPEG")],
)
def test_validate_and_decode_valid_phase_zero_images(tmp_path, suffix, expected_format):
    source = write_test_image(tmp_path / f"valid{suffix}")

    assert validate_source(source) == source.stat().st_size
    decoded = decode_image(source)

    assert decoded == DecodedImageInfo(format=expected_format, width=8, height=6)


def test_validate_source_reports_a_missing_file_before_decode(tmp_path):
    with pytest.raises(InvalidSource) as raised:
        validate_source(tmp_path / "missing.png")

    assert raised.value.code == "SOURCE_NOT_FOUND"


def test_validate_source_rejects_a_directory(tmp_path):
    source = tmp_path / "directory.png"
    source.mkdir()

    with pytest.raises(InvalidSource) as raised:
        validate_source(source)

    assert raised.value.code == "SOURCE_INVALID"


def test_validate_source_rejects_an_empty_file(tmp_path):
    source = tmp_path / "empty.png"
    source.touch()

    with pytest.raises(InvalidSource) as raised:
        validate_source(source)

    assert raised.value.code == "SOURCE_INVALID"


def test_validate_source_maps_open_failures_to_unreadable(tmp_path, monkeypatch):
    source = write_test_image(tmp_path / "unreadable.png")
    original_open = Path.open

    def deny_open(path, *args, **kwargs):
        if path == source:
            raise PermissionError("test-only denial")
        return original_open(path, *args, **kwargs)

    monkeypatch.setattr(Path, "open", deny_open)

    with pytest.raises(InvalidSource) as raised:
        validate_source(source)

    assert raised.value.code == "SOURCE_UNREADABLE"


def test_validate_source_accepts_the_exact_byte_limit(tmp_path):
    source = tmp_path / "at-limit.png"
    with source.open("wb") as source_file:
        source_file.write(b"x")
        source_file.truncate(MAX_SOURCE_BYTES)

    assert validate_source(source) == MAX_SOURCE_BYTES


def test_validate_source_rejects_one_byte_above_the_limit(tmp_path):
    source = tmp_path / "too-large.png"
    with source.open("wb") as source_file:
        source_file.write(b"x")
        source_file.truncate(MAX_SOURCE_BYTES + 1)

    with pytest.raises(InvalidSource) as raised:
        validate_source(source)

    assert raised.value.code == "SOURCE_TOO_LARGE"


def test_validate_source_rejects_an_unapproved_extension(tmp_path):
    source = tmp_path / "image.webp"
    source.write_bytes(b"not inspected because the suffix is unsupported")

    with pytest.raises(UnsupportedFormat) as raised:
        validate_source(source)

    assert raised.value.code == "UNSUPPORTED_FORMAT"


def test_validate_source_maps_an_invalid_path_to_source_invalid():
    with pytest.raises(InvalidSource) as raised:
        validate_source(Path("invalid\x00path.png"))

    assert raised.value.code == "SOURCE_INVALID"


def test_decode_image_rejects_corrupt_and_truncated_data(tmp_path):
    corrupt = tmp_path / "corrupt.png"
    corrupt.write_bytes(b"not an image")
    valid = write_test_image(tmp_path / "valid.png")
    truncated = tmp_path / "truncated.png"
    truncated.write_bytes(valid.read_bytes()[:-10])

    for source in (corrupt, truncated):
        with pytest.raises(InvalidSource) as raised:
            decode_image(source)
        assert raised.value.code == "SOURCE_INVALID"


def test_decode_image_rejects_content_that_does_not_match_the_suffix(tmp_path):
    from PIL import Image

    source = tmp_path / "claims-jpeg.jpg"
    Image.new("RGB", (8, 6)).save(source, format="PNG")

    with pytest.raises(InvalidSource) as raised:
        decode_image(source)

    assert raised.value.code == "SOURCE_INVALID"


def test_decode_image_maps_missing_pillow_to_the_image_extra(tmp_path, monkeypatch):
    source = write_test_image(tmp_path / "valid.png")
    original_import = builtins.__import__

    def import_without_pillow(name, *args, **kwargs):
        if name == "PIL" or name.startswith("PIL."):
            raise ModuleNotFoundError("test-only missing Pillow")
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", import_without_pillow)

    with pytest.raises(DependencyMissing) as raised:
        decode_image(source)

    assert raised.value.code == "DEPENDENCY_MISSING"
    assert raised.value.details["extra"] == "image"


def test_decode_image_does_not_change_pillow_global_pixel_limit(tmp_path):
    from PIL import Image

    source = write_test_image(tmp_path / "valid.png")
    original_limit = Image.MAX_IMAGE_PIXELS

    decode_image(source)

    assert Image.MAX_IMAGE_PIXELS == original_limit


def test_decode_image_rejects_dimensions_above_the_pixel_limit(tmp_path, monkeypatch):
    decode_module = importlib.import_module("ocrllm.imaging.decode_image")
    fake_module = _FakeImageModule(
        size=(MAX_IMAGE_PIXELS + 1, 1),
        image_format="PNG",
    )
    monkeypatch.setattr(decode_module, "_load_pillow", lambda: (fake_module, OSError))

    with pytest.raises(InvalidSource) as raised:
        decode_module.decode_image(tmp_path / "huge.png")

    assert raised.value.code == "SOURCE_TOO_LARGE"


def test_decode_image_accepts_the_exact_pixel_limit(tmp_path, monkeypatch):
    decode_module = importlib.import_module("ocrllm.imaging.decode_image")
    fake_module = _FakeImageModule(
        size=(MAX_IMAGE_PIXELS, 1),
        image_format="PNG",
    )
    monkeypatch.setattr(decode_module, "_load_pillow", lambda: (fake_module, OSError))

    decoded = decode_module.decode_image(tmp_path / "at-limit.png")

    assert decoded.pixel_count == MAX_IMAGE_PIXELS


def test_decode_image_maps_decompression_bomb_warning_to_too_large(tmp_path, monkeypatch):
    decode_module = importlib.import_module("ocrllm.imaging.decode_image")
    fake_module = _FakeImageModule(
        size=(1, 1),
        image_format="PNG",
        warn_about_bomb=True,
    )
    monkeypatch.setattr(decode_module, "_load_pillow", lambda: (fake_module, OSError))

    with pytest.raises(InvalidSource) as raised:
        decode_module.decode_image(tmp_path / "bomb.png")

    assert raised.value.code == "SOURCE_TOO_LARGE"


def test_validate_image_group_rejects_more_than_ten_before_file_access():
    sources = tuple(Path(f"{index}.png") for index in range(MAX_IMAGE_GROUP_COUNT + 1))

    with pytest.raises(InvalidSource) as raised:
        validate_image_group(sources)

    assert raised.value.code == "SOURCE_TOO_LARGE"


def test_validate_image_group_accepts_exactly_ten_images(monkeypatch):
    group_module = importlib.import_module("ocrllm.validate_image_group")
    sources = tuple(Path(f"{index}.png") for index in range(MAX_IMAGE_GROUP_COUNT))
    monkeypatch.setattr(group_module, "validate_source", lambda _source: 1)
    monkeypatch.setattr(
        group_module,
        "decode_image",
        lambda _source: DecodedImageInfo(format="PNG", width=1, height=1),
    )

    assert len(group_module.validate_image_group(sources)) == MAX_IMAGE_GROUP_COUNT


def test_validate_image_group_rejects_aggregate_source_bytes(monkeypatch):
    group_module = importlib.import_module("ocrllm.validate_image_group")
    sources = tuple(Path(f"{index}.png") for index in range(5))
    bytes_per_source = MAX_AGGREGATE_SOURCE_BYTES // 5 + 1
    monkeypatch.setattr(group_module, "validate_source", lambda _source: bytes_per_source)

    def fail_if_decoded(_source):
        raise AssertionError("decode must not run after the aggregate byte cap fails")

    monkeypatch.setattr(group_module, "decode_image", fail_if_decoded)

    with pytest.raises(InvalidSource) as raised:
        group_module.validate_image_group(sources)

    assert raised.value.code == "SOURCE_TOO_LARGE"


def test_validate_image_group_accepts_exact_aggregate_source_bytes(monkeypatch):
    group_module = importlib.import_module("ocrllm.validate_image_group")
    sources = tuple(Path(f"{index}.png") for index in range(5))
    bytes_per_source = MAX_AGGREGATE_SOURCE_BYTES // len(sources)
    monkeypatch.setattr(group_module, "validate_source", lambda _source: bytes_per_source)
    monkeypatch.setattr(
        group_module,
        "decode_image",
        lambda _source: DecodedImageInfo(format="PNG", width=1, height=1),
    )

    assert len(group_module.validate_image_group(sources)) == len(sources)


def test_validate_image_group_rejects_aggregate_pixels(monkeypatch):
    group_module = importlib.import_module("ocrllm.validate_image_group")
    sources = tuple(Path(f"{index}.png") for index in range(3))
    monkeypatch.setattr(group_module, "validate_source", lambda _source: 1)
    monkeypatch.setattr(
        group_module,
        "decode_image",
        lambda _source: DecodedImageInfo(format="PNG", width=8_000, height=3_000),
    )

    with pytest.raises(InvalidSource) as raised:
        group_module.validate_image_group(sources)

    assert raised.value.code == "SOURCE_TOO_LARGE"


def test_validate_image_group_accepts_the_exact_aggregate_pixel_limit(monkeypatch):
    group_module = importlib.import_module("ocrllm.validate_image_group")
    sources = tuple(Path(f"{index}.png") for index in range(4))
    monkeypatch.setattr(group_module, "validate_source", lambda _source: 1)
    monkeypatch.setattr(
        group_module,
        "decode_image",
        lambda _source: DecodedImageInfo(format="PNG", width=4_000, height=4_000),
    )

    decoded = group_module.validate_image_group(sources)

    assert len(decoded) == 4
    assert sum(image.pixel_count for image in decoded) == MAX_AGGREGATE_PIXELS


class _FakeBombWarning(RuntimeWarning):
    pass


class _FakeBombError(Exception):
    pass


class _FakeImage:
    def __init__(self, *, size, image_format):
        self.size = size
        self.format = image_format

    def __enter__(self):
        return self

    def __exit__(self, _error_type, _error, _traceback):
        return False

    def verify(self):
        return None

    def load(self):
        return None


class _FakeImageModule:
    DecompressionBombWarning = _FakeBombWarning
    DecompressionBombError = _FakeBombError

    def __init__(self, *, size, image_format, warn_about_bomb=False):
        self._size = size
        self._format = image_format
        self._warn_about_bomb = warn_about_bomb

    def open(self, _source):
        if self._warn_about_bomb:
            warnings.warn("test-only decompression bomb", self.DecompressionBombWarning)
        return _FakeImage(size=self._size, image_format=self._format)
