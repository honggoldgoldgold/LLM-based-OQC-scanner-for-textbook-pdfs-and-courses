"""Honor an Event-compatible cancellation signal before recognition work."""

from __future__ import annotations

from .errors import Cancelled, ConfigError


def raise_if_cancelled(cancellation: object | None) -> None:
    """Raise ``Cancelled`` when an explicit Event-compatible signal is set."""
    if cancellation is None:
        return

    try:
        is_set = getattr(cancellation, "is_set", None)
    except Exception:
        raise ConfigError(
            "Config.cancellation could not be inspected safely.",
            code="CONFIG_INVALID",
        ) from None
    if not callable(is_set):
        raise ConfigError(
            "Config.cancellation must expose a callable is_set() method.",
            code="CONFIG_INVALID",
        ) from None

    try:
        cancelled = is_set()
    except Exception:
        raise ConfigError(
            "Config.cancellation could not be checked safely.",
            code="CONFIG_INVALID",
        ) from None
    if type(cancelled) is not bool:
        raise ConfigError(
            "Config.cancellation.is_set() must return a boolean.",
            code="CONFIG_INVALID",
        ) from None
    if cancelled:
        raise Cancelled("Recognition was cancelled before recognition work.") from None
