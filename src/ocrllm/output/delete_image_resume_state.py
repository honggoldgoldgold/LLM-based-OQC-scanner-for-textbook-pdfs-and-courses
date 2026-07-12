"""Best-effort cleanup for validated image resume state after publication."""

from __future__ import annotations

import atexit
from pathlib import Path


def delete_image_resume_state(state_path: Path) -> None:
    """Delete completed state or register safe process-exit cleanup."""
    try:
        state_path.unlink(missing_ok=True)
    except (OSError, ValueError):
        atexit.register(_delete_at_exit, state_path)


def _delete_at_exit(state_path: Path) -> None:
    try:
        state_path.unlink(missing_ok=True)
    except (OSError, ValueError):
        pass
