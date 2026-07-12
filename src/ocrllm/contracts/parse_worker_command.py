"""Parse one decoded JSON object into an exact worker command."""

from __future__ import annotations

from collections.abc import Mapping
from typing import cast

from ocrllm.errors import ConfigError, OCRLLMError

from .cancel_command import CancelCommand
from .capabilities_command import CapabilitiesCommand
from .image_recognition_request import ImageRecognitionRequest
from .source_descriptor import SourceDescriptor
from .validate_worker_request_id import validate_worker_request_id
from .worker_command import WorkerCommand
from .worker_protocol_version import CURRENT_WORKER_PROTOCOL_VERSION


_CONTROL_FIELDS = frozenset({"protocol_version", "command", "request_id"})
_RECOGNIZE_FIELDS = frozenset(
    {
        "protocol_version",
        "command",
        "request_id",
        "sources",
        "provider",
        "model",
        "input_languages",
        "output_language",
        "profile",
        "options",
    }
)


def parse_worker_command(value: object) -> WorkerCommand:
    """Strictly parse a Phase 2 command without echoing caller-controlled data."""

    if not isinstance(value, Mapping) or any(not isinstance(key, str) for key in value):
        raise _command_invalid()

    protocol_version = value.get("protocol_version")
    if protocol_version != CURRENT_WORKER_PROTOCOL_VERSION:
        if isinstance(protocol_version, str):
            raise OCRLLMError(
                "Worker protocol version is not supported.",
                code="PROTOCOL_UNSUPPORTED",
            )
        raise _command_invalid()

    command = value.get("command")
    if command == "capabilities":
        _require_exact_fields(value, _CONTROL_FIELDS)
        request_id = _parse_request_id(value.get("request_id"))
        return CapabilitiesCommand(request_id=request_id)
    if command == "cancel":
        _require_exact_fields(value, _CONTROL_FIELDS)
        request_id = _parse_request_id(value.get("request_id"))
        return CancelCommand(request_id=request_id)
    if command != "recognize":
        raise _command_invalid()

    _require_exact_fields(value, _RECOGNIZE_FIELDS)
    request_id = _parse_request_id(value.get("request_id"))
    sources_value = value.get("sources")
    if not isinstance(sources_value, list):
        raise ConfigError("Recognition sources must be a nonempty JSON array.")
    try:
        sources = tuple(_parse_source_descriptor(source) for source in sources_value)
        input_languages_value = value.get("input_languages")
        if not isinstance(input_languages_value, list) or any(
            not isinstance(language, str) for language in input_languages_value
        ):
            raise ConfigError("Recognition input_languages must be a JSON array.")
        options = value.get("options")
        return ImageRecognitionRequest(
            request_id=request_id,
            sources=sources,
            provider=cast(object, value.get("provider")),
            model=cast(object, value.get("model")),
            input_languages=tuple(input_languages_value),
            output_language=cast(object, value.get("output_language")),
            profile=cast(object, value.get("profile")),
            options=cast(object, options),
        )
    except ConfigError:
        raise
    except (TypeError, ValueError):
        raise ConfigError("Recognition command configuration is invalid.") from None


def _require_exact_fields(
    value: Mapping[object, object], expected: frozenset[str]
) -> None:
    if set(value) != expected:
        raise _command_invalid()


def _parse_request_id(value: object) -> str:
    try:
        return validate_worker_request_id(value)
    except (TypeError, ValueError):
        raise _command_invalid() from None


def _parse_source_descriptor(value: object) -> SourceDescriptor:
    if not isinstance(value, Mapping) or set(value) != {"media_type", "uri"}:
        raise ConfigError("Recognition source descriptors are invalid.")
    return SourceDescriptor(
        media_type=cast(object, value.get("media_type")),
        uri=cast(object, value.get("uri")),
    )


def _command_invalid() -> OCRLLMError:
    return OCRLLMError("Worker command is invalid.", code="COMMAND_INVALID")
