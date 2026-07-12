"""Convert one validated absolute local file URI to a platform path."""

from __future__ import annotations

import os
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

from ocrllm.errors import ConfigError


_ENCODED_SEPARATOR = re.compile(r"%(?:2f|5c)", re.IGNORECASE)


def file_uri_to_path(uri: str) -> Path:
    """Decode an unambiguous local/Windows-UNC file URI without filesystem I/O."""

    if _ENCODED_SEPARATOR.search(uri):
        raise _invalid_file_uri()
    try:
        parsed = urlsplit(uri)
        port = parsed.port
    except (TypeError, ValueError):
        raise _invalid_file_uri() from None
    if (
        parsed.scheme != "file"
        or parsed.query
        or parsed.fragment
        or parsed.username is not None
        or parsed.password is not None
        or port is not None
    ):
        raise _invalid_file_uri()

    try:
        decoded = unquote(parsed.path, errors="strict")
    except UnicodeDecodeError:
        raise _invalid_file_uri() from None
    if "\x00" in decoded or "\\" in decoded:
        raise _invalid_file_uri()
    if os.name == "nt":
        if parsed.netloc:
            candidate = Path(f"//{parsed.netloc}{decoded}")
        else:
            local_path = decoded[1:] if _has_windows_drive_prefix(decoded) else decoded
            candidate = Path(local_path)
    else:
        if parsed.netloc not in {"", "localhost"}:
            raise _invalid_file_uri()
        candidate = Path(decoded)
    if not candidate.is_absolute():
        raise _invalid_file_uri()
    return candidate


def _has_windows_drive_prefix(path: str) -> bool:
    return len(path) >= 3 and path[0] == "/" and path[1].isalpha() and path[2] == ":"


def _invalid_file_uri() -> ConfigError:
    return ConfigError(
        "Worker file URI must identify an unambiguous absolute local path.",
        code="CONFIG_INVALID",
    )
