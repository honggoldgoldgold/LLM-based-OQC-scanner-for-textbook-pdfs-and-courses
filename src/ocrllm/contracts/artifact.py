"""One final user-meaningful worker artifact."""

from __future__ import annotations

from dataclasses import dataclass

from .validate_absolute_file_uri import validate_absolute_file_uri
from .validate_nonempty_text import validate_nonempty_text


@dataclass(frozen=True, slots=True, kw_only=True)
class Artifact:
    kind: str
    uri: str
    media_type: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "kind",
            validate_nonempty_text(self.kind, field_name="artifact kind"),
        )
        object.__setattr__(
            self,
            "uri",
            validate_absolute_file_uri(self.uri, field_name="artifact uri"),
        )
        media_type = validate_nonempty_text(
            self.media_type,
            field_name="artifact media_type",
        )
        if "/" not in media_type or any(
            character.isspace() for character in media_type
        ):
            raise ValueError("artifact media_type must be a MIME type")
        object.__setattr__(self, "media_type", media_type)
