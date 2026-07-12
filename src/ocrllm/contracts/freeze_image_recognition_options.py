"""Validate and freeze v1alpha1 image recognition options."""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import cast

from ocrllm.errors import ConfigError
from ocrllm.freeze_json_value import FrozenJSONValue, JSONValue, freeze_json_value

from .validate_absolute_file_uri import validate_absolute_file_uri


_OPTION_KEYS = frozenset({"output_directory_uri", "overwrite", "timeout_seconds"})


def freeze_image_recognition_options(
    options: object,
) -> Mapping[str, FrozenJSONValue]:
    """Apply exact option defaults and return an immutable JSON mapping."""

    if not isinstance(options, Mapping):
        raise ConfigError("Recognition options must be a JSON object.")
    if any(not isinstance(key, str) for key in options):
        raise ConfigError("Recognition option names must be text.")
    unknown = set(options) - _OPTION_KEYS
    if unknown:
        raise ConfigError("Recognition options contain unknown keys.")

    output_directory_uri = options.get("output_directory_uri")
    if output_directory_uri is not None:
        try:
            output_directory_uri = validate_absolute_file_uri(
                output_directory_uri,
                field_name="output_directory_uri",
            )
        except (TypeError, ValueError):
            raise ConfigError(
                "Recognition output_directory_uri must be an absolute file URI."
            ) from None

    overwrite = options.get("overwrite", False)
    if not isinstance(overwrite, bool):
        raise ConfigError("Recognition overwrite must be a boolean.")

    timeout_seconds = options.get("timeout_seconds", 120)
    if (
        isinstance(timeout_seconds, bool)
        or not isinstance(timeout_seconds, (int, float))
        or not 0 < timeout_seconds <= 600
    ):
        raise ConfigError("Recognition timeout_seconds must be in (0, 600].")

    normalized: Mapping[str, JSONValue] = {
        "output_directory_uri": output_directory_uri,
        "overwrite": overwrite,
        "timeout_seconds": timeout_seconds,
    }
    frozen = freeze_json_value(normalized)
    if not isinstance(frozen, MappingProxyType):
        raise AssertionError("normalized recognition options must be a JSON object")
    return cast(Mapping[str, FrozenJSONValue], frozen)
