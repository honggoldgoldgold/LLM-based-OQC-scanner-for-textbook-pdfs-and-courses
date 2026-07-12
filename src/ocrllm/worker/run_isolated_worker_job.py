"""Run one recognition callable inside the isolated child process."""

from __future__ import annotations

import os
import json
import sys
from multiprocessing.connection import Connection
from multiprocessing.synchronize import Event

from ocrllm.contracts.error_event import ErrorEvent
from ocrllm.contracts.image_recognition_request import ImageRecognitionRequest
from ocrllm.contracts.parse_worker_command import parse_worker_command
from ocrllm.contracts.progress_event import ProgressEvent
from ocrllm.contracts.result_event import ResultEvent
from ocrllm.contracts.warning_event import WarningEvent
from ocrllm.contracts.worker_event import WorkerEvent
from ocrllm.contracts.serialize_worker_event import serialize_worker_event
from ocrllm.errors import OCRLLMError

from .build_worker_error_event import build_worker_error_event
from .worker_job_callable import WorkerJobCallable


_CHILD_EVENT_TYPES = (ProgressEvent, WarningEvent, ResultEvent, ErrorEvent)


def run_isolated_worker_job(
    command_value: dict[str, object],
    send_connection: Connection,
    start_gate: Event,
    ready_gate: Event,
    job_callable: WorkerJobCallable,
) -> None:
    """Wait for parent acceptance, run one job, and send one terminal event."""

    _start_posix_process_group()
    ready_gate.set()
    parsed_command = parse_worker_command(command_value)
    if type(parsed_command) is not ImageRecognitionRequest:
        raise TypeError("isolated job command must be recognize")
    command = parsed_command
    terminal_sent = False

    def emit(event: WorkerEvent) -> None:
        nonlocal terminal_sent
        if type(event) not in _CHILD_EVENT_TYPES:
            raise TypeError("isolated job emitted an unsupported event type")
        if event.request_id != command.request_id:
            raise ValueError("isolated job emitted a mismatched request_id")
        if terminal_sent:
            raise RuntimeError("isolated job emitted after its terminal event")
        payload = json.dumps(
            serialize_worker_event(event),
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
        ).encode("utf-8")
        send_connection.send_bytes(payload)
        if type(event) in {ResultEvent, ErrorEvent}:
            terminal_sent = True

    try:
        start_gate.wait()
        job_callable(command, emit)
        if not terminal_sent:
            raise RuntimeError("isolated job returned without a terminal event")
    except OCRLLMError as error:
        if not terminal_sent:
            error._add_safe_detail("request_id", command.request_id)
            emit(build_worker_error_event(error))
    except BaseException as error:
        _report_internal_error_type(error)
        if not terminal_sent:
            emit(
                ErrorEvent(
                    request_id=command.request_id,
                    code="WORKER_INTERNAL",
                    message="Isolated recognition job failed.",
                    retryable=False,
                )
            )
    finally:
        send_connection.close()


def _start_posix_process_group() -> None:
    if os.name != "nt":
        os.setsid()


def _report_internal_error_type(error: BaseException) -> None:
    error_type = f"{type(error).__module__}.{type(error).__qualname__}"
    print(
        f"isolated worker job internal error type: {error_type}",
        file=sys.stderr,
        flush=True,
    )
