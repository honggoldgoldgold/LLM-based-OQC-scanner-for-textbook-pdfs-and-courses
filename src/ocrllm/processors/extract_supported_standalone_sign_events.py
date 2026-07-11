"""Extract only exact supported records from one untrusted scout response."""

from __future__ import annotations

from .parse_standalone_sign_ledger import (
    StandaloneSignEvent,
    parse_standalone_sign_ledger,
)


_MAX_SCOUT_RESPONSE_LINES = 256


def extract_supported_standalone_sign_events(
    response: str,
) -> tuple[StandaloneSignEvent, ...]:
    """Return allowlisted exact records while discarding unrelated lines."""

    if type(response) is not str or not response.strip():
        raise ValueError("standalone-sign response must be nonempty plain text")
    if response == "NONE":
        return ()

    lines = tuple(line for line in response.splitlines() if line.strip())
    if not lines or len(lines) > _MAX_SCOUT_RESPONSE_LINES:
        raise ValueError("standalone-sign response has an invalid line count")

    result = []
    for line in lines:
        try:
            events = parse_standalone_sign_ledger(line)
        except ValueError:
            continue
        result.extend(events)
    if not result:
        raise ValueError("standalone-sign response has no supported exact record")
    return tuple(dict.fromkeys(result))
