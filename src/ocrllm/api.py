"""Public recognition entrypoints and input routing."""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from pathlib import Path

from .config import Config
from .errors import UnsupportedFormat
from .processors.board import recognize_board
from .result import RecognitionResult

BOARD_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp",
    ".heic",
    ".heif",
    ".tif",
    ".tiff",
}


def recognize(
    source: str | Path | Sequence[str | Path],
    *,
    config: Config | None = None,
) -> RecognitionResult:
    """Recognize one source or a same-type source group.

    Phase 0 intentionally supports board/image inputs only. Other source types
    stay out of the import contract until their library behavior is proven.
    """
    paths = _coerce_source_paths(source)
    source_type = _detect_source_type(paths)
    if source_type == "board":
        return recognize_board(paths, config or Config())
    raise UnsupportedFormat(f"{source_type!r} is not supported by the extracted library yet")


def recognize_batch(
    sources: Iterable[str | Path | Sequence[str | Path]],
    *,
    config: Config | None = None,
) -> list[RecognitionResult]:
    """Recognize independent sources and return one result per source."""
    cfg = config or Config()
    return [recognize(source, config=cfg) for source in sources]


def _coerce_source_paths(source: str | Path | Sequence[str | Path]) -> tuple[Path, ...]:
    if isinstance(source, (str, Path)):
        paths = (Path(source),)
    else:
        paths = tuple(Path(item) for item in source)
    if not paths:
        raise UnsupportedFormat("recognize() requires at least one input path")
    return paths


def _detect_source_type(paths: Sequence[Path]) -> str:
    suffixes = {path.suffix.lower() for path in paths}
    if suffixes <= BOARD_EXTENSIONS:
        return "board"
    if len(suffixes) > 1:
        raise UnsupportedFormat(f"mixed source types are not supported in one recognize() call: {sorted(suffixes)}")
    suffix = next(iter(suffixes))
    if not suffix:
        raise UnsupportedFormat("input path has no file extension")
    raise UnsupportedFormat(f"unsupported source extension: {suffix}")
