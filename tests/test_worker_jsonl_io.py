from __future__ import annotations

import io
import json
from pathlib import Path

import pytest

from ocrllm.contracts import (
    AcceptedEvent,
    CapabilitiesCommand,
    ErrorEvent,
    ImageRecognitionRequest,
    ResultEvent,
    WorkerRecognitionResult,
    parse_worker_command,
)
from ocrllm.errors import OCRLLMError
from ocrllm.worker import (
    MAX_JSONL_COMMAND_BYTES,
    build_worker_error_event,
    read_jsonl_command,
    write_jsonl_event,
)


COMMAND_FIXTURE = (
    Path(__file__).parent / "fixtures" / "worker" / "v1alpha1_commands.jsonl"
)
REQUEST_ID = "22222222-2222-4222-8222-222222222222"


class FlushTrackingBytesIO(io.BytesIO):
    def __init__(self) -> None:
        super().__init__()
        self.flush_count = 0

    def flush(self) -> None:
        self.flush_count += 1
        super().flush()


class PartialWriteBytesIO(FlushTrackingBytesIO):
    def write(self, value: bytes) -> int:
        return super().write(value[:7])


class RejectingBytesIO(FlushTrackingBytesIO):
    def write(self, value: bytes) -> int:
        return 0


def _fixture_bytes() -> bytes:
    return COMMAND_FIXTURE.read_bytes()


def _valid_recognize_line() -> bytes:
    return _fixture_bytes().splitlines(keepends=True)[1]


def test_reader_returns_each_command_then_none_at_clean_eof() -> None:
    stream = io.BytesIO(_fixture_bytes())

    first = read_jsonl_command(stream)
    second = read_jsonl_command(stream)
    third = read_jsonl_command(stream)
    fourth = read_jsonl_command(stream)

    assert isinstance(first, CapabilitiesCommand)
    assert isinstance(second, ImageRecognitionRequest)
    assert third.command == "cancel"
    assert fourth is None


def test_reader_accepts_exact_byte_limit_with_json_whitespace_padding() -> None:
    base = _valid_recognize_line().rstrip(b"\r\n")
    padding = b" " * (MAX_JSONL_COMMAND_BYTES - len(base) - 1)
    stream = io.BytesIO(base + padding + b"\n")

    command = read_jsonl_command(stream)

    assert isinstance(command, ImageRecognitionRequest)
    assert stream.read() == b""


def test_reader_rejects_and_drains_oversized_record_before_next_command() -> None:
    oversized = b"{" + b"x" * MAX_JSONL_COMMAND_BYTES + b"}\n"
    stream = io.BytesIO(oversized + _valid_recognize_line())

    with pytest.raises(OCRLLMError) as caught:
        read_jsonl_command(stream)
    recovered = read_jsonl_command(stream)

    assert caught.value.code == "COMMAND_INVALID"
    assert isinstance(recovered, ImageRecognitionRequest)


@pytest.mark.parametrize(
    "payload",
    [
        b"{}",
        b"\xff\n",
        b"\n",
    ],
)
def test_reader_rejects_incomplete_invalid_utf8_and_empty_records(
    payload: bytes,
) -> None:
    with pytest.raises(OCRLLMError) as caught:
        read_jsonl_command(io.BytesIO(payload))
    assert caught.value.code == "COMMAND_INVALID"


def test_writer_emits_one_compact_utf8_record_and_flushes() -> None:
    event = ResultEvent(
        request_id=REQUEST_ID,
        result=WorkerRecognitionResult(
            markdown="# 识别\n\n第二行\n",
            source_type="image",
            profile="board",
        ),
    )
    stream = FlushTrackingBytesIO()

    write_jsonl_event(event, stream=stream)

    payload = stream.getvalue()
    assert payload.endswith(b"\n")
    assert b"\n" not in payload[:-1]
    assert "识别" in payload.decode("utf-8")
    assert json.loads(payload)["result"]["markdown"] == "# 识别\n\n第二行\n"
    assert stream.flush_count == 1


def test_writer_completes_partial_binary_writes_before_flushing() -> None:
    stream = PartialWriteBytesIO()

    write_jsonl_event(AcceptedEvent(request_id=REQUEST_ID), stream=stream)

    assert json.loads(stream.getvalue())["event"] == "accepted"
    assert stream.flush_count == 1


def test_writer_fails_when_stream_makes_no_progress() -> None:
    stream = RejectingBytesIO()

    with pytest.raises(OSError, match="did not accept"):
        write_jsonl_event(AcceptedEvent(request_id=REQUEST_ID), stream=stream)
    assert stream.flush_count == 0


@pytest.mark.parametrize(
    "raw",
    [
        {
            "protocol_version": "ocrllm.v9",
            "command": "capabilities",
            "request_id": REQUEST_ID,
        },
        {
            "protocol_version": "ocrllm.v1alpha1",
            "command": "capabilities",
            "request_id": REQUEST_ID,
            "extra": True,
        },
        {
            "protocol_version": "ocrllm.v1alpha1",
            "command": "recognize",
            "request_id": REQUEST_ID,
            "sources": [],
            "provider": "dashscope",
            "model": None,
            "input_languages": [],
            "output_language": None,
            "profile": "board",
            "options": {"unknown": True},
        },
    ],
)
def test_typed_parser_errors_recover_valid_request_id(raw: dict[str, object]) -> None:
    with pytest.raises(OCRLLMError) as caught:
        parse_worker_command(raw)

    event = build_worker_error_event(caught.value)

    assert event.request_id == REQUEST_ID
    assert "request_id" not in event.details


def test_error_builder_uses_null_when_no_canonical_request_id_exists() -> None:
    error = OCRLLMError(
        "Worker command is invalid.",
        code="COMMAND_INVALID",
        details={"request_id": "not-a-uuid"},
    )

    event = build_worker_error_event(error)

    assert event.request_id is None
    assert event.details == {}


def test_error_builder_preserves_redaction_and_retryability() -> None:
    error = OCRLLMError(
        "Provider timed out.",
        code="PROVIDER_TIMEOUT",
        retryable=True,
        details={"authorization": "secret-sentinel", "attempt": 1},
    )

    event = build_worker_error_event(error)
    stream = FlushTrackingBytesIO()
    write_jsonl_event(event, stream=stream)
    encoded = stream.getvalue().decode("utf-8")

    assert isinstance(event, ErrorEvent)
    assert event.retryable is True
    assert "secret-sentinel" not in encoded
    assert "[REDACTED]" in encoded
    assert json.loads(encoded)["details"]["attempt"] == 1


def test_error_builder_rejects_non_library_exception() -> None:
    with pytest.raises(TypeError, match="OCRLLMError"):
        build_worker_error_event(ValueError("secret-sentinel"))  # type: ignore[arg-type]
