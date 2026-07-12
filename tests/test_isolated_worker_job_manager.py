from __future__ import annotations

import os
import subprocess
import time
from collections.abc import Callable
from pathlib import Path

import pytest

from ocrllm.contracts import (
    AcceptedEvent,
    CancelCommand,
    ErrorEvent,
    ImageRecognitionRequest,
    ResultEvent,
    SourceDescriptor,
    WorkerEvent,
)
from ocrllm.errors import OCRLLMError
from ocrllm.worker import IsolatedWorkerJobManager
from worker_job_fixtures import (
    block_with_grandchild,
    emit_mismatched_request_id,
    emit_successful_job,
    raise_typed_job_error,
    raise_unexpected_job_error,
    return_without_terminal_event,
)


ACTIVE_ID = "22222222-2222-4222-8222-222222222222"
OTHER_ID = "33333333-3333-4333-8333-333333333333"


def _command(source: Path, *, request_id: str = ACTIVE_ID) -> ImageRecognitionRequest:
    return ImageRecognitionRequest(
        request_id=request_id,
        sources=(SourceDescriptor(media_type="image", uri=source.resolve().as_uri()),),
        provider="dashscope",
        model=None,
    )


def _wait_until(predicate: Callable[[], bool], *, timeout: float = 10.0) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if predicate():
            return
        time.sleep(0.02)
    raise AssertionError("condition did not become true before timeout")


def test_isolated_manager_relays_accepted_progress_and_result(tmp_path) -> None:
    source = tmp_path / "board.png"
    source.write_bytes(b"fixture")
    events: list[WorkerEvent] = []
    manager = IsolatedWorkerJobManager(emit_successful_job)

    manager.start(_command(source), emit=events.append)
    _wait_until(lambda: any(type(event) is ResultEvent for event in events))
    _wait_until(lambda: manager.active_request_id is None)
    manager.close()

    assert type(events[0]) is AcceptedEvent
    assert [event.event for event in events] == ["accepted", "progress", "result"]
    result = events[-1]
    assert isinstance(result, ResultEvent)
    assert result.result.metadata["pid"] != os.getpid()


@pytest.mark.parametrize(
    ("job_callable", "expected_code", "expected_retryable"),
    [
        (raise_typed_job_error, "PROVIDER_TIMEOUT", True),
        (raise_unexpected_job_error, "WORKER_INTERNAL", False),
        (emit_mismatched_request_id, "WORKER_INTERNAL", False),
        (return_without_terminal_event, "WORKER_INTERNAL", False),
    ],
)
def test_isolated_child_failures_become_one_typed_terminal_event(
    tmp_path,
    job_callable,
    expected_code,
    expected_retryable,
) -> None:
    source = tmp_path / "board.png"
    source.write_bytes(b"fixture")
    events: list[WorkerEvent] = []
    manager = IsolatedWorkerJobManager(job_callable)

    manager.start(_command(source), emit=events.append)
    _wait_until(lambda: any(type(event) is ErrorEvent for event in events))
    _wait_until(lambda: manager.active_request_id is None)
    manager.close()

    terminal = [event for event in events if type(event) is ErrorEvent]
    assert len(terminal) == 1
    assert terminal[0].code == expected_code
    assert terminal[0].retryable is expected_retryable
    assert "secret-sentinel" not in repr(terminal[0])


def test_busy_and_wrong_cancel_do_not_replace_or_kill_active_job(tmp_path) -> None:
    source = tmp_path / "board.png"
    source.write_bytes(b"fixture")
    events: list[WorkerEvent] = []
    manager = IsolatedWorkerJobManager(block_with_grandchild)
    manager.start(_command(source), emit=events.append)

    with pytest.raises(OCRLLMError) as busy:
        manager.start(_command(source, request_id=OTHER_ID), emit=events.append)
    with pytest.raises(OCRLLMError) as wrong_cancel:
        manager.cancel(CancelCommand(request_id=OTHER_ID), emit=events.append)

    assert busy.value.code == "WORKER_BUSY"
    assert wrong_cancel.value.code == "REQUEST_NOT_ACTIVE"
    assert manager.active_request_id == ACTIVE_ID
    manager.cancel(CancelCommand(request_id=ACTIVE_ID), emit=events.append)
    assert manager.active_request_id is None


def test_cancel_terminates_child_and_grandchild_within_five_seconds(tmp_path) -> None:
    source = tmp_path / "board.png"
    source.write_bytes(b"fixture")
    pid_path = source.with_suffix(source.suffix + ".grandchild.pid")
    events: list[WorkerEvent] = []
    manager = IsolatedWorkerJobManager(block_with_grandchild)
    manager.start(_command(source), emit=events.append)
    _wait_until(pid_path.exists)
    grandchild_pid = int(pid_path.read_text(encoding="utf-8"))

    started = time.monotonic()
    try:
        manager.cancel(CancelCommand(request_id=ACTIVE_ID), emit=events.append)
        elapsed = time.monotonic() - started
        _wait_until(lambda: not _pid_exists(grandchild_pid), timeout=2.0)
    finally:
        manager.close()
        _kill_pid_if_alive(grandchild_pid)

    assert elapsed <= 5.0
    assert manager.active_request_id is None
    cancelled = [event for event in events if type(event) is ErrorEvent]
    assert len(cancelled) == 1
    assert cancelled[0].code == "CANCELLED"


def test_close_terminates_active_tree_without_emitting_cancelled(tmp_path) -> None:
    source = tmp_path / "board.png"
    source.write_bytes(b"fixture")
    pid_path = source.with_suffix(source.suffix + ".grandchild.pid")
    events: list[WorkerEvent] = []
    manager = IsolatedWorkerJobManager(block_with_grandchild)
    manager.start(_command(source), emit=events.append)
    _wait_until(pid_path.exists)
    grandchild_pid = int(pid_path.read_text(encoding="utf-8"))

    try:
        manager.close()
        _wait_until(lambda: not _pid_exists(grandchild_pid), timeout=2.0)
    finally:
        _kill_pid_if_alive(grandchild_pid)

    assert manager.active_request_id is None
    assert not any(type(event) is ErrorEvent for event in events)


def _pid_exists(pid: int) -> bool:
    if os.name == "nt":
        completed = subprocess.run(
            ["tasklist", "/FI", f"PID eq {pid}", "/FO", "CSV", "/NH"],
            check=False,
            capture_output=True,
            text=True,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            timeout=5,
        )
        return f'"{pid}"' in completed.stdout
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def _kill_pid_if_alive(pid: int) -> None:
    if not _pid_exists(pid):
        return
    if os.name == "nt":
        subprocess.run(
            ["taskkill", "/PID", str(pid), "/T", "/F"],
            check=False,
            capture_output=True,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            timeout=5,
        )
    else:
        os.kill(pid, 9)
