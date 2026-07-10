"""Copy JSON-compatible data into an immutable representation."""

from __future__ import annotations

import math
from collections.abc import Mapping
from types import MappingProxyType
from typing import TypeAlias, cast


JSONScalar: TypeAlias = None | bool | int | float | str
JSONValue: TypeAlias = (
    JSONScalar
    | Mapping[str, "JSONValue"]
    | list["JSONValue"]
    | tuple["JSONValue", ...]
)
FrozenJSONValue: TypeAlias = (
    JSONScalar | Mapping[str, "FrozenJSONValue"] | tuple["FrozenJSONValue", ...]
)


class _InvalidJSONValue(ValueError):
    """Internal marker whose messages never contain caller-controlled values."""


def freeze_json_value(value: object) -> FrozenJSONValue:
    """Deep-copy and freeze finite JSON data.

    JSON objects become read-only mappings and JSON arrays become tuples. Error
    messages intentionally omit caller values so invalid provider data cannot
    leak credentials or arbitrary exception text.
    """

    try:
        return _freeze_json_value(value, active_container_ids=set())
    except _InvalidJSONValue as exc:
        raise ValueError(str(exc)) from None
    except Exception:
        raise ValueError("JSON data could not be read safely") from None


def _freeze_json_value(
    value: object,
    *,
    active_container_ids: set[int],
) -> FrozenJSONValue:
    if value is None or isinstance(value, (bool, int, str)):
        return value

    if isinstance(value, float):
        if not math.isfinite(value):
            raise _InvalidJSONValue("JSON numbers must be finite")
        return value

    if isinstance(value, Mapping):
        container_id = id(value)
        _enter_container(container_id, active_container_ids)
        try:
            frozen_mapping: dict[str, FrozenJSONValue] = {}
            for key, item in value.items():
                if not isinstance(key, str):
                    raise _InvalidJSONValue("JSON object keys must be strings")
                frozen_mapping[key] = _freeze_json_value(
                    item,
                    active_container_ids=active_container_ids,
                )
            return cast(
                Mapping[str, FrozenJSONValue],
                MappingProxyType(frozen_mapping),
            )
        finally:
            active_container_ids.discard(container_id)

    if isinstance(value, (list, tuple)):
        container_id = id(value)
        _enter_container(container_id, active_container_ids)
        try:
            return tuple(
                _freeze_json_value(item, active_container_ids=active_container_ids)
                for item in value
            )
        finally:
            active_container_ids.discard(container_id)

    raise _InvalidJSONValue("JSON data contains an unsupported value")


def _enter_container(container_id: int, active_container_ids: set[int]) -> None:
    if container_id in active_container_ids:
        raise _InvalidJSONValue("JSON data must not contain reference cycles")
    active_container_ids.add(container_id)
