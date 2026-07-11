"""Create small valid image fixtures for recognition tests."""

from __future__ import annotations

from pathlib import Path

from PIL import Image


def write_test_image(
    path: Path,
    *,
    color: tuple[int, int, int] = (32, 96, 160),
    size: tuple[int, int] = (8, 6),
) -> Path:
    """Write a decodable PNG or JPEG and return its path."""
    formats = {
        ".png": "PNG",
        ".jpg": "JPEG",
        ".jpeg": "JPEG",
    }
    image_format = formats[path.suffix.lower()]
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", size, color=color).save(path, format=image_format)
    return path
