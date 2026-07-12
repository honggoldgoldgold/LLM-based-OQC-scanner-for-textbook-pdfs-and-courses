"""Protocol for nonblocking recognition job ownership behind the control loop."""

from __future__ import annotations

from collections.abc import Callable
from typing import Protocol

from ocrllm.contracts.cancel_command import CancelCommand
from ocrllm.contracts.image_recognition_request import ImageRecognitionRequest
from ocrllm.contracts.worker_event import WorkerEvent


class WorkerJobManager(Protocol):
    """Start/cancel jobs without blocking the command-reading control loop."""

    def start(
        self,
        command: ImageRecognitionRequest,
        *,
        emit: Callable[[WorkerEvent], None],
    ) -> None:
        """Start one job or raise a typed worker error before returning."""

    def cancel(
        self,
        command: CancelCommand,
        *,
        emit: Callable[[WorkerEvent], None],
    ) -> None:
        """Cancel the matching job or raise a typed worker error."""

    def close(self) -> None:
        """Release or terminate any active job before worker shutdown."""
