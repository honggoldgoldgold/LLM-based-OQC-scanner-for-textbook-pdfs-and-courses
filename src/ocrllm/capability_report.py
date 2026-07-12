"""One immutable public atomic capability report."""

from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True, slots=True, kw_only=True)
class CapabilityReport:
    name: str
    status: Literal["available", "experimental", "unavailable", "deferred"]
    reason: str

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("capability name must be nonempty text")
        if self.status not in {
            "available",
            "experimental",
            "unavailable",
            "deferred",
        }:
            raise ValueError("capability status is not canonical")
        if not isinstance(self.reason, str) or not self.reason.strip():
            raise ValueError("capability reason must be nonempty text")
