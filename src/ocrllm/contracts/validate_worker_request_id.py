"""Validate one canonical worker request UUID."""

from __future__ import annotations

from uuid import UUID


def validate_worker_request_id(request_id: object) -> str:
    """Return a canonical lowercase UUID string or raise a redacted error."""

    if not isinstance(request_id, str):
        raise TypeError("worker request_id must be a canonical UUID string")
    try:
        parsed = UUID(request_id)
    except (AttributeError, TypeError, ValueError):
        raise ValueError("worker request_id must be a canonical UUID string") from None
    if str(parsed) != request_id:
        raise ValueError("worker request_id must be a canonical UUID string")
    return request_id
