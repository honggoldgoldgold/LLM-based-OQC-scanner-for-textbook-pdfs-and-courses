"""Validate an absolute RFC 8089-style file URI."""

from __future__ import annotations

import re
from urllib.parse import urlsplit


_INVALID_PERCENT_ESCAPE = re.compile(r"%(?![0-9A-Fa-f]{2})")


def validate_absolute_file_uri(uri: object, *, field_name: str) -> str:
    """Return an absolute file URI without exposing its value in failures."""

    if (
        not isinstance(uri, str)
        or not uri
        or any(ord(character) <= 0x20 or ord(character) == 0x7F for character in uri)
        or _INVALID_PERCENT_ESCAPE.search(uri) is not None
    ):
        raise TypeError(f"{field_name} must be an absolute file URI")
    try:
        parsed = urlsplit(uri)
        port = parsed.port
    except (TypeError, ValueError):
        raise ValueError(f"{field_name} must be an absolute file URI") from None
    if (
        parsed.scheme != "file"
        or parsed.query
        or parsed.fragment
        or not parsed.path.startswith("/")
        or parsed.path == "/"
        or "\\" in parsed.path
        or parsed.username is not None
        or parsed.password is not None
        or port is not None
    ):
        raise ValueError(f"{field_name} must be an absolute file URI")
    return uri
