"""Small immutable configuration object for library callers."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class Config:
    """Runtime options for OCRLLM library calls."""

    api_key: str | None = None
    model: str = "qwen-vl-max"
    output_dir: str | Path | None = None
    parallel_requests: int = 8
    provider: Any | None = None

    def output_directory(self) -> Path | None:
        """Return the configured output directory, or None for in-memory mode."""
        if self.output_dir is None:
            return None
        return Path(self.output_dir)
