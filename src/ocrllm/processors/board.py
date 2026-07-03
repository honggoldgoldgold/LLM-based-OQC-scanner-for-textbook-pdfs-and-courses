"""Board image recognition using an injected provider."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

from ..config import Config
from ..errors import ConfigError
from ..result import RecognitionResult

DEFAULT_BOARD_PROMPT = "Recognize the board or screenshot content as structured Markdown."


def recognize_board(image_paths: Sequence[Path], config: Config) -> RecognitionResult:
    """Recognize one board-image group and optionally write Markdown output."""
    provider = config.provider
    if provider is None or not hasattr(provider, "recognize_images"):
        raise ConfigError("Config.provider must implement recognize_images(image_paths, *, prompt, config)")

    normalized_paths = tuple(Path(path) for path in image_paths)
    markdown = provider.recognize_images(normalized_paths, prompt=DEFAULT_BOARD_PROMPT, config=config)
    if not isinstance(markdown, str):
        raise ConfigError("provider.recognize_images() must return Markdown text")

    output_path = _write_output_if_requested(normalized_paths, markdown, config)
    return RecognitionResult(
        markdown=markdown,
        source_type="board",
        output_path=output_path,
        metadata={"image_count": len(normalized_paths), "model": config.model},
    )


def _write_output_if_requested(image_paths: Sequence[Path], markdown: str, config: Config) -> Path | None:
    output_dir = config.output_directory()
    if output_dir is None:
        return None
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = image_paths[0].stem if len(image_paths) == 1 else f"board_{len(image_paths)}_images"
    output_path = output_dir / f"{stem}_board.md"
    output_path.write_text(markdown, encoding="utf-8")
    return output_path
