"""Pickle-safe deterministic child jobs for isolated-manager tests."""

from __future__ import annotations

import os
import subprocess
import sys
import time
from collections.abc import Callable
from pathlib import Path
from urllib.parse import unquote, urlsplit
from urllib.request import url2pathname

from ocrllm.contracts import (
    ImageRecognitionRequest,
    ProgressEvent,
    ResultEvent,
    WorkerEvent,
    WorkerRecognitionResult,
)
from ocrllm.errors import OCRLLMError


def emit_successful_job(
    command: ImageRecognitionRequest,
    emit: Callable[[WorkerEvent], None],
) -> None:
    emit(
        ProgressEvent(
            request_id=command.request_id,
            stage="fixture",
            completed=1,
            total=1,
            unit="job",
        )
    )
    emit(
        ResultEvent(
            request_id=command.request_id,
            result=WorkerRecognitionResult(
                markdown="# Isolated fixture result\n",
                source_type="image",
                profile="board",
                metadata={"pid": os.getpid()},
            ),
        )
    )


def raise_typed_job_error(
    command: ImageRecognitionRequest,
    emit: Callable[[WorkerEvent], None],
) -> None:
    raise OCRLLMError(
        "Fixture provider timed out.",
        code="PROVIDER_TIMEOUT",
        retryable=True,
        details={"authorization": "secret-sentinel"},
    )


def raise_unexpected_job_error(
    command: ImageRecognitionRequest,
    emit: Callable[[WorkerEvent], None],
) -> None:
    raise RuntimeError("secret-sentinel")


def emit_mismatched_request_id(
    command: ImageRecognitionRequest,
    emit: Callable[[WorkerEvent], None],
) -> None:
    emit(
        ProgressEvent(
            request_id="99999999-9999-4999-8999-999999999999",
            stage="fixture",
            completed=0,
            total=1,
            unit="job",
        )
    )


def return_without_terminal_event(
    command: ImageRecognitionRequest,
    emit: Callable[[WorkerEvent], None],
) -> None:
    return None


def block_with_grandchild(
    command: ImageRecognitionRequest,
    emit: Callable[[WorkerEvent], None],
) -> None:
    source_path = _file_uri_to_path(command.sources[0].uri)
    pid_path = source_path.with_suffix(source_path.suffix + ".grandchild.pid")
    script = (
        "import os,sys,time; "
        "path=sys.argv[1]; "
        "handle=open(path,'w',encoding='utf-8'); "
        "handle.write(str(os.getpid())); handle.flush(); handle.close(); "
        "time.sleep(60)"
    )
    subprocess.Popen(
        [sys.executable, "-c", script, str(pid_path)],
        close_fds=True,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    while True:
        time.sleep(1)


def _file_uri_to_path(uri: str) -> Path:
    parsed = urlsplit(uri)
    decoded_path = url2pathname(unquote(parsed.path))
    if os.name == "nt" and decoded_path.startswith("\\") and len(decoded_path) > 2:
        decoded_path = decoded_path[1:]
    return Path(decoded_path)
