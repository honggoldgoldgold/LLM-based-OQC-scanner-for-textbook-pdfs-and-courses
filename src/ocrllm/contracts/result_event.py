"""Successful worker recognition result event."""

from dataclasses import dataclass
from typing import Literal

from .validate_worker_request_id import validate_worker_request_id
from .worker_protocol_version import CURRENT_WORKER_PROTOCOL_VERSION
from .worker_recognition_result import WorkerRecognitionResult


@dataclass(frozen=True, slots=True, kw_only=True)
class ResultEvent:
    protocol_version: Literal["ocrllm.v1alpha1"] = CURRENT_WORKER_PROTOCOL_VERSION
    event: Literal["result"] = "result"
    request_id: str
    result: WorkerRecognitionResult

    def __post_init__(self) -> None:
        if (
            self.protocol_version != CURRENT_WORKER_PROTOCOL_VERSION
            or self.event != "result"
        ):
            raise ValueError("result event envelope is invalid")
        object.__setattr__(
            self, "request_id", validate_worker_request_id(self.request_id)
        )
        if type(self.result) is not WorkerRecognitionResult:
            raise TypeError("result must be an exact WorkerRecognitionResult")
