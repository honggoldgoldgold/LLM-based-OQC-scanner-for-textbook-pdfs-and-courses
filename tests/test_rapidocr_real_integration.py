from __future__ import annotations

import importlib.metadata

import pytest

from ocrllm import Config, recognize


rapidocr = pytest.importorskip("rapidocr")
PIL = pytest.importorskip("PIL")
requests = pytest.importorskip("requests")


def _write_text_image(path, text: str) -> None:
    from PIL import Image, ImageDraw, ImageFont

    image = Image.new("RGB", (900, 220), "white")
    drawing = ImageDraw.Draw(image)
    font = ImageFont.load_default(size=64)
    drawing.text((40, 65), text, fill="black", font=font)
    image.save(path)


def test_real_rapidocr_recognizes_ordered_png_and_jpeg_offline(
    tmp_path,
    monkeypatch,
    capsys,
) -> None:
    first = tmp_path / "课程 OCRLLM.png"
    second = tmp_path / "second image.jpg"
    _write_text_image(first, "OCRLLM 2026")
    _write_text_image(second, "BOARD 31415")

    def reject_network(*args, **kwargs):
        raise AssertionError("RapidOCR attempted a network request")

    monkeypatch.setattr(requests.sessions.Session, "request", reject_network)

    result = recognize((first, second), config=Config(image_mode="ocr"))

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""
    assert result.markdown.startswith("## Image 1")
    assert "OCRLLM" in result.markdown
    assert "2026" in result.markdown
    assert "## Image 2" in result.markdown
    assert "BOARD" in result.markdown
    assert "31415" in result.markdown
    assert result.metadata["ocr_engine"] == "rapidocr"
    assert result.metadata["ocr_engine_version"] == importlib.metadata.version(
        "rapidocr"
    )
    assert result.metadata["image_count"] == 2
    assert result.metadata["retained_line_count"] >= 2
    assert result.metadata["provider_call_count"] == 0
    assert result.metadata["network_call_count"] == 0
