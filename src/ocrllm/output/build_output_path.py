"""Build and preflight the optional Markdown output path."""

from __future__ import annotations

import os
from collections.abc import Sequence
from pathlib import Path

from ..config import Config
from ..errors import OutputError, OutputExists
from .normalize_output_stem import normalize_output_stem


def build_output_path(
    source_paths: Sequence[Path],
    *,
    profile: str,
    config: Config,
) -> Path | None:
    """Return a deterministic collision-checked path, or None for memory-only."""
    output_dir = config.output_directory()
    if output_dir is None:
        return None
    try:
        if output_dir.exists() and not output_dir.is_dir():
            raise OutputError(
                "Config.output_dir must identify a directory.",
                code="OUTPUT_PATH_INVALID",
            )
        output_dir.mkdir(parents=True, exist_ok=True)
    except OutputError:
        raise
    except (OSError, ValueError) as error:
        raise OutputError(
            "Config.output_dir could not be created or opened.",
            code="OUTPUT_PATH_INVALID",
        ) from error

    first_stem = normalize_output_stem(source_paths[0].stem)
    filename_stem = (
        first_stem
        if len(source_paths) == 1
        else f"{first_stem}_plus_{len(source_paths) - 1}"
    )
    output_path = output_dir / f"{filename_stem}_{profile}.md"
    target_exists = os.path.lexists(output_path)
    if target_exists and not output_path.is_file():
        raise OutputError(
            "The requested Markdown output path is not a regular file.",
            code="OUTPUT_PATH_INVALID",
        )
    if target_exists and not config.overwrite and not config.resume:
        raise OutputExists("The requested Markdown output already exists.")
    return output_path
