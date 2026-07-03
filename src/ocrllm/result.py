"""Recognition result data returned to library callers."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class RecognitionResult:
    """Structured output from one recognition call."""

    markdown: str
    source_type: str
    output_path: Path | None = None
    assets: tuple[Path, ...] = ()
    hotwords: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)
