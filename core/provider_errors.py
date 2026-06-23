"""Shared provider error types used by processors."""

from __future__ import annotations


class ProviderSetupError(RuntimeError):
    """Raised when a provider cannot run because the local environment is invalid."""


def is_provider_setup_error(exc: BaseException) -> bool:
    """Return True if an exception chain contains a provider setup failure."""
    seen: set[int] = set()
    current: BaseException | None = exc
    while current is not None and id(current) not in seen:
        if isinstance(current, ProviderSetupError):
            return True
        seen.add(id(current))
        current = current.__cause__ or current.__context__
    return False
