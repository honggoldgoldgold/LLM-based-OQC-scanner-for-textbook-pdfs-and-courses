"""Immutable JSON-safe recognition payload for one worker result event."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Literal, cast

from ocrllm.freeze_json_value import FrozenJSONValue, JSONValue, freeze_json_value

from .artifact import Artifact
from .validate_absolute_file_uri import validate_absolute_file_uri
from .validate_nonempty_text import validate_nonempty_text


@dataclass(frozen=True, slots=True, kw_only=True)
class WorkerRecognitionResult:
    """Carry result data without repeating the event identity envelope."""

    markdown: str
    source_type: Literal["image", "pdf", "audio", "video"]
    profile: str | None = None
    status: Literal["complete", "partial"] = "complete"
    output_uri: str | None = None
    artifacts: tuple[Artifact, ...] = ()
    hotwords: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    metadata: Mapping[str, JSONValue] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "markdown",
            validate_nonempty_text(self.markdown, field_name="result markdown"),
        )
        if self.source_type not in {"image", "pdf", "audio", "video"}:
            raise ValueError("result source_type is not canonical")
        if self.profile is not None:
            object.__setattr__(
                self,
                "profile",
                validate_nonempty_text(self.profile, field_name="result profile"),
            )
        if self.status not in {"complete", "partial"}:
            raise ValueError("result status must be complete or partial")
        if self.output_uri is not None:
            object.__setattr__(
                self,
                "output_uri",
                validate_absolute_file_uri(
                    self.output_uri,
                    field_name="result output_uri",
                ),
            )

        artifacts = tuple(self.artifacts)
        if any(type(artifact) is not Artifact for artifact in artifacts):
            raise TypeError("result artifacts must contain exact Artifact values")
        hotwords = tuple(self.hotwords)
        warnings = tuple(self.warnings)
        if any(not isinstance(value, str) for value in hotwords):
            raise TypeError("result hotwords must contain text")
        if any(not isinstance(value, str) for value in warnings):
            raise TypeError("result warnings must contain text")

        frozen_metadata = freeze_json_value(self.metadata)
        if not isinstance(frozen_metadata, MappingProxyType):
            raise TypeError("result metadata must be a JSON object")
        object.__setattr__(self, "artifacts", artifacts)
        object.__setattr__(self, "hotwords", hotwords)
        object.__setattr__(self, "warnings", warnings)
        object.__setattr__(
            self,
            "metadata",
            cast(Mapping[str, FrozenJSONValue], frozen_metadata),
        )
