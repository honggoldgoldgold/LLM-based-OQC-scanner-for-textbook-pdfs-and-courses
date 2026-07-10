"""Black-box proof that invalid images never spend a provider call."""

from __future__ import annotations

import traceback
from pathlib import Path

import pytest

from ocrllm import Config, InvalidSource, UnsupportedFormat, recognize
from ocrllm.validate_source import MAX_SOURCE_BYTES
from write_test_image import write_test_image


class CountingProvider:
    def __init__(self) -> None:
        self.calls = 0

    def recognize_images(self, image_paths, *, prompt, config):
        self.calls += 1
        return "# Unexpected provider call\n"


@pytest.mark.parametrize(
    ("filename", "contents", "expected_error", "expected_code"),
    [
        ("empty.png", b"", InvalidSource, "SOURCE_INVALID"),
        ("corrupt.png", b"not an image", InvalidSource, "SOURCE_INVALID"),
        ("unsupported.webp", b"not inspected", UnsupportedFormat, "UNSUPPORTED_FORMAT"),
    ],
)
def test_invalid_source_content_fails_before_provider(
    tmp_path,
    filename,
    contents,
    expected_error,
    expected_code,
):
    source = tmp_path / filename
    source.write_bytes(contents)
    provider = CountingProvider()

    with pytest.raises(expected_error) as captured:
        recognize(source, config=Config(provider=provider))

    assert captured.value.code == expected_code
    assert provider.calls == 0


def test_missing_source_fails_before_provider(tmp_path):
    provider = CountingProvider()
    path_sentinel = "MISSING_SOURCE_PATH_SECRET_475a"

    with pytest.raises(InvalidSource) as captured:
        recognize(
            tmp_path / f"{path_sentinel}.png",
            config=Config(provider=provider),
        )

    assert captured.value.code == "SOURCE_NOT_FOUND"
    assert provider.calls == 0
    rendered = "".join(
        traceback.format_exception(
            type(captured.value),
            captured.value,
            captured.value.__traceback__,
        )
    )
    assert path_sentinel not in rendered
    assert captured.value.__cause__ is None
    assert captured.value.__context__ is None


def test_unreadable_source_fails_before_provider(tmp_path, monkeypatch):
    source = write_test_image(tmp_path / "unreadable.png")
    provider = CountingProvider()
    original_open = Path.open

    def deny_source_open(path, *args, **kwargs):
        if path == source:
            raise PermissionError("test-only source denial")
        return original_open(path, *args, **kwargs)

    monkeypatch.setattr(Path, "open", deny_source_open)

    with pytest.raises(InvalidSource) as captured:
        recognize(source, config=Config(provider=provider))

    assert captured.value.code == "SOURCE_UNREADABLE"
    assert provider.calls == 0


def test_oversized_source_fails_before_provider(tmp_path):
    source = tmp_path / "oversized.png"
    with source.open("wb") as stream:
        stream.write(b"x")
        stream.truncate(MAX_SOURCE_BYTES + 1)
    provider = CountingProvider()

    with pytest.raises(InvalidSource) as captured:
        recognize(source, config=Config(provider=provider))

    assert captured.value.code == "SOURCE_TOO_LARGE"
    assert provider.calls == 0


def test_invalid_later_group_member_fails_before_provider(tmp_path):
    valid = write_test_image(tmp_path / "valid.png")
    invalid = tmp_path / "invalid.jpg"
    invalid.write_bytes(b"not a JPEG")
    provider = CountingProvider()

    with pytest.raises(InvalidSource) as captured:
        recognize((valid, invalid), config=Config(provider=provider))

    assert captured.value.code == "SOURCE_INVALID"
    assert provider.calls == 0


def test_too_many_images_fail_before_file_or_provider_access(tmp_path):
    sources = tuple(tmp_path / f"missing-{index}.png" for index in range(11))
    provider = CountingProvider()

    with pytest.raises(InvalidSource) as captured:
        recognize(sources, config=Config(provider=provider))

    assert captured.value.code == "SOURCE_TOO_LARGE"
    assert provider.calls == 0
