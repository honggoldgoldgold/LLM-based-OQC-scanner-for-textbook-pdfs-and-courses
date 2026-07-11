"""Parse one strict, untrusted standalone-sign scout ledger."""

from __future__ import annotations

import re
from dataclasses import dataclass


_LEDGER_LINE = re.compile(
    r"^(?P<sign>[^|\r\n]{1,8}) \| "
    r"(?P<before>[^|\r\n]{1,120}) \| "
    r"(?P<after>[^|\r\n]{1,120})$"
)
SUPPORTED_STANDALONE_SIGNS = frozenset(
    {"+", "-", "=", "<=", ">=", "≤", "≥", "→", "←", "↑", "↓", "↔", "⇒", "⇐", "⇔"}
)
_MAX_LEDGER_EVENTS = 256


@dataclass(frozen=True, slots=True)
class StandaloneSignEvent:
    """One exact sign plus normalized neighboring visible-text anchors."""

    sign: str
    previous: str
    following: str


def parse_standalone_sign_ledger(ledger: str) -> tuple[StandaloneSignEvent, ...]:
    """Return strict events or reject the entire untrusted ledger."""

    if type(ledger) is not str or not ledger.strip():
        raise ValueError("standalone-sign ledger must be nonempty plain text")
    if ledger == "NONE":
        return ()
    lines = tuple(line for line in ledger.splitlines() if line.strip())
    if not lines or len(lines) > _MAX_LEDGER_EVENTS:
        raise ValueError("standalone-sign ledger has an invalid event count")

    result = []
    for line in lines:
        match = _LEDGER_LINE.fullmatch(line)
        if match is None:
            raise ValueError("standalone-sign ledger line violates the strict format")
        sign = match.group("sign")
        if sign not in SUPPORTED_STANDALONE_SIGNS:
            raise ValueError("standalone-sign ledger contains an unsupported sign")
        previous = _parse_anchor(match.group("before"))
        following = _parse_anchor(match.group("after"))
        if not previous and not following:
            raise ValueError("standalone-sign ledger event has no visible neighbor")
        result.append(StandaloneSignEvent(sign, previous, following))
    return tuple(result)


def _parse_anchor(value: str) -> str:
    if value == "NONE":
        return ""
    if value != value.strip() or len(value.split()) > 5:
        raise ValueError("standalone-sign ledger neighbor violates the word bound")
    normalized = "".join(
        character for character in value.casefold() if character.isalnum()
    )
    if not normalized:
        raise ValueError("standalone-sign ledger neighbor has no text anchor")
    return normalized
