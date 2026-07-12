"""Write secret-safe worker diagnostics outside the JSON protocol stream."""

from __future__ import annotations

from typing import TextIO


def report_worker_internal_error(error: BaseException, *, stream: TextIO) -> None:
    """Write only an unexpected exception's qualified type to stderr."""

    if not isinstance(error, BaseException):
        raise TypeError("error must be an exception")
    error_type = f"{type(error).__module__}.{type(error).__qualname__}"
    print(f"worker internal error type: {error_type}", file=stream, flush=True)
