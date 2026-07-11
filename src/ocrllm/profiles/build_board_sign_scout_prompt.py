"""Build the strict standalone-sign ledger prompt."""

from __future__ import annotations


def build_board_sign_scout_prompt() -> str:
    """Return the fixed, non-prose sign-ledger request."""

    return (
        "Inspect the supplied source images only for standalone conventional textual signs "
        "or operators that occupy their own visible text position. If there is no such sign, "
        "return exactly NONE. Otherwise return one plain-text record per visible occurrence "
        "using exactly SIGN | BEFORE | AFTER, with no header. SIGN must be the exact visible "
        "sign. BEFORE and AFTER must be nearest literally visible text fragments, at most "
        "five words each; use NONE only if no neighbor exists. Do not transcribe other content. "
        "Never treat spatial relationships, separate text lines, bullets, list markers, borders, "
        "rounded panels, box outlines, underlines, table or grid lines, decorative strokes, "
        "hatch, fill, shading, or texture as signs. Never report punctuation or a hyphen inside "
        "a word, identifier, date, or number. Do not output headings, fences, captions, or "
        "explanations. SIGN must be exactly one of +, -, =, <=, >=, ≤, ≥. Never report "
        "directional or diagram arrows. Do not report any other punctuation such as colon, "
        "slash, apostrophe, period, or comma."
    )
