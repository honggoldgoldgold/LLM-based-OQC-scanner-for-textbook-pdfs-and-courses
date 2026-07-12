"""One JSON-safe recognition source descriptor."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from .validate_absolute_file_uri import validate_absolute_file_uri


@dataclass(frozen=True, slots=True, kw_only=True)
class SourceDescriptor:
    """Describe one local source without opening it or retaining a handle."""

    media_type: Literal["image", "pdf", "audio", "video"]
    uri: str

    def __post_init__(self) -> None:
        if self.media_type not in {"image", "pdf", "audio", "video"}:
            raise ValueError("source media_type is not canonical")
        object.__setattr__(
            self,
            "uri",
            validate_absolute_file_uri(self.uri, field_name="source uri"),
        )
