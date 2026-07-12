"""Immutable completed-result state for one resumable image group."""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType

from .contracts.source_fingerprint import SourceFingerprint
from .freeze_json_value import JSONValue, freeze_json_value


IMAGE_RESUME_STATE_VERSION = "ocrllm.image-resume.v1"
_SHA256 = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True, slots=True, kw_only=True)
class ImageResumeState:
    """Store one complete image processor output before final publication."""

    state_version: str
    request_fingerprint: str
    processor_name: str
    processor_version: str
    sources: tuple[SourceFingerprint, ...]
    markdown: str
    media_type: str
    profile: str
    status: str
    hotwords: tuple[str, ...]
    warnings: tuple[str, ...]
    metadata: Mapping[str, JSONValue] = field(default_factory=dict)
    final_markdown_sha256: str = ""

    def __post_init__(self) -> None:
        if self.state_version != IMAGE_RESUME_STATE_VERSION:
            raise ValueError("image resume state version is unsupported")
        for value, field_name in (
            (self.request_fingerprint, "request fingerprint"),
            (self.final_markdown_sha256, "final Markdown SHA-256"),
        ):
            if type(value) is not str or _SHA256.fullmatch(value) is None:
                raise ValueError(f"image resume {field_name} is invalid")
        if type(self.processor_name) is not str or not self.processor_name:
            raise ValueError("image resume processor name is invalid")
        if type(self.processor_version) is not str or not self.processor_version:
            raise ValueError("image resume processor version is invalid")
        if (
            type(self.sources) is not tuple
            or not self.sources
            or any(type(source) is not SourceFingerprint for source in self.sources)
        ):
            raise ValueError("image resume sources are invalid")
        if type(self.markdown) is not str or not self.markdown.strip():
            raise ValueError("image resume Markdown is invalid")
        if self.media_type != "image":
            raise ValueError("image resume media type is invalid")
        if type(self.profile) is not str or not self.profile:
            raise ValueError("image resume profile is invalid")
        if self.status not in {"complete", "partial"}:
            raise ValueError("image resume status is invalid")
        if type(self.hotwords) is not tuple or any(
            type(value) is not str for value in self.hotwords
        ):
            raise ValueError("image resume hotwords are invalid")
        if type(self.warnings) is not tuple or any(
            type(value) is not str for value in self.warnings
        ):
            raise ValueError("image resume warnings are invalid")
        frozen_metadata = freeze_json_value(self.metadata)
        if not isinstance(frozen_metadata, MappingProxyType):
            raise ValueError("image resume metadata is invalid")
        object.__setattr__(self, "metadata", frozen_metadata)
