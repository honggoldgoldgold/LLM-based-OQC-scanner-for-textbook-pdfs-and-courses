"""Normalize one source stem for a portable output filename."""

from __future__ import annotations

import unicodedata


WINDOWS_FORBIDDEN = frozenset('<>:"/\\|?*')


def normalize_output_stem(stem: str) -> str:
    """Return a Windows-safe NFC filename stem capped at 96 code points."""
    normalized = unicodedata.normalize("NFC", stem)
    safe = "".join(
        "_"
        if ord(character) < 32 or ord(character) == 127 or character in WINDOWS_FORBIDDEN
        else character
        for character in normalized
    )
    safe = safe.rstrip(" .")[:96].rstrip(" .")
    return safe or "source"
