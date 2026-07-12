"""Execute one worker image command through the proven public facade."""

from __future__ import annotations

from collections.abc import Callable

from ocrllm.contracts.build_worker_recognition_result import (
    build_worker_recognition_result,
)
from ocrllm.contracts.image_recognition_request import ImageRecognitionRequest
from ocrllm.contracts.progress_event import ProgressEvent
from ocrllm.contracts.result_event import ResultEvent
from ocrllm.contracts.worker_event import WorkerEvent
from ocrllm.recognize import recognize

from .build_worker_image_config import build_worker_image_config
from .file_uri_to_path import file_uri_to_path


def run_image_recognition_job(
    command: ImageRecognitionRequest,
    emit: Callable[[WorkerEvent], None],
) -> None:
    """Recognize one ordered image group and emit progress plus one result."""

    if type(command) is not ImageRecognitionRequest:
        raise TypeError("command must be an exact ImageRecognitionRequest")
    source_paths = tuple(file_uri_to_path(source.uri) for source in command.sources)
    config = build_worker_image_config(command)
    total = len(source_paths)
    emit(
        ProgressEvent(
            request_id=command.request_id,
            stage="recognition",
            completed=0,
            total=total,
            unit="image",
        )
    )
    direct_result = recognize(source_paths, config=config)
    worker_result = build_worker_recognition_result(direct_result)
    emit(
        ProgressEvent(
            request_id=command.request_id,
            stage="recognition",
            completed=total,
            total=total,
            unit="image",
        )
    )
    emit(ResultEvent(request_id=command.request_id, result=worker_result))
