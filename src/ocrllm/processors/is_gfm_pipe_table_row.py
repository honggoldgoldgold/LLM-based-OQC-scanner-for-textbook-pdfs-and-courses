"""Identify one conservative GFM pipe-table row boundary."""

from __future__ import annotations


def is_gfm_pipe_table_row(line: str) -> bool:
    """Return whether a line has a protected outer-pipe table shape."""

    if type(line) is not str:
        raise ValueError("line must be plain text")
    stripped = line.strip()
    return len(stripped) >= 2 and stripped.startswith("|") and stripped.endswith("|")
