"""Immutable ocrllm.v1alpha1 image recognition command."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Literal

from ocrllm.errors import ConfigError
from ocrllm.freeze_json_value import JSONValue

from .freeze_image_recognition_options import freeze_image_recognition_options
from .source_descriptor import SourceDescriptor
from .validate_language_tag import validate_language_tag
from .validate_worker_request_id import validate_worker_request_id
from .worker_protocol_version import CURRENT_WORKER_PROTOCOL_VERSION


@dataclass(frozen=True, slots=True, kw_only=True)
class ImageRecognitionRequest:
    """Represent one strict, ordered Phase 2 image request."""

    protocol_version: Literal["ocrllm.v1alpha1"] = CURRENT_WORKER_PROTOCOL_VERSION
    command: Literal["recognize"] = "recognize"
    request_id: str
    sources: tuple[SourceDescriptor, ...]
    provider: Literal["dashscope"]
    model: str | None
    input_languages: tuple[str, ...] = ()
    output_language: str | None = None
    profile: Literal["board"] = "board"
    options: Mapping[str, JSONValue] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.protocol_version != CURRENT_WORKER_PROTOCOL_VERSION:
            raise ValueError("image request protocol_version is not supported")
        if self.command != "recognize":
            raise ValueError("image request command must be recognize")
        object.__setattr__(
            self, "request_id", validate_worker_request_id(self.request_id)
        )

        sources = tuple(self.sources)
        if not sources or any(
            type(source) is not SourceDescriptor for source in sources
        ):
            raise ConfigError("Recognition sources must be a nonempty descriptor list.")
        if any(source.media_type != "image" for source in sources):
            raise ConfigError("V1alpha1 recognition sources must all be images.")
        object.__setattr__(self, "sources", sources)

        if self.provider != "dashscope":
            raise ConfigError("V1alpha1 recognition provider must be dashscope.")
        if self.model is not None and (
            not isinstance(self.model, str) or not self.model.strip()
        ):
            raise ConfigError("Recognition model must be nonempty text or null.")

        languages = tuple(self.input_languages)
        try:
            languages = tuple(
                validate_language_tag(value, field_name="input_languages")
                for value in languages
            )
            output_language = (
                None
                if self.output_language is None
                else validate_language_tag(
                    self.output_language,
                    field_name="output_language",
                )
            )
        except (TypeError, ValueError):
            raise ConfigError("Recognition languages must be BCP-47 tags.") from None
        object.__setattr__(self, "input_languages", languages)
        object.__setattr__(self, "output_language", output_language)

        if self.profile != "board":
            raise ConfigError("V1alpha1 recognition profile must be board.")
        object.__setattr__(
            self,
            "options",
            freeze_image_recognition_options(self.options),
        )
