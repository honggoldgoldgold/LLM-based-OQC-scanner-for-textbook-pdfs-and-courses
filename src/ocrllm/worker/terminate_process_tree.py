"""Terminate one isolated worker process and all descendants within a deadline."""

from __future__ import annotations

import os
import signal
import subprocess
import time
from multiprocessing.process import BaseProcess

from ocrllm.errors import OCRLLMError


def terminate_process_tree(
    process: BaseProcess, *, timeout_seconds: float = 5.0
) -> None:
    """Terminate a spawned child tree on Windows or its POSIX process group."""

    if timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be positive")
    deadline = time.monotonic() + timeout_seconds
    if not process.is_alive():
        process.join(timeout=0)
        return
    if process.pid is None:
        raise _termination_failed()

    if os.name == "nt":
        _taskkill_tree(process.pid, timeout_seconds=_remaining(deadline))
    else:
        _signal_process_group(process.pid, signal.SIGTERM)

    process.join(timeout=min(1.0, _remaining(deadline)))
    if process.is_alive():
        if os.name == "nt":
            _taskkill_tree(process.pid, timeout_seconds=_remaining(deadline))
        else:
            _signal_process_group(process.pid, signal.SIGKILL)
        process.join(timeout=_remaining(deadline))
    if process.is_alive():
        raise _termination_failed()


def _taskkill_tree(pid: int, *, timeout_seconds: float) -> None:
    if timeout_seconds <= 0:
        return
    try:
        subprocess.run(
            ["taskkill", "/PID", str(pid), "/T", "/F"],
            check=False,
            capture_output=True,
            timeout=timeout_seconds,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
    except (OSError, subprocess.SubprocessError):
        return


def _signal_process_group(pid: int, signal_number: signal.Signals) -> None:
    try:
        os.killpg(pid, signal_number)
    except ProcessLookupError:
        return
    except OSError:
        return


def _remaining(deadline: float) -> float:
    return max(0.0, deadline - time.monotonic())


def _termination_failed() -> OCRLLMError:
    return OCRLLMError(
        "The isolated worker process tree could not be terminated in time.",
        code="WORKER_INTERNAL",
    )
