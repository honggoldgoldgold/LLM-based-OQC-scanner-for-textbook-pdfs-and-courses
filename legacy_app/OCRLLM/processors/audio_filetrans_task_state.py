"""Persist in-flight DashScope filetrans task ids for audio resume."""

from __future__ import annotations

import json
import hashlib
import os
import time
from pathlib import Path
from typing import Any


_STATE_SUFFIX = ".filetrans_task.json"
_MAX_STATE_AGE_SECONDS = 24 * 60 * 60
_MAX_COMPATIBLE_STATE_PATH_CHARS = 240


def filetrans_task_state_path(output_path: str) -> Path:
    """Return the sidecar path for an audio Markdown output."""
    output = Path(output_path)
    candidate = output.with_name(output.name + _STATE_SUFFIX)
    if _compatible_temp_path(candidate):
        return candidate

    digest = hashlib.sha1(str(output).encode("utf-8", errors="surrogatepass")).hexdigest()[:12]
    prefix = output.stem[:48].rstrip(" .") or "audio"
    shortened = output.with_name(f"{prefix}.{digest}{_STATE_SUFFIX}")
    if _compatible_temp_path(shortened):
        return shortened
    return output.with_name(f"audio.{digest}{_STATE_SUFFIX}")


def load_filetrans_task_id(output_path: str, *, model: str, audio_path: str) -> str | None:
    """Load a reusable task id when the sidecar still matches this input."""
    state_path = filetrans_task_state_path(output_path)
    try:
        raw = json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None

    if not isinstance(raw, dict):
        return None
    if raw.get("model") != model:
        return None
    if raw.get("audio_fingerprint") != _audio_fingerprint(audio_path):
        return None

    submitted_at = float(raw.get("submitted_at") or 0.0)
    if submitted_at and time.time() - submitted_at > _MAX_STATE_AGE_SECONDS:
        clear_filetrans_task_state(output_path)
        return None

    task_id = str(raw.get("task_id") or "").strip()
    return task_id or None


def save_filetrans_task_state(
    output_path: str,
    *,
    task_id: str,
    model: str,
    audio_path: str,
    file_url: str,
) -> None:
    """Save the provider task id before waiting for async transcription."""
    state_path = filetrans_task_state_path(output_path)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "task_id": task_id,
        "model": model,
        "audio_fingerprint": _audio_fingerprint(audio_path),
        "file_url_kind": "remote" if _is_remote(file_url) else "local",
        "submitted_at": time.time(),
    }
    temp_path = state_path.with_name(state_path.name + ".tmp")
    temp_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(temp_path, state_path)


def clear_filetrans_task_state(output_path: str) -> None:
    """Remove the filetrans task sidecar if it exists."""
    try:
        filetrans_task_state_path(output_path).unlink()
    except FileNotFoundError:
        pass


def _audio_fingerprint(audio_path: str) -> dict[str, Any]:
    if _is_remote(audio_path):
        return {"kind": "remote", "value": audio_path}

    path = Path(audio_path)
    try:
        stat = path.stat()
    except OSError:
        return {"kind": "local", "path": str(path.resolve()), "size": -1, "mtime_ns": -1}
    return {
        "kind": "local",
        "path": str(path.resolve()),
        "size": stat.st_size,
        "mtime_ns": stat.st_mtime_ns,
    }


def _is_remote(path: str) -> bool:
    lowered = str(path).lower()
    return lowered.startswith(("http://", "https://", "oss://"))


def _compatible_temp_path(state_path: Path) -> bool:
    temp_path = state_path.with_name(state_path.name + ".tmp")
    absolute = temp_path.resolve(strict=False)
    return len(str(absolute)) <= _MAX_COMPATIBLE_STATE_PATH_CHARS
