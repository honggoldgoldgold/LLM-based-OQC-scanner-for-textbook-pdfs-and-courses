"""One immutable worker capability report."""

from dataclasses import dataclass
from typing import Literal

from .validate_nonempty_text import validate_nonempty_text


@dataclass(frozen=True, slots=True, kw_only=True)
class CapabilityReport:
    name: str
    status: Literal["available", "experimental", "unavailable", "deferred"]
    reason: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "name",
            validate_nonempty_text(self.name, field_name="capability name"),
        )
        if self.status not in {"available", "experimental", "unavailable", "deferred"}:
            raise ValueError("capability status is not canonical")
        object.__setattr__(
            self,
            "reason",
            validate_nonempty_text(self.reason, field_name="capability reason"),
        )
