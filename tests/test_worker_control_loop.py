from __future__ import annotations

import io
import json
import threading
import time
from collections.abc import Callable

from ocrllm.contracts import (
    AcceptedEvent,
    CancelCommand,
    ErrorEvent,
    ImageRecognitionRequest,
    ProgressEvent,
    WorkerEvent,
)
from ocrllm.errors import OCRLLMError
from ocrllm.worker import run_worker_control_loop


FIRST_ID = "11111111-1111-4111-8111-111111111111"
ACTIVE_ID = "22222222-2222-4222-8222-222222222222"
OTHER_ID = "33333333-3333-4333-8333-333333333333"


def _line(value: dict[str, object]) -> bytes:
    return (json.dumps(value, separators=(",", ":")) + "\n").encode()


def _capabilities(request_id: str = FIRST_ID) -> dict[str, object]:
    return {
        "protocol_version": "ocrllm.v1alpha1",
        "command": "capabilities",
        "request_id": request_id,
    }


def _recognize(request_id: str) -> dict[str, object]:
    return {
        "protocol_version": "ocrllm.v1alpha1",
        "command": "recognize",
        "request_id": request_id,
        "sources": [{"media_type": "image", "uri": "file:///C:/Course/board.png"}],
        "provider": "dashscope",
        "model": None,
        "input_languages": [],
        "output_language": None,
        "profile": "board",
        "options": {},
    }


def _cancel(request_id: str) -> dict[str, object]:
    return {
        "protocol_version": "ocrllm.v1alpha1",
        "command": "cancel",
        "request_id": request_id,
    }


class DeterministicJobManager:
    def __init__(self) -> None:
        self.active_request_id: str | None = None
        self.closed = 0

    def start(
        self,
        command: ImageRecognitionRequest,
        *,
        emit: Callable[[WorkerEvent], None],
    ) -> None:
        if self.active_request_id is not None:
            raise OCRLLMError("Worker already has an active job.", code="WORKER_BUSY")
        self.active_request_id = command.request_id
        emit(AcceptedEvent(request_id=command.request_id))

    def cancel(
        self,
        command: CancelCommand,
        *,
        emit: Callable[[WorkerEvent], None],
    ) -> None:
        if self.active_request_id != command.request_id:
            raise OCRLLMError(
                "The requested worker job is not active.",
                code="REQUEST_NOT_ACTIVE",
            )
        self.active_request_id = None
        emit(
            ErrorEvent(
                request_id=command.request_id,
                code="CANCELLED",
                message="Recognition was cancelled.",
                retryable=False,
            )
        )

    def close(self) -> None:
        self.closed += 1
        self.active_request_id = None


def _decode_lines(stream: io.BytesIO) -> list[dict[str, object]]:
    return [json.loads(line) for line in stream.getvalue().splitlines()]


def test_control_loop_handles_errors_capabilities_job_state_and_eof() -> None:
    input_stream = io.BytesIO(
        b"not-json\n"
        + _line(_capabilities())
        + _line(_recognize(ACTIVE_ID))
        + _line(_recognize(OTHER_ID))
        + _line(_cancel(OTHER_ID))
        + _line(_cancel(ACTIVE_ID))
    )
    output_stream = io.BytesIO()
    manager = DeterministicJobManager()

    run_worker_control_loop(
        input_stream=input_stream,
        output_stream=output_stream,
        job_manager=manager,
    )

    events = _decode_lines(output_stream)
    assert [event["event"] for event in events] == [
        "error",
        "capabilities",
        "accepted",
        "error",
        "error",
        "error",
    ]
    assert events[0]["code"] == "COMMAND_INVALID"
    assert events[0]["request_id"] is None
    assert len(events[1]["capabilities"]) == 20
    assert events[2]["request_id"] == ACTIVE_ID
    assert events[3]["code"] == "WORKER_BUSY"
    assert events[3]["request_id"] == OTHER_ID
    assert events[4]["code"] == "REQUEST_NOT_ACTIVE"
    assert events[4]["request_id"] == OTHER_ID
    assert events[5]["code"] == "CANCELLED"
    assert events[5]["request_id"] == ACTIVE_ID
    assert manager.closed == 1


class CrashingJobManager(DeterministicJobManager):
    def start(
        self,
        command: ImageRecognitionRequest,
        *,
        emit: Callable[[WorkerEvent], None],
    ) -> None:
        raise RuntimeError("secret-sentinel")


def test_unexpected_manager_failure_is_reported_off_protocol_and_redacted_on_stdout() -> (
    None
):
    output_stream = io.BytesIO()
    manager = CrashingJobManager()
    reported: list[BaseException] = []

    run_worker_control_loop(
        input_stream=io.BytesIO(_line(_recognize(ACTIVE_ID))),
        output_stream=output_stream,
        job_manager=manager,
        internal_error_reporter=reported.append,
    )

    events = _decode_lines(output_stream)
    assert len(events) == 1
    assert events[0]["code"] == "WORKER_INTERNAL"
    assert events[0]["request_id"] == ACTIVE_ID
    assert "secret-sentinel" not in output_stream.getvalue().decode()
    assert len(reported) == 1
    assert "secret-sentinel" in str(reported[0])
    assert manager.closed == 1


class YieldingPartialBytesIO(io.BytesIO):
    def write(self, value: bytes) -> int:
        time.sleep(0)
        return super().write(value[:3])


class ConcurrentEmitterManager(DeterministicJobManager):
    def __init__(self) -> None:
        super().__init__()
        self.thread: threading.Thread | None = None

    def start(
        self,
        command: ImageRecognitionRequest,
        *,
        emit: Callable[[WorkerEvent], None],
    ) -> None:
        self.active_request_id = command.request_id

        def emit_progress() -> None:
            for completed in range(10):
                emit(
                    ProgressEvent(
                        request_id=command.request_id,
                        stage="recognition",
                        completed=completed,
                        total=10,
                        unit="step",
                    )
                )

        self.thread = threading.Thread(target=emit_progress)
        self.thread.start()

    def close(self) -> None:
        if self.thread is not None:
            self.thread.join(timeout=5)
            assert not self.thread.is_alive()
        super().close()


def test_control_loop_serializes_concurrent_events_without_line_interleaving() -> None:
    commands = _line(_recognize(ACTIVE_ID)) + b"".join(
        _line(_capabilities(f"{index:08d}-1111-4111-8111-111111111111"))
        for index in range(10, 20)
    )
    output_stream = YieldingPartialBytesIO()

    run_worker_control_loop(
        input_stream=io.BytesIO(commands),
        output_stream=output_stream,
        job_manager=ConcurrentEmitterManager(),
    )

    events = _decode_lines(output_stream)
    assert len(events) == 20
    assert sum(event["event"] == "progress" for event in events) == 10
    assert sum(event["event"] == "capabilities" for event in events) == 10


class CloseTrackingManager(DeterministicJobManager):
    def close(self) -> None:
        super().close()
        raise RuntimeError("close failure")


def test_close_failure_propagates_after_clean_eof() -> None:
    manager = CloseTrackingManager()

    try:
        run_worker_control_loop(
            input_stream=io.BytesIO(),
            output_stream=io.BytesIO(),
            job_manager=manager,
        )
    except RuntimeError as error:
        assert str(error) == "close failure"
    else:
        raise AssertionError("close failure was hidden")
    assert manager.closed == 1
