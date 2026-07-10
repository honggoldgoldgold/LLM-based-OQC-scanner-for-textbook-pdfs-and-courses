"""Build and validate one public recognition result."""

from __future__ import annotations

from pathlib import Path

from .errors import OutputError
from .processor_output import ProcessorOutput
from .result import RecognitionResult


def build_recognition_result(
    processor_output: ProcessorOutput,
    *,
    output_path: Path | None,
) -> RecognitionResult:
    """Combine processor content with final artifacts that really exist."""
    if output_path is not None and not output_path.is_file():
        raise OutputError(
            "The requested Markdown output was not created.",
            code="OUTPUT_WRITE_FAILED",
        )

    missing_assets = [path for path in processor_output.assets if not path.is_file()]
    if missing_assets:
        raise OutputError(
            "A processor reported a final artifact that does not exist.",
            code="OUTPUT_WRITE_FAILED",
        )

    return RecognitionResult(
        markdown=processor_output.markdown,
        source_type=processor_output.media_type,
        profile=processor_output.profile,
        status=processor_output.status,
        output_path=output_path,
        assets=processor_output.assets,
        hotwords=processor_output.hotwords,
        warnings=processor_output.warnings,
        metadata=processor_output.metadata,
    )
