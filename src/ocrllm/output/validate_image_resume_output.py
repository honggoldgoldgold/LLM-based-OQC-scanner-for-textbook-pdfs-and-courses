"""Verify a final Markdown artifact against completed image resume state."""

from __future__ import annotations

import hashlib
from pathlib import Path

from ..errors import ResumeStateError
from ..image_resume_state import ImageResumeState


_CHUNK_BYTES = 1024 * 1024


def validate_image_resume_output(
    output_path: Path,
    state: ImageResumeState,
) -> None:
    """Fail closed when the durable final artifact was edited or replaced."""
    try:
        digest = hashlib.sha256()
        with output_path.open("rb") as stream:
            while chunk := stream.read(_CHUNK_BYTES):
                digest.update(chunk)
    except (OSError, ValueError):
        raise ResumeStateError(
            "The final image output could not be validated for resume.",
            code="RESUME_STATE_MISMATCH",
        ) from None
    if digest.hexdigest() != state.final_markdown_sha256:
        raise ResumeStateError(
            "The final image output does not match the resume state.",
            code="RESUME_STATE_MISMATCH",
        ) from None
