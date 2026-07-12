"""Recognition-accepted worker event."""

from dataclasses import dataclass
from typing import Literal

from .validate_worker_request_id import validate_worker_request_id
from .worker_protocol_version import CURRENT_WORKER_PROTOCOL_VERSION


@dataclass(frozen=True, slots=True, kw_only=True)
class AcceptedEvent:
    protocol_version: Literal["ocrllm.v1alpha1"] = CURRENT_WORKER_PROTOCOL_VERSION
    event: Literal["accepted"] = "accepted"
    request_id: str

    def __post_init__(self) -> None:
        if (
            self.protocol_version != CURRENT_WORKER_PROTOCOL_VERSION
            or self.event != "accepted"
        ):
            raise ValueError("accepted event envelope is invalid")
        object.__setattr__(
            self, "request_id", validate_worker_request_id(self.request_id)
        )
