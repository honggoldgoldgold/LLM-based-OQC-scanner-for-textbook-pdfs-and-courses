"""Restore only standalone signs meeting quorum across untrusted scouts."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from .parse_standalone_sign_ledger import (
    SUPPORTED_STANDALONE_SIGNS,
    StandaloneSignEvent,
    parse_standalone_sign_ledger,
)

_MAX_SCOUT_SIGN_EVENTS = 256


@dataclass(frozen=True, slots=True)
class RestoredStandaloneSigns:
    """One base transcript plus its bounded deterministic restoration count."""

    markdown: str
    restored_count: int
    abstained_scout_count: int


def restore_quorum_standalone_signs(
    base_markdown: str,
    scout_markdowns: tuple[str, ...],
    *,
    minimum_agreement: int = 2,
) -> RestoredStandaloneSigns:
    """Add only sign events meeting quorum between matching anchors."""

    if type(base_markdown) is not str or not base_markdown.strip():
        raise ValueError("base_markdown must be nonempty plain text")
    if (
        type(scout_markdowns) is not tuple
        or not 2 <= len(scout_markdowns) <= 8
        or any(type(value) is not str or not value.strip() for value in scout_markdowns)
    ):
        raise ValueError("scout_markdowns must contain 2 to 8 nonempty plain texts")
    if (
        type(minimum_agreement) is not int
        or not 2 <= minimum_agreement <= len(scout_markdowns)
    ):
        raise ValueError("minimum_agreement must be between 2 and the scout count")

    quorum_events, abstained_scout_count = _quorum_sign_events(
        scout_markdowns,
        minimum_agreement=minimum_agreement,
    )
    if len(quorum_events) > _MAX_SCOUT_SIGN_EVENTS:
        raise ValueError("scout sign-event quorum exceeds the safe bound")

    lines = base_markdown.splitlines()
    insertions: list[tuple[int, str]] = []
    quorum_counts = Counter(event[0] for event in quorum_events)
    remaining = {
        sign: max(0, count - _count_isolated_tokens(lines, sign))
        for sign, count in quorum_counts.items()
    }
    search_from = 0
    for sign, previous, following in quorum_events:
        if remaining[sign] <= 0:
            continue
        insertion_index = _find_safe_insertion_index(
            lines,
            sign=sign,
            previous=previous,
            following=following,
            search_from=search_from,
        )
        if insertion_index is None:
            continue
        insertions.append((insertion_index, sign))
        remaining[sign] -= 1
        search_from = insertion_index

    for index, sign in sorted(insertions, reverse=True):
        lines[index:index] = [sign]
    suffix = "\n" if base_markdown.endswith("\n") else ""
    return RestoredStandaloneSigns(
        markdown="\n".join(lines) + suffix,
        restored_count=len(insertions),
        abstained_scout_count=abstained_scout_count,
    )


def _quorum_sign_events(
    scout_markdowns: tuple[str, ...],
    *,
    minimum_agreement: int,
) -> tuple[tuple[tuple[str, str, str], ...], int]:
    clusters: list[list[tuple[int, tuple[str, str, str]]]] = []
    abstained_scout_count = 0
    for scout_index, markdown in enumerate(scout_markdowns):
        try:
            parsed_events = parse_standalone_sign_ledger(markdown)
        except ValueError:
            abstained_scout_count += 1
            continue
        for parsed_event in parsed_events:
            event = _event_tuple(parsed_event)
            cluster = next(
                (
                    candidate
                    for candidate in clusters
                    if all(index != scout_index for index, _ in candidate)
                    and any(_events_match(event, value) for _, value in candidate)
                ),
                None,
            )
            if cluster is None:
                clusters.append([(scout_index, event)])
            else:
                cluster.append((scout_index, event))

    result = []
    for cluster in clusters:
        if len(cluster) < minimum_agreement:
            continue
        events = tuple(event for _, event in cluster)
        previous = _shared_anchor(events, anchor_index=1, minimum_agreement=minimum_agreement)
        following = _shared_anchor(events, anchor_index=2, minimum_agreement=minimum_agreement)
        if previous or following:
            result.append((events[0][0], previous, following))
    return tuple(result), abstained_scout_count


def _events_match(
    first: tuple[str, str, str],
    second: tuple[str, str, str],
) -> bool:
    return first[0] == second[0] and (
        _anchors_match(first[1], second[1])
        or _anchors_match(first[2], second[2])
    )


def _shared_anchor(
    events: tuple[tuple[str, str, str], ...],
    *,
    anchor_index: int,
    minimum_agreement: int,
) -> str:
    candidates = tuple(dict.fromkeys(event[anchor_index] for event in events))
    scored = tuple(
        (
            sum(_anchors_match(candidate, event[anchor_index]) for event in events),
            len(candidate),
            candidate,
        )
        for candidate in candidates
        if candidate
    )
    if not scored:
        return ""
    count, _, anchor = max(scored)
    return anchor if count >= minimum_agreement else ""


def _event_tuple(event: StandaloneSignEvent) -> tuple[str, str, str]:
    return event.sign, event.previous, event.following


def _find_safe_insertion_index(
    lines: list[str],
    *,
    sign: str,
    previous: str,
    following: str,
    search_from: int,
) -> int | None:
    if previous and following:
        previous_index = _find_anchor(lines, previous, search_from)
        if previous_index is None:
            return None
        following_index = _find_anchor(lines, following, previous_index + 1)
        if following_index is None:
            return None
        if _contains_any_supported_sign(lines, previous_index + 1, following_index):
            return None
        return following_index
    if following:
        following_index = _find_anchor(lines, following, search_from)
        if following_index is None:
            return None
        window_start = max(search_from, following_index - 4)
        if _contains_any_supported_sign(lines, window_start, following_index):
            return None
        return following_index
    if previous:
        previous_index = _find_anchor(lines, previous, search_from)
        if previous_index is None:
            return None
        window_end = min(len(lines), previous_index + 5)
        if _contains_any_supported_sign(lines, previous_index + 1, window_end):
            return None
        return previous_index + 1
    return None


def _count_isolated_tokens(lines: list[str], sign: str) -> int:
    return sum(token == sign for line in lines for token in line.split())


def _contains_any_supported_sign(lines: list[str], start: int, stop: int) -> bool:
    return any(
        token in SUPPORTED_STANDALONE_SIGNS
        for line in lines[start:stop]
        for token in line.split()
    )


def _find_anchor(lines: list[str], anchor: str, start: int) -> int | None:
    return next(
        (
            index
            for index in range(start, len(lines))
            if _anchors_match(_normalize_anchor(lines[index]), anchor)
        ),
        None,
    )


def _anchors_match(first: str, second: str) -> bool:
    return bool(first and second and (first in second or second in first))


def _normalize_anchor(value: str) -> str:
    return "".join(character for character in value.casefold() if character.isalnum())
