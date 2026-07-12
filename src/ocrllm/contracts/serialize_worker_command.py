"""Serialize one validated worker command to mutable JSON data."""

from __future__ import annotations

from ocrllm.thaw_json_value import thaw_json_value

from .cancel_command import CancelCommand
from .capabilities_command import CapabilitiesCommand
from .image_recognition_request import ImageRecognitionRequest
from .worker_command import WorkerCommand


def serialize_worker_command(command: WorkerCommand) -> dict[str, object]:
    """Return a fresh canonical JSON object for one exact command DTO."""

    if type(command) is CapabilitiesCommand or type(command) is CancelCommand:
        return {
            "protocol_version": command.protocol_version,
            "command": command.command,
            "request_id": command.request_id,
        }
    if type(command) is ImageRecognitionRequest:
        return {
            "protocol_version": command.protocol_version,
            "command": command.command,
            "request_id": command.request_id,
            "sources": [
                {"media_type": source.media_type, "uri": source.uri}
                for source in command.sources
            ],
            "provider": command.provider,
            "model": command.model,
            "input_languages": list(command.input_languages),
            "output_language": command.output_language,
            "profile": command.profile,
            "options": thaw_json_value(command.options),
        }
    raise TypeError("command must be an exact worker command DTO")
