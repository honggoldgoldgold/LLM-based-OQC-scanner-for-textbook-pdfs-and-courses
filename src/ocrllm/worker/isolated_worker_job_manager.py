"""Own one spawned recognition child and relay its typed events."""

from __future__ import annotations

import multiprocessing
import json
import time
from collections.abc import Callable
from dataclasses import dataclass
from multiprocessing.connection import Connection
from multiprocessing.context import BaseContext
from multiprocessing.process import BaseProcess
from multiprocessing.synchronize import Event
from threading import Event as ThreadEvent
from threading import Lock, Thread

from ocrllm.contracts.accepted_event import AcceptedEvent
from ocrllm.contracts.cancel_command import CancelCommand
from ocrllm.contracts.error_event import ErrorEvent
from ocrllm.contracts.image_recognition_request import ImageRecognitionRequest
from ocrllm.contracts.progress_event import ProgressEvent
from ocrllm.contracts.parse_worker_event import parse_worker_event
from ocrllm.contracts.result_event import ResultEvent
from ocrllm.contracts.warning_event import WarningEvent
from ocrllm.contracts.serialize_worker_command import serialize_worker_command
from ocrllm.contracts.worker_event import WorkerEvent
from ocrllm.errors import OCRLLMError

from .run_isolated_worker_job import run_isolated_worker_job
from .terminate_process_tree import terminate_process_tree
from .worker_job_callable import WorkerJobCallable


_RELAYED_EVENT_TYPES = (ProgressEvent, WarningEvent, ResultEvent, ErrorEvent)
MAX_CHILD_EVENT_BYTES = 67_108_864


@dataclass(slots=True)
class _ActiveJob:
    request_id: str
    process: BaseProcess
    receive_connection: Connection
    start_gate: Event
    cancelled: ThreadEvent
    relay_thread: Thread | None = None


class IsolatedWorkerJobManager:
    """Start at most one spawned job and keep control-loop calls nonblocking."""

    def __init__(
        self,
        job_callable: WorkerJobCallable,
        *,
        context: BaseContext | None = None,
        internal_error_reporter: Callable[[BaseException], None] | None = None,
    ) -> None:
        if not callable(job_callable):
            raise TypeError("job_callable must be callable")
        self._job_callable = job_callable
        self._context = (
            multiprocessing.get_context("spawn") if context is None else context
        )
        self._internal_error_reporter = internal_error_reporter
        self._state_lock = Lock()
        self._active: _ActiveJob | None = None

    @property
    def active_request_id(self) -> str | None:
        """Return the active request identity without exposing process handles."""

        with self._state_lock:
            return None if self._active is None else self._active.request_id

    def start(
        self,
        command: ImageRecognitionRequest,
        *,
        emit: Callable[[WorkerEvent], None],
    ) -> None:
        """Spawn one gated child, emit acceptance, then release it to work."""

        if type(command) is not ImageRecognitionRequest:
            raise TypeError("command must be an exact ImageRecognitionRequest")
        with self._state_lock:
            if self._active is not None:
                raise OCRLLMError(
                    "Worker already has an active recognition job.",
                    code="WORKER_BUSY",
                )
            receive_connection, send_connection = self._context.Pipe(duplex=False)
            start_gate = self._context.Event()
            ready_gate = self._context.Event()
            process = self._context.Process(
                target=run_isolated_worker_job,
                args=(
                    serialize_worker_command(command),
                    send_connection,
                    start_gate,
                    ready_gate,
                    self._job_callable,
                ),
                name=f"ocrllm-job-{command.request_id}",
                daemon=False,
            )
            try:
                process.start()
            except BaseException:
                receive_connection.close()
                send_connection.close()
                raise
            send_connection.close()
            if not ready_gate.wait(timeout=5.0):
                terminate_process_tree(process)
                receive_connection.close()
                raise OCRLLMError(
                    "The isolated worker process did not become ready in time.",
                    code="WORKER_INTERNAL",
                )
            active = _ActiveJob(
                request_id=command.request_id,
                process=process,
                receive_connection=receive_connection,
                start_gate=start_gate,
                cancelled=ThreadEvent(),
            )
            relay_thread = Thread(
                target=self._relay_events,
                args=(active, emit),
                name=f"ocrllm-relay-{command.request_id}",
                daemon=True,
            )
            active.relay_thread = relay_thread
            self._active = active
            relay_thread.start()

        try:
            emit(AcceptedEvent(request_id=command.request_id))
        except BaseException:
            active.cancelled.set()
            terminate_process_tree(active.process)
            active.start_gate.set()
            self._join_relay(active, timeout_seconds=5.0)
            self._clear_active(active)
            raise
        active.start_gate.set()

    def cancel(
        self,
        command: CancelCommand,
        *,
        emit: Callable[[WorkerEvent], None],
    ) -> None:
        """Terminate only the matching active process tree and emit CANCELLED."""

        if type(command) is not CancelCommand:
            raise TypeError("command must be an exact CancelCommand")
        with self._state_lock:
            active = self._active
            if active is None or active.request_id != command.request_id:
                raise OCRLLMError(
                    "The requested worker job is not active.",
                    code="REQUEST_NOT_ACTIVE",
                )
            active.cancelled.set()

        deadline = time.monotonic() + 5.0
        terminate_process_tree(active.process, timeout_seconds=_remaining(deadline))
        self._join_relay(active, timeout_seconds=_remaining(deadline))
        self._clear_active(active)
        emit(
            ErrorEvent(
                request_id=command.request_id,
                code="CANCELLED",
                message="Recognition was cancelled.",
                retryable=False,
            )
        )

    def close(self) -> None:
        """Terminate an active child tree without emitting after control EOF."""

        with self._state_lock:
            active = self._active
            if active is None:
                return
            active.cancelled.set()
        deadline = time.monotonic() + 5.0
        terminate_process_tree(active.process, timeout_seconds=_remaining(deadline))
        self._join_relay(active, timeout_seconds=_remaining(deadline))
        self._clear_active(active)

    def _relay_events(
        self,
        active: _ActiveJob,
        emit: Callable[[WorkerEvent], None],
    ) -> None:
        terminal_sent = False
        relay_failure: BaseException | None = None
        try:
            while True:
                try:
                    payload = active.receive_connection.recv_bytes(
                        maxlength=MAX_CHILD_EVENT_BYTES
                    )
                except EOFError:
                    break
                event = parse_worker_event(json.loads(payload.decode("utf-8")))
                if active.cancelled.is_set():
                    continue
                if type(event) not in _RELAYED_EVENT_TYPES:
                    raise TypeError("isolated child sent an unsupported event type")
                if event.request_id != active.request_id:
                    raise ValueError("isolated child sent a mismatched request_id")
                if terminal_sent:
                    raise RuntimeError(
                        "isolated child sent an event after terminal output"
                    )
                emit(event)
                if type(event) in {ResultEvent, ErrorEvent}:
                    terminal_sent = True
        except BaseException as error:
            relay_failure = error
            self._report_internal_error(error)
        finally:
            active.receive_connection.close()
            active.process.join(timeout=0.5)
            if active.process.is_alive():
                try:
                    terminate_process_tree(active.process)
                except BaseException as error:
                    self._report_internal_error(error)
            if not active.cancelled.is_set() and not terminal_sent:
                try:
                    emit(
                        ErrorEvent(
                            request_id=active.request_id,
                            code="WORKER_INTERNAL",
                            message="Isolated recognition job ended without a result.",
                            retryable=False,
                        )
                    )
                except BaseException as error:
                    if relay_failure is None:
                        self._report_internal_error(error)
            self._clear_active(active)

    def _join_relay(self, active: _ActiveJob, *, timeout_seconds: float) -> None:
        relay_thread = active.relay_thread
        if relay_thread is None:
            return
        relay_thread.join(timeout=max(0.0, timeout_seconds))
        if relay_thread.is_alive():
            raise OCRLLMError(
                "The isolated worker event relay did not stop in time.",
                code="WORKER_INTERNAL",
            )

    def _clear_active(self, active: _ActiveJob) -> None:
        with self._state_lock:
            if self._active is active:
                self._active = None

    def _report_internal_error(self, error: BaseException) -> None:
        if self._internal_error_reporter is not None:
            self._internal_error_reporter(error)


def _remaining(deadline: float) -> float:
    return max(0.0, deadline - time.monotonic())
