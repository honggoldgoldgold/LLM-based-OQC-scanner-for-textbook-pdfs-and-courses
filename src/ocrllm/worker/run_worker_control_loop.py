"""Run the protocol loop independently of recognition process ownership."""

from __future__ import annotations

from collections.abc import Callable
from threading import Lock
from typing import BinaryIO

from ocrllm.contracts.cancel_command import CancelCommand
from ocrllm.contracts.capabilities_command import CapabilitiesCommand
from ocrllm.contracts.capabilities_event import CapabilitiesEvent
from ocrllm.contracts.image_recognition_request import ImageRecognitionRequest
from ocrllm.contracts.worker_event import WorkerEvent
from ocrllm.errors import OCRLLMError
from ocrllm.get_capabilities import get_capabilities

from .build_worker_error_event import build_worker_error_event
from .read_jsonl_command import read_jsonl_command
from .worker_job_manager import WorkerJobManager
from .write_jsonl_event import write_jsonl_event


def run_worker_control_loop(
    *,
    input_stream: BinaryIO,
    output_stream: BinaryIO,
    job_manager: WorkerJobManager,
    capability_getter: Callable[[], tuple] = get_capabilities,
    internal_error_reporter: Callable[[BaseException], None] | None = None,
) -> None:
    """Read commands until EOF while a nonblocking manager owns job state."""

    output_lock = Lock()

    def emit(event: WorkerEvent) -> None:
        with output_lock:
            write_jsonl_event(event, stream=output_stream)

    try:
        while True:
            try:
                command = read_jsonl_command(input_stream)
            except OCRLLMError as error:
                emit(build_worker_error_event(error))
                continue
            if command is None:
                return

            try:
                if type(command) is CapabilitiesCommand:
                    emit(
                        CapabilitiesEvent(
                            request_id=command.request_id,
                            capabilities=capability_getter(),
                        )
                    )
                elif type(command) is ImageRecognitionRequest:
                    job_manager.start(command, emit=emit)
                elif type(command) is CancelCommand:
                    job_manager.cancel(command, emit=emit)
                else:
                    raise AssertionError("parsed command union is incomplete")
            except OCRLLMError as error:
                if "request_id" not in error.details:
                    error._add_safe_detail("request_id", command.request_id)
                emit(build_worker_error_event(error))
            except Exception as error:
                if internal_error_reporter is not None:
                    internal_error_reporter(error)
                emit(
                    build_worker_error_event(
                        OCRLLMError(
                            "Worker job management failed.",
                            code="WORKER_INTERNAL",
                            details={"request_id": command.request_id},
                        )
                    )
                )
    finally:
        job_manager.close()
