"""Typed secret-safe worker error event."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Literal

from ocrllm.errors import OCRLLMError
from ocrllm.freeze_json_value import JSONValue

from .validate_worker_request_id import validate_worker_request_id
from .worker_protocol_version import CURRENT_WORKER_PROTOCOL_VERSION


@dataclass(frozen=True, slots=True, kw_only=True)
class ErrorEvent:
    protocol_version: Literal["ocrllm.v1alpha1"] = CURRENT_WORKER_PROTOCOL_VERSION
    event: Literal["error"] = "error"
    request_id: str | None
    code: str
    message: str
    retryable: bool
    details: Mapping[str, JSONValue] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if (
            self.protocol_version != CURRENT_WORKER_PROTOCOL_VERSION
            or self.event != "error"
        ):
            raise ValueError("error event envelope is invalid")
        if self.request_id is not None:
            object.__setattr__(
                self,
                "request_id",
                validate_worker_request_id(self.request_id),
            )
        validated = OCRLLMError(
            self.message,
            code=self.code,
            retryable=self.retryable,
            details=self.details,
        )
        object.__setattr__(self, "message", str(validated))
        object.__setattr__(self, "details", validated.details)
