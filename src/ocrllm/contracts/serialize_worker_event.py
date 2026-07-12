"""Serialize one exact worker event to mutable JSON data."""

from __future__ import annotations

from ocrllm.thaw_json_value import thaw_json_value

from .accepted_event import AcceptedEvent
from .capabilities_event import CapabilitiesEvent
from .error_event import ErrorEvent
from .progress_event import ProgressEvent
from .result_event import ResultEvent
from .warning_event import WarningEvent
from .worker_event import WorkerEvent
from .worker_recognition_result import WorkerRecognitionResult


def serialize_worker_event(event: WorkerEvent) -> dict[str, object]:
    """Return a fresh canonical JSON object for one exact event DTO."""

    envelope: dict[str, object] = {
        "protocol_version": event.protocol_version,
        "event": event.event,
        "request_id": event.request_id,
    }
    if type(event) is AcceptedEvent:
        return envelope
    if type(event) is ProgressEvent:
        return envelope | {
            "stage": event.stage,
            "completed": event.completed,
            "total": event.total,
            "unit": event.unit,
        }
    if type(event) is WarningEvent:
        return envelope | {
            "code": event.code,
            "message": event.message,
            "details": thaw_json_value(event.details),
        }
    if type(event) is ErrorEvent:
        return envelope | {
            "code": event.code,
            "message": event.message,
            "retryable": event.retryable,
            "details": thaw_json_value(event.details),
        }
    if type(event) is CapabilitiesEvent:
        return envelope | {
            "capabilities": [
                {"name": report.name, "status": report.status, "reason": report.reason}
                for report in event.capabilities
            ]
        }
    if type(event) is ResultEvent:
        return envelope | {"result": _serialize_result(event.result)}
    raise TypeError("event must be an exact worker event DTO")


def _serialize_result(result: WorkerRecognitionResult) -> dict[str, object]:
    return {
        "markdown": result.markdown,
        "source_type": result.source_type,
        "profile": result.profile,
        "status": result.status,
        "output_uri": result.output_uri,
        "artifacts": [
            {"kind": item.kind, "uri": item.uri, "media_type": item.media_type}
            for item in result.artifacts
        ],
        "hotwords": list(result.hotwords),
        "warnings": list(result.warnings),
        "metadata": thaw_json_value(result.metadata),
    }
