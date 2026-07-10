"""Build the dependency-free board-recognition prompt."""

from __future__ import annotations

from collections.abc import Sequence


def build_board_prompt(
    input_languages: Sequence[str] = (),
    output_language: str | None = None,
) -> str:
    """Return the board profile prompt for validated language preferences."""
    prompt = (
        "Recognize the board or screenshot as structured Markdown. "
        "Preserve formulas, tables, labels, and reading order; do not invent missing content."
    )
    if input_languages:
        prompt += f" Expected input languages: {', '.join(input_languages)}."
    if output_language:
        prompt += f" Write explanatory text in {output_language}."
    return prompt
