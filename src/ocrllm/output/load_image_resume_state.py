"""Load one optional bounded sibling image resume state file."""

from __future__ import annotations

import os
from pathlib import Path

from ..errors import ResumeStateError
from ..image_resume_state import ImageResumeState
from ..parse_image_resume_state import parse_image_resume_state


_MAX_STATE_BYTES = 16 * 1024 * 1024


def load_image_resume_state(state_path: Path) -> ImageResumeState | None:
    """Return strict state, None when absent, or a redacted typed failure."""
    try:
        if not os.path.lexists(state_path):
            return None
        if not state_path.is_file():
            raise ResumeStateError(
                "The image resume state path is not a regular file.",
                code="RESUME_STATE_INVALID",
            ) from None
        if state_path.stat().st_size > _MAX_STATE_BYTES:
            raise ResumeStateError(
                "The image resume state exceeds the safety limit.",
                code="RESUME_STATE_INVALID",
            ) from None
        raw = state_path.read_bytes()
    except ResumeStateError:
        raise
    except (OSError, ValueError):
        raise ResumeStateError(
            "The image resume state could not be read safely.",
            code="RESUME_STATE_INVALID",
        ) from None
    return parse_image_resume_state(raw)
