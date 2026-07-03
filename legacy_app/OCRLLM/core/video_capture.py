"""Shared OpenCV video capture backend selection."""

from __future__ import annotations

import logging
import os
from collections.abc import Iterable

import cv2

logger = logging.getLogger(__name__)

_BACKEND_ENV = "OCRLLM_VIDEO_CAPTURE_BACKENDS"


def _default_backend_names() -> tuple[str, ...]:
    if os.name == "nt":
        return ("FFMPEG", "MSMF", "DSHOW", "ANY")
    return ("ANY", "FFMPEG")


def _configured_backend_names() -> tuple[str, ...]:
    raw = os.environ.get(_BACKEND_ENV, "")
    if not raw.strip():
        return _default_backend_names()
    names = tuple(part.strip().upper() for part in raw.split(",") if part.strip())
    return names or _default_backend_names()


def _backend_id(name: str):
    attr = "CAP_ANY" if name == "ANY" else f"CAP_{name}"
    return getattr(cv2, attr, None)


def iter_video_capture_backends(names: Iterable[str] | None = None) -> tuple[tuple[str, int], ...]:
    backends: list[tuple[str, int]] = []
    seen: set[int] = set()
    for name in names or _configured_backend_names():
        backend_id = _backend_id(name)
        if backend_id is None or backend_id in seen:
            continue
        seen.add(backend_id)
        backends.append((name, backend_id))
    return tuple(backends)


def open_video_capture(video_path: str, *, backend_names: Iterable[str] | None = None):
    """Open a video file with platform-aware backend fallbacks."""
    last_failed = None
    for backend_name, backend_id in iter_video_capture_backends(backend_names):
        cap = cv2.VideoCapture(video_path, backend_id)
        if cap.isOpened():
            if last_failed is not None:
                last_failed.release()
            logger.info("[VIDEO] VideoCapture backend=%s", backend_name)
            return cap
        if last_failed is not None:
            last_failed.release()
        last_failed = cap

    return last_failed if last_failed is not None else cv2.VideoCapture(video_path)
