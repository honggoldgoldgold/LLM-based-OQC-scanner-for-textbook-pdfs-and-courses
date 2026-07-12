"""Immutable identity for one ordered resume source."""

from __future__ import annotations

import re
from dataclasses import dataclass
from urllib.parse import urlsplit


_SHA256 = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True, slots=True, kw_only=True)
class SourceFingerprint:
    """Record one source location, byte count, and content digest."""

    uri: str
    byte_size: int
    sha256: str

    def __post_init__(self) -> None:
        try:
            parsed_uri = urlsplit(self.uri)
        except (TypeError, ValueError):
            parsed_uri = None
        if (
            type(self.uri) is not str
            or parsed_uri is None
            or parsed_uri.scheme != "file"
            or (not parsed_uri.netloc and not parsed_uri.path.startswith("/"))
            or parsed_uri.query
            or parsed_uri.fragment
        ):
            raise ValueError("source fingerprint URI must be an absolute file URI")
        if type(self.byte_size) is not int or self.byte_size < 0:
            raise ValueError("source fingerprint byte size must be nonnegative")
        if type(self.sha256) is not str or _SHA256.fullmatch(self.sha256) is None:
            raise ValueError("source fingerprint SHA-256 must be canonical")
