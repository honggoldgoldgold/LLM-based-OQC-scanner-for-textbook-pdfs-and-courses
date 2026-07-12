"""Worker capability-query response event."""

from dataclasses import dataclass
from typing import Literal

from .capability_report import CapabilityReport
from .validate_worker_request_id import validate_worker_request_id
from .worker_protocol_version import CURRENT_WORKER_PROTOCOL_VERSION


@dataclass(frozen=True, slots=True, kw_only=True)
class CapabilitiesEvent:
    protocol_version: Literal["ocrllm.v1alpha1"] = CURRENT_WORKER_PROTOCOL_VERSION
    event: Literal["capabilities"] = "capabilities"
    request_id: str
    capabilities: tuple[CapabilityReport, ...]

    def __post_init__(self) -> None:
        if (
            self.protocol_version != CURRENT_WORKER_PROTOCOL_VERSION
            or self.event != "capabilities"
        ):
            raise ValueError("capabilities event envelope is invalid")
        object.__setattr__(
            self, "request_id", validate_worker_request_id(self.request_id)
        )
        capabilities = tuple(self.capabilities)
        if any(type(report) is not CapabilityReport for report in capabilities):
            raise TypeError("capabilities must contain exact CapabilityReport values")
        object.__setattr__(self, "capabilities", capabilities)
