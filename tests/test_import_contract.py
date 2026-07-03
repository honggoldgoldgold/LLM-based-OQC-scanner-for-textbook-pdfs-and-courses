from pathlib import Path

from ocrllm import Config, RecognitionResult, recognize, recognize_batch
from ocrllm.errors import ConfigError, UnsupportedFormat


class FakeProvider:
    def recognize_images(self, image_paths, *, prompt, config):
        names = ", ".join(path.name for path in image_paths)
        return f"# Board\n\nImages: {names}\n"


def test_import_contract_recognizes_board_without_writing(tmp_path):
    source = tmp_path / "board.png"
    source.write_bytes(b"not a real image; provider is faked")

    result = recognize(source, config=Config(provider=FakeProvider()))

    assert isinstance(result, RecognitionResult)
    assert result.source_type == "board"
    assert result.output_path is None
    assert "board.png" in result.markdown


def test_import_contract_writes_when_output_dir_is_set(tmp_path):
    source = tmp_path / "board.jpg"
    source.write_bytes(b"fake")
    out_dir = tmp_path / "out"

    result = recognize(source, config=Config(provider=FakeProvider(), output_dir=out_dir))

    assert result.output_path == out_dir / "board_board.md"
    assert result.output_path.read_text(encoding="utf-8") == result.markdown


def test_batch_returns_one_result_per_source(tmp_path):
    first = tmp_path / "a.png"
    second = tmp_path / "b.png"
    first.write_bytes(b"fake")
    second.write_bytes(b"fake")

    results = recognize_batch([first, second], config=Config(provider=FakeProvider()))

    assert [result.source_type for result in results] == ["board", "board"]


def test_provider_is_required_for_board(tmp_path):
    source = tmp_path / "board.png"
    source.write_bytes(b"fake")

    try:
        recognize(source)
    except ConfigError as exc:
        assert "Config.provider" in str(exc)
    else:
        raise AssertionError("ConfigError was not raised")


def test_unsupported_extension_is_explicit(tmp_path):
    source = tmp_path / "lecture.pdf"
    source.write_bytes(b"fake")

    try:
        recognize(source, config=Config(provider=FakeProvider()))
    except UnsupportedFormat as exc:
        assert ".pdf" in str(exc)
    else:
        raise AssertionError("UnsupportedFormat was not raised")
