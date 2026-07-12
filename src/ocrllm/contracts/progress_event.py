"""Bounded worker progress event."""

from dataclasses import dataclass
from typing import Literal

from .validate_nonempty_text import validate_nonempty_text
from .validate_worker_request_id import validate_worker_request_id
from .worker_protocol_version import CURRENT_WORKER_PROTOCOL_VERSION


@dataclass(frozen=True, slots=True, kw_only=True)
class ProgressEvent:
    protocol_version: Literal["ocrllm.v1alpha1"] = CURRENT_WORKER_PROTOCOL_VERSION
    event: Literal["progress"] = "progress"
    request_id: str
    stage: str
    completed: int
    total: int | None
    unit: str

    def __post_init__(self) -> None:
        if (
            self.protocol_version != CURRENT_WORKER_PROTOCOL_VERSION
            or self.event != "progress"
        ):
            raise ValueError("progress event envelope is invalid")
        object.__setattr__(
            self, "request_id", validate_worker_request_id(self.request_id)
        )
        object.__setattr__(
            self,
            "stage",
            validate_nonempty_text(self.stage, field_name="progress stage"),
        )
        if (
            isinstance(self.completed, bool)
            or not isinstance(self.completed, int)
            or self.completed < 0
        ):
            raise ValueError("progress completed must be a nonnegative integer")
        if self.total is not None and (
            isinstance(self.total, bool)
            or not isinstance(self.total, int)
            or self.total < self.completed
        ):
            raise ValueError("progress total must be null or at least completed")
        object.__setattr__(
            self,
            "unit",
            validate_nonempty_text(self.unit, field_name="progress unit"),
        )
