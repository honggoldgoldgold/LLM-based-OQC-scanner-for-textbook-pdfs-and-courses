from __future__ import annotations

import json
from dataclasses import FrozenInstanceError, dataclass
from pathlib import Path
from types import MappingProxyType

import pytest

from ocrllm import RecognitionResult
from ocrllm.contracts import (
    AcceptedEvent,
    Artifact,
    CapabilitiesEvent,
    CapabilityReport,
    ErrorEvent,
    ProgressEvent,
    ResultEvent,
    WarningEvent,
    WorkerRecognitionResult,
    build_worker_recognition_result,
    serialize_worker_event,
)


FIXTURE = Path(__file__).parent / "fixtures" / "worker" / "v1alpha1_events.jsonl"
REQUEST_ID = "22222222-2222-4222-8222-222222222222"


def _events() -> list[object]:
    return [
        CapabilitiesEvent(
            request_id="11111111-1111-4111-8111-111111111111",
            capabilities=(
                CapabilityReport(
                    name="image.board.png",
                    status="available",
                    reason="Phase 1 live and packaging gates passed.",
                ),
            ),
        ),
        AcceptedEvent(request_id=REQUEST_ID),
        ProgressEvent(
            request_id=REQUEST_ID,
            stage="recognition",
            completed=1,
            total=2,
            unit="image",
        ),
        WarningEvent(
            request_id=REQUEST_ID,
            code="SIGN_RESTORED",
            message="One source-visible sign was restored by quorum.",
            details={"count": 1},
        ),
        ResultEvent(
            request_id=REQUEST_ID,
            result=WorkerRecognitionResult(
                markdown="# 识别结果\n",
                source_type="image",
                profile="board",
                hotwords=("遗传",),
                metadata={"provider": "dashscope", "restored_signs": 1},
            ),
        ),
        ErrorEvent(
            request_id=None,
            code="COMMAND_INVALID",
            message="Worker command is invalid.",
            retryable=False,
        ),
    ]


def test_frozen_event_fixture_covers_all_six_event_shapes() -> None:
    lines = FIXTURE.read_text(encoding="utf-8").splitlines()
    events = _events()

    assert len(lines) == len(events) == 6
    assert [serialize_worker_event(event) for event in events] == [
        json.loads(line) for line in lines
    ]
    for event in events:
        json.dumps(serialize_worker_event(event), ensure_ascii=False, allow_nan=False)


def test_event_payloads_copy_and_freeze_nested_json() -> None:
    details = {"nested": {"items": [1, 2]}}
    warning = WarningEvent(
        request_id=REQUEST_ID,
        code="NORMALIZED",
        message="Output was normalized.",
        details=details,
    )
    metadata = {"nested": {"items": [3, 4]}}
    result = WorkerRecognitionResult(
        markdown="# Result\n",
        source_type="image",
        profile="board",
        metadata=metadata,
    )

    details["nested"]["items"].append(99)
    metadata["nested"]["items"].append(99)

    assert warning.details["nested"]["items"] == (1, 2)
    assert result.metadata["nested"]["items"] == (3, 4)
    assert isinstance(warning.details, MappingProxyType)
    assert isinstance(result.metadata, MappingProxyType)
    with pytest.raises(FrozenInstanceError):
        warning.code = "CHANGED"  # type: ignore[misc]


def test_warning_and_error_details_redact_sensitive_keys_recursively() -> None:
    warning = WarningEvent(
        request_id=REQUEST_ID,
        code="SAFE_WARNING",
        message="A safe warning occurred.",
        details={"nested": {"api_key": "secret-sentinel"}},
    )
    error = ErrorEvent(
        request_id=REQUEST_ID,
        code="PROVIDER_TIMEOUT",
        message="Provider timed out.",
        retryable=True,
        details={"authorization": "secret-sentinel"},
    )

    encoded = json.dumps(
        [serialize_worker_event(warning), serialize_worker_event(error)],
        ensure_ascii=False,
    )
    assert "secret-sentinel" not in encoded
    assert encoded.count("[REDACTED]") == 2


def test_direct_result_adapter_preserves_phase1_values_without_mutation() -> None:
    metadata = {"provider": "dashscope", "nested": [1, 2]}
    direct = RecognitionResult(
        markdown="# Board\n",
        source_type="image",
        profile="board",
        hotwords=("gene",),
        warnings=("faint",),
        metadata=metadata,
    )
    worker = build_worker_recognition_result(direct)

    assert worker.markdown == direct.markdown
    assert worker.source_type == "image"
    assert worker.profile == "board"
    assert worker.output_uri is None
    assert worker.artifacts == ()
    assert worker.hotwords == ("gene",)
    assert worker.warnings == ("faint",)
    assert worker.metadata == direct.metadata


def test_direct_result_adapter_converts_absolute_output_path_to_file_uri(
    tmp_path,
) -> None:
    output = tmp_path / "中文 result.md"
    output.write_text("# Board\n", encoding="utf-8")
    direct = RecognitionResult(
        markdown="# Board\n",
        source_type="image",
        profile="board",
        output_path=output,
    )

    worker = build_worker_recognition_result(direct)

    assert worker.output_uri == output.resolve().as_uri()


def test_direct_result_adapter_fails_closed_for_untyped_assets(tmp_path) -> None:
    asset = tmp_path / "asset.bin"
    asset.write_bytes(b"asset")
    direct = RecognitionResult(
        markdown="# Board\n",
        source_type="image",
        profile="board",
        assets=(asset,),
    )

    with pytest.raises(ValueError, match="typed artifact metadata"):
        build_worker_recognition_result(direct)


def test_direct_result_adapter_rejects_missing_output_file(tmp_path) -> None:
    direct = RecognitionResult(
        markdown="# Board\n",
        source_type="image",
        profile="board",
        output_path=tmp_path / "missing.md",
    )

    with pytest.raises(ValueError, match="existing file"):
        build_worker_recognition_result(direct)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"stage": "", "completed": 0, "total": None, "unit": "image"},
        {"stage": "run", "completed": True, "total": None, "unit": "image"},
        {"stage": "run", "completed": -1, "total": None, "unit": "image"},
        {"stage": "run", "completed": 2, "total": 1, "unit": "image"},
        {"stage": "run", "completed": 0, "total": None, "unit": ""},
    ],
)
def test_progress_event_rejects_invalid_counters_and_labels(
    kwargs: dict[str, object],
) -> None:
    with pytest.raises((TypeError, ValueError)):
        ProgressEvent(request_id=REQUEST_ID, **kwargs)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "report",
    [
        {"name": "", "status": "available", "reason": "ready"},
        {"name": "image.board.png", "status": "ready", "reason": "ready"},
        {"name": "image.board.png", "status": "available", "reason": ""},
    ],
)
def test_capability_report_rejects_invalid_vocabulary(
    report: dict[str, object],
) -> None:
    with pytest.raises((TypeError, ValueError)):
        CapabilityReport(**report)  # type: ignore[arg-type]


def test_error_event_rejects_unknown_error_code() -> None:
    with pytest.raises(ValueError, match="error code"):
        ErrorEvent(
            request_id=None,
            code="SECRET_SENTINEL",
            message="Failure.",
            retryable=False,
        )


def test_artifact_requires_file_uri_and_mime_type() -> None:
    artifact = Artifact(
        kind="markdown",
        uri="file:///D:/Output/result.md",
        media_type="text/markdown",
    )
    assert artifact.kind == "markdown"

    with pytest.raises(ValueError, match="file URI"):
        Artifact(
            kind="markdown",
            uri="https://example.test/result.md",
            media_type="text/markdown",
        )
    with pytest.raises(ValueError, match="MIME"):
        Artifact(
            kind="markdown", uri="file:///D:/Output/result.md", media_type="markdown"
        )


def test_event_serializer_rejects_subclasses() -> None:
    @dataclass(frozen=True, slots=True, kw_only=True)
    class AcceptedSubclass(AcceptedEvent):
        pass

    with pytest.raises(TypeError, match="exact worker event"):
        serialize_worker_event(AcceptedSubclass(request_id=REQUEST_ID))
