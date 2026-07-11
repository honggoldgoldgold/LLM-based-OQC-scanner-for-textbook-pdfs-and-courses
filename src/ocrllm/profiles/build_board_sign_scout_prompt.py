"""Build the strict standalone-sign ledger prompt."""

from __future__ import annotations


def build_board_sign_scout_prompt() -> str:
    """Return the fixed, non-prose sign-ledger request."""

    return (
        "Inspect the supplied board images only for standalone conventional textual signs "
        "or operators that are spatially separate from words and drawing strokes. Return "
        "one plain-text record per visible occurrence using exactly this format: "
        "SIGN | BEFORE | AFTER. SIGN must be the exact visible sign. BEFORE and AFTER must "
        "be the nearest literally visible text fragments, at most five words each; use NONE "
        "only if no neighbor exists. Do not transcribe other content. Do not output headings, "
        "bullets, fences, captions, explanations, Markdown separators, hatch marks, fill, "
        "shading, or texture."
    )
