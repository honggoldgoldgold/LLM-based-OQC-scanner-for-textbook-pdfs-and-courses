"""Copy frozen JSON-compatible data into mutable serialization values."""

from __future__ import annotations

from collections.abc import Mapping

from .freeze_json_value import FrozenJSONValue, JSONValue


def thaw_json_value(value: FrozenJSONValue) -> JSONValue:
    """Return a fresh dict/list representation of one frozen JSON value."""

    if isinstance(value, Mapping):
        return {key: thaw_json_value(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [thaw_json_value(item) for item in value]
    return value
