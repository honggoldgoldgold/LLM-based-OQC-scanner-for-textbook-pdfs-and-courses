"""Restore only standalone signs agreed by two untrusted scout outputs."""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass


_STANDALONE_SIGN = re.compile(r"^(?:\+|-|=|<=|>=|≤|≥|→|←|↑|↓|↔|⇒|⇐|⇔)+$")
_MAX_SCOUT_SIGN_EVENTS = 256


@dataclass(frozen=True, slots=True)
class RestoredStandaloneSigns:
    """One base transcript plus its bounded deterministic restoration count."""

    markdown: str
    restored_count: int


def restore_quorum_standalone_signs(
    base_markdown: str,
    first_scout_markdown: str,
    second_scout_markdown: str,
) -> RestoredStandaloneSigns:
    """Add only sign events shared by both scouts between matching anchors."""

    for value, name in (
        (base_markdown, "base_markdown"),
        (first_scout_markdown, "first_scout_markdown"),
        (second_scout_markdown, "second_scout_markdown"),
    ):
        if type(value) is not str or not value.strip():
            raise ValueError(f"{name} must be nonempty plain text")

    quorum_events = _quorum_sign_events(
        first_scout_markdown,
        second_scout_markdown,
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
    )


def _sign_events(markdown: str) -> tuple[tuple[str, str, str], ...]:
    lines = tuple(line.strip() for line in markdown.splitlines())
    result = []
    for index, line in enumerate(lines):
        if _STANDALONE_SIGN.fullmatch(line) is None:
            continue
        previous = _nearest_anchor(lines, range(index - 1, -1, -1))
        following = _nearest_anchor(lines, range(index + 1, len(lines)))
        if previous and following:
            result.append((line, previous, following))
    return tuple(result)


def _nearest_anchor(lines: tuple[str, ...], indexes: range) -> str:
    return next(
        (
            _normalize_anchor(lines[index])
            for index in indexes
            if lines[index] and _STANDALONE_SIGN.fullmatch(lines[index]) is None
        ),
        "",
    )


def _quorum_sign_events(
    first_scout: str,
    second_scout: str,
) -> tuple[tuple[str, str, str], ...]:
    first_events = _sign_events(first_scout)
    second_events = _sign_events(second_scout)
    used: set[int] = set()
    result = []
    for sign, previous, following in first_events:
        for index, (other_sign, other_previous, other_following) in enumerate(
            second_events
        ):
            if index in used or sign != other_sign:
                continue
            previous_agrees = _anchors_match(previous, other_previous)
            following_agrees = _anchors_match(following, other_following)
            if not (previous_agrees or following_agrees):
                continue
            used.add(index)
            result.append(
                (
                    sign,
                    previous if previous_agrees else "",
                    following if following_agrees else "",
                )
            )
            break
    return tuple(result)


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
        if _contains_sign(lines, sign, previous_index + 1, following_index):
            return None
        return following_index
    if following:
        following_index = _find_anchor(lines, following, search_from)
        if following_index is None:
            return None
        window_start = max(search_from, following_index - 4)
        if _contains_sign(lines, sign, window_start, following_index):
            return None
        return following_index
    if previous:
        previous_index = _find_anchor(lines, previous, search_from)
        if previous_index is None:
            return None
        window_end = min(len(lines), previous_index + 5)
        if _contains_sign(lines, sign, previous_index + 1, window_end):
            return None
        return previous_index + 1
    return None


def _count_isolated_tokens(lines: list[str], sign: str) -> int:
    return sum(token == sign for line in lines for token in line.split())


def _contains_sign(lines: list[str], sign: str, start: int, stop: int) -> bool:
    return any(sign in line.split() for line in lines[start:stop])


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
