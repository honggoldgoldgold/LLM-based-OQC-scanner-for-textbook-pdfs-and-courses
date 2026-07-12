"""Validate one bounded BCP-47 language tag."""

from __future__ import annotations

import re


_LANGUAGE_TAG = re.compile(r"^(?:[A-Za-z]{2,8}|x)(?:-[A-Za-z0-9]{1,8})*$")


def validate_language_tag(value: object, *, field_name: str) -> str:
    """Return a structurally valid BCP-47 tag or raise a redacted error."""

    if not isinstance(value, str) or _LANGUAGE_TAG.fullmatch(value) is None:
        raise ValueError(f"{field_name} must contain BCP-47 language tags")
    return value
