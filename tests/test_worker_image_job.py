from __future__ import annotations

import importlib
import os
from pathlib import Path

import pytest

from ocrllm import Config, RecognitionResult
from ocrllm.contracts import (
    ImageRecognitionRequest,
    ProgressEvent,
    ResultEvent,
    SourceDescriptor,
    WorkerEvent,
)
from ocrllm.errors import ConfigError, ProviderError
from ocrllm.providers.dashscope.resolve_dashscope_model import DEFAULT_DASHSCOPE_MODEL
from ocrllm.worker import (
    build_worker_image_config,
    file_uri_to_path,
    run_image_recognition_job,
)


REQUEST_ID = "22222222-2222-4222-8222-222222222222"


def _command(
    sources: tuple[Path, ...],
    *,
    output_dir: Path | None = None,
    overwrite: bool = False,
    timeout_seconds: int | float = 120,
    model: str | None = None,
) -> ImageRecognitionRequest:
    return ImageRecognitionRequest(
        request_id=REQUEST_ID,
        sources=tuple(
            SourceDescriptor(media_type="image", uri=source.resolve().as_uri())
            for source in sources
        ),
        provider="dashscope",
        model=model,
        input_languages=("zh-Hans", "en"),
        output_language="zh-Hans",
        options={
            "output_directory_uri": (
                None if output_dir is None else output_dir.resolve().as_uri()
            ),
            "overwrite": overwrite,
            "timeout_seconds": timeout_seconds,
        },
    )


def test_file_uri_round_trips_unicode_space_and_emoji_path(tmp_path) -> None:
    path = (tmp_path / "课程 📚" / "board image.png").resolve()

    decoded = file_uri_to_path(path.as_uri())

    assert decoded == path


def test_file_uri_round_trips_literal_percent_escape_text(tmp_path) -> None:
    path = (tmp_path / "literal%20name.png").resolve()

    decoded = file_uri_to_path(path.as_uri())

    assert decoded == path


@pytest.mark.parametrize(
    "uri",
    [
        "https://example.test/a.png",
        "file:///C:/folder%2Fescape.png",
        "file:///C:/folder%5Cescape.png",
        "file:///C:/folder/a.png?query=1",
        "file://user:password@server/share/a.png",
        "file://server:bad/share/a.png",
        "file:///C:/folder/%FF.png",
    ],
)
def test_file_uri_conversion_rejects_ambiguous_or_nonlocal_values(uri: str) -> None:
    with pytest.raises(ConfigError, match="unambiguous absolute local path"):
        file_uri_to_path(uri)


def test_worker_config_is_exact_beijing_v17_and_credential_free(
    tmp_path,
    monkeypatch,
) -> None:
    source = tmp_path / "board.png"
    output_dir = tmp_path / "输出"
    command = _command(
        (source,),
        output_dir=output_dir,
        overwrite=True,
        timeout_seconds=33.5,
        model=DEFAULT_DASHSCOPE_MODEL,
    )
    monkeypatch.setenv("DASHSCOPE_API_KEY", "secret-sentinel")

    config = build_worker_image_config(command)

    assert type(config) is Config
    assert config.provider == "dashscope"
    assert config.api_key is None
    assert config.model == DEFAULT_DASHSCOPE_MODEL
    assert config.profile == "board"
    assert config.input_languages == ("zh-Hans", "en")
    assert config.output_language == "zh-Hans"
    assert config.output_dir == output_dir.resolve()
    assert config.overwrite is True
    assert config.timeout_seconds == 33.5
    assert config.dashscope is not None
    assert config.dashscope.region == "cn-beijing"
    assert (
        config.dashscope.base_url == "https://dashscope.aliyuncs.com/compatible-mode/v1"
    )
    assert config.dashscope.enable_thinking is True
    assert config.dashscope.vl_high_resolution_images is True
    assert config.dashscope.standalone_sign_scout_model == DEFAULT_DASHSCOPE_MODEL
    assert "secret-sentinel" not in repr(config)


def test_image_job_reuses_public_facade_preserves_order_and_emits_result(
    tmp_path,
    monkeypatch,
) -> None:
    first = tmp_path / "第一张.png"
    second = tmp_path / "second image.jpg"
    first.write_bytes(b"first")
    second.write_bytes(b"second")
    command = _command((first, second))
    captured: dict[str, object] = {}

    def fake_recognize(source, *, config):
        captured["source"] = source
        captured["config"] = config
        return RecognitionResult(
            markdown="# Unified board result\n",
            source_type="image",
            profile="board",
            metadata={"provider": "dashscope", "restored_signs": 1},
        )

    job_module = importlib.import_module("ocrllm.worker.run_image_recognition_job")
    monkeypatch.setattr(job_module, "recognize", fake_recognize)
    events: list[WorkerEvent] = []

    run_image_recognition_job(command, events.append)

    assert captured["source"] == (first.resolve(), second.resolve())
    config = captured["config"]
    assert isinstance(config, Config)
    assert config.api_key is None
    assert [event.event for event in events] == ["progress", "progress", "result"]
    assert isinstance(events[0], ProgressEvent)
    assert (events[0].completed, events[0].total) == (0, 2)
    assert isinstance(events[1], ProgressEvent)
    assert (events[1].completed, events[1].total) == (2, 2)
    assert isinstance(events[2], ResultEvent)
    assert events[2].result.markdown == "# Unified board result\n"
    assert events[2].result.metadata["restored_signs"] == 1


def test_image_job_maps_existing_output_to_file_uri(tmp_path, monkeypatch) -> None:
    source = tmp_path / "board.png"
    source.write_bytes(b"source")
    output = tmp_path / "out" / "board_board.md"
    output.parent.mkdir()
    output.write_text("# Board\n", encoding="utf-8")
    command = _command((source,), output_dir=output.parent)

    def fake_recognize(source, *, config):
        return RecognitionResult(
            markdown="# Board\n",
            source_type="image",
            profile="board",
            output_path=output,
        )

    job_module = importlib.import_module("ocrllm.worker.run_image_recognition_job")
    monkeypatch.setattr(job_module, "recognize", fake_recognize)
    events: list[WorkerEvent] = []

    run_image_recognition_job(command, events.append)

    result = events[-1]
    assert isinstance(result, ResultEvent)
    assert result.result.output_uri == output.resolve().as_uri()


def test_image_job_propagates_typed_facade_error_for_child_wrapper(
    tmp_path,
    monkeypatch,
) -> None:
    source = tmp_path / "board.png"
    source.write_bytes(b"source")
    command = _command((source,))

    def fake_recognize(source, *, config):
        raise ProviderError(
            "Provider timed out.",
            code="PROVIDER_TIMEOUT",
            retryable=True,
            details={"authorization": "secret-sentinel"},
        )

    job_module = importlib.import_module("ocrllm.worker.run_image_recognition_job")
    monkeypatch.setattr(job_module, "recognize", fake_recognize)
    events: list[WorkerEvent] = []

    with pytest.raises(ProviderError) as caught:
        run_image_recognition_job(command, events.append)

    assert caught.value.code == "PROVIDER_TIMEOUT"
    assert "secret-sentinel" not in repr(caught.value.details)
    assert len(events) == 1
    assert isinstance(events[0], ProgressEvent)


def test_worker_image_module_does_not_read_credential_during_config_build(
    tmp_path,
    monkeypatch,
) -> None:
    source = tmp_path / "board.png"
    monkeypatch.delenv("DASHSCOPE_API_KEY", raising=False)
    command = _command((source,))

    config = build_worker_image_config(command)

    assert config.api_key is None
    assert "DASHSCOPE_API_KEY" not in os.environ
