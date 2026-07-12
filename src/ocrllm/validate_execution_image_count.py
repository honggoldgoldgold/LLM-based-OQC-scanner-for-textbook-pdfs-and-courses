"""Reject image groups that exceed caller execution policy."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

from .errors import InvalidSource
from .recognition_execution_policy import RecognitionExecutionPolicy


def validate_execution_image_count(
    source_paths: Sequence[Path],
    *,
    execution: RecognitionExecutionPolicy,
) -> None:
    """Fail before file access when a request exceeds its configured image cap."""
    image_count = len(source_paths)
    maximum_image_count = execution.maximum_images_per_request
    if image_count > maximum_image_count:
        raise InvalidSource(
            "The image group exceeds the configured per-request image limit.",
            code="SOURCE_TOO_LARGE",
            details={
                "image_count": image_count,
                "maximum_image_count": maximum_image_count,
                "limit_source": "recognition_execution_policy",
            },
        ) from None
