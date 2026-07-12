"""Validated backend-neutral lines from one RapidOCR image result."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RapidOCRImageResult:
    lines: tuple[str, ...]
    confidences: tuple[float, ...]
    detected_line_count: int
