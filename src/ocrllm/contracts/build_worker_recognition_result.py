"""Adapt the proven direct-Python result to the worker wire payload."""

from __future__ import annotations

from ocrllm.result import RecognitionResult

from .worker_recognition_result import WorkerRecognitionResult


def build_worker_recognition_result(
    result: RecognitionResult,
) -> WorkerRecognitionResult:
    """Build a wire payload without guessing metadata for untyped assets."""

    if type(result) is not RecognitionResult:
        raise TypeError("result must be an exact direct RecognitionResult")
    if result.assets:
        raise ValueError(
            "direct result assets require typed artifact metadata before worker use"
        )
    output_uri = None
    if result.output_path is not None:
        output_path = result.output_path.resolve()
        if not output_path.is_file():
            raise ValueError("direct result output_path must name an existing file")
        output_uri = output_path.as_uri()
    return WorkerRecognitionResult(
        markdown=result.markdown,
        source_type=result.source_type,
        profile=result.profile,
        status=result.status,
        output_uri=output_uri,
        artifacts=(),
        hotwords=result.hotwords,
        warnings=result.warnings,
        metadata=result.metadata,
    )
