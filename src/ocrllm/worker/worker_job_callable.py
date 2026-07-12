"""Pickle-safe callable contract for one isolated recognition job."""

from collections.abc import Callable
from typing import TypeAlias

from ocrllm.contracts.image_recognition_request import ImageRecognitionRequest
from ocrllm.contracts.worker_event import WorkerEvent


WorkerJobCallable: TypeAlias = Callable[
    [ImageRecognitionRequest, Callable[[WorkerEvent], None]],
    None,
]
