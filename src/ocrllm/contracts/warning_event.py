"""Secret-safe degraded-success worker warning event."""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Literal

from ocrllm.errors import OCRLLMError
from ocrllm.freeze_json_value import JSONValue

from .validate_nonempty_text import validate_nonempty_text
from .validate_worker_request_id import validate_worker_request_id
from .worker_protocol_version import CURRENT_WORKER_PROTOCOL_VERSION


_STABLE_CODE = re.compile(r"^[A-Z][A-Z0-9_]*$")


@dataclass(frozen=True, slots=True, kw_only=True)
class WarningEvent:
    protocol_version: Literal["ocrllm.v1alpha1"] = CURRENT_WORKER_PROTOCOL_VERSION
    event: Literal["warning"] = "warning"
    request_id: str
    code: str
    message: str
    details: Mapping[str, JSONValue] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if (
            self.protocol_version != CURRENT_WORKER_PROTOCOL_VERSION
            or self.event != "warning"
        ):
            raise ValueError("warning event envelope is invalid")
        object.__setattr__(
            self, "request_id", validate_worker_request_id(self.request_id)
        )
        if not isinstance(self.code, str) or _STABLE_CODE.fullmatch(self.code) is None:
            raise ValueError("warning code must be stable uppercase text")
        object.__setattr__(
            self,
            "message",
            validate_nonempty_text(self.message, field_name="warning message"),
        )
        redaction_probe = OCRLLMError(code="COMMAND_INVALID", details=self.details)
        object.__setattr__(
            self,
            "details",
            redaction_probe.details,
        )
