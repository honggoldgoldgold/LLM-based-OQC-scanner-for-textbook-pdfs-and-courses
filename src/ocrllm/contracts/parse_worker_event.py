"""Parse one decoded JSON object into an exact worker event."""

from __future__ import annotations

from collections.abc import Mapping
from typing import cast

from .accepted_event import AcceptedEvent
from .artifact import Artifact
from .capabilities_event import CapabilitiesEvent
from .capability_report import CapabilityReport
from .error_event import ErrorEvent
from .progress_event import ProgressEvent
from .result_event import ResultEvent
from .warning_event import WarningEvent
from .worker_event import WorkerEvent
from .worker_protocol_version import CURRENT_WORKER_PROTOCOL_VERSION
from .worker_recognition_result import WorkerRecognitionResult


_ENVELOPE_FIELDS = frozenset({"protocol_version", "event", "request_id"})


def parse_worker_event(value: object) -> WorkerEvent:
    """Strictly reconstruct one validated event from JSON-compatible data."""

    if not isinstance(value, Mapping) or any(not isinstance(key, str) for key in value):
        raise ValueError("worker event must be a JSON object")
    if value.get("protocol_version") != CURRENT_WORKER_PROTOCOL_VERSION:
        raise ValueError("worker event protocol_version is not supported")

    event = value.get("event")
    if event == "accepted":
        _require_fields(value, _ENVELOPE_FIELDS)
        return AcceptedEvent(request_id=cast(object, value.get("request_id")))
    if event == "progress":
        _require_fields(
            value,
            _ENVELOPE_FIELDS | {"stage", "completed", "total", "unit"},
        )
        return ProgressEvent(
            request_id=cast(object, value.get("request_id")),
            stage=cast(object, value.get("stage")),
            completed=cast(object, value.get("completed")),
            total=cast(object, value.get("total")),
            unit=cast(object, value.get("unit")),
        )
    if event == "warning":
        _require_fields(
            value,
            _ENVELOPE_FIELDS | {"code", "message", "details"},
        )
        return WarningEvent(
            request_id=cast(object, value.get("request_id")),
            code=cast(object, value.get("code")),
            message=cast(object, value.get("message")),
            details=cast(object, value.get("details")),
        )
    if event == "error":
        _require_fields(
            value,
            _ENVELOPE_FIELDS | {"code", "message", "retryable", "details"},
        )
        return ErrorEvent(
            request_id=cast(object, value.get("request_id")),
            code=cast(object, value.get("code")),
            message=cast(object, value.get("message")),
            retryable=cast(object, value.get("retryable")),
            details=cast(object, value.get("details")),
        )
    if event == "capabilities":
        _require_fields(value, _ENVELOPE_FIELDS | {"capabilities"})
        capabilities_value = value.get("capabilities")
        if not isinstance(capabilities_value, list):
            raise ValueError("capabilities event payload must be a JSON array")
        return CapabilitiesEvent(
            request_id=cast(object, value.get("request_id")),
            capabilities=tuple(
                _parse_capability_report(report) for report in capabilities_value
            ),
        )
    if event == "result":
        _require_fields(value, _ENVELOPE_FIELDS | {"result"})
        return ResultEvent(
            request_id=cast(object, value.get("request_id")),
            result=_parse_worker_result(value.get("result")),
        )
    raise ValueError("worker event literal is invalid")


def _parse_capability_report(value: object) -> CapabilityReport:
    if not isinstance(value, Mapping) or set(value) != {"name", "status", "reason"}:
        raise ValueError("capability report is invalid")
    return CapabilityReport(
        name=cast(object, value.get("name")),
        status=cast(object, value.get("status")),
        reason=cast(object, value.get("reason")),
    )


def _parse_worker_result(value: object) -> WorkerRecognitionResult:
    fields = {
        "markdown",
        "source_type",
        "profile",
        "status",
        "output_uri",
        "artifacts",
        "hotwords",
        "warnings",
        "metadata",
    }
    if not isinstance(value, Mapping) or set(value) != fields:
        raise ValueError("worker result payload is invalid")
    artifacts_value = value.get("artifacts")
    hotwords_value = value.get("hotwords")
    warnings_value = value.get("warnings")
    if not isinstance(artifacts_value, list):
        raise ValueError("worker result artifacts must be a JSON array")
    if not isinstance(hotwords_value, list) or not isinstance(warnings_value, list):
        raise ValueError("worker result text lists must be JSON arrays")
    return WorkerRecognitionResult(
        markdown=cast(object, value.get("markdown")),
        source_type=cast(object, value.get("source_type")),
        profile=cast(object, value.get("profile")),
        status=cast(object, value.get("status")),
        output_uri=cast(object, value.get("output_uri")),
        artifacts=tuple(_parse_artifact(item) for item in artifacts_value),
        hotwords=tuple(hotwords_value),
        warnings=tuple(warnings_value),
        metadata=cast(object, value.get("metadata")),
    )


def _parse_artifact(value: object) -> Artifact:
    if not isinstance(value, Mapping) or set(value) != {"kind", "uri", "media_type"}:
        raise ValueError("worker artifact is invalid")
    return Artifact(
        kind=cast(object, value.get("kind")),
        uri=cast(object, value.get("uri")),
        media_type=cast(object, value.get("media_type")),
    )


def _require_fields(
    value: Mapping[object, object], expected: set[str] | frozenset[str]
) -> None:
    if set(value) != expected:
        raise ValueError("worker event fields are invalid")
