"""Immutable direct-Python configuration for OCRLLM calls."""

from __future__ import annotations

import math
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal, cast

from .errors import ConfigError
from .freeze_json_value import FrozenJSONValue, JSONValue, freeze_json_value
from .providers.dashscope.provider_settings import DashScopeSettings
from .recognition_preferences import RecognitionPreferences


_LANGUAGE_SUBTAG = re.compile(r"^[A-Za-z0-9]{1,8}$")
_PDF_MODES = frozenset({"text", "vision"})


@dataclass(frozen=True, slots=True)
class Config:
    """Runtime options for OCRLLM library calls."""

    provider: str | object | None = field(default=None, repr=False)
    api_key: str | None = field(default=None, repr=False)
    model: str | None = None
    dashscope: DashScopeSettings | None = field(default=None, repr=False)
    preferences: RecognitionPreferences = field(default_factory=RecognitionPreferences)
    profile: str | None = None
    input_languages: tuple[str, ...] = ()
    output_language: str | None = None
    pdf_mode: Literal["text", "vision"] | None = None
    pdf_pages: tuple[int, ...] | None = None
    pdf_password: str | None = field(default=None, repr=False)
    pdf_allow_partial: bool = False
    output_dir: str | Path | None = None
    temp_dir: str | Path | None = None
    cache_dir: str | Path | None = None
    timeout_seconds: float = 120.0
    resume: bool = False
    overwrite: bool = False
    progress: object | None = field(default=None, repr=False)
    cancellation: object | None = field(default=None, repr=False)
    extra: Mapping[str, JSONValue] = field(default_factory=dict, repr=False)

    def __post_init__(self) -> None:
        _validate_optional_nonempty_text(self.provider, field_name="provider", allow_object=True)
        _validate_optional_nonempty_text(self.api_key, field_name="api_key")
        _validate_optional_nonempty_text(self.model, field_name="model")
        _validate_optional_nonempty_text(self.profile, field_name="profile")
        _validate_optional_text(self.pdf_password, field_name="pdf_password")
        dashscope = _normalize_dashscope_pair(self.provider, self.dashscope)
        preferences = _normalize_preferences(self.preferences)
        _validate_dashscope_scout_workflow(
            dashscope=dashscope,
            preferences=preferences,
        )

        input_languages = _normalize_input_languages(self.input_languages)
        output_language = _normalize_output_language(self.output_language)
        pdf_pages = _normalize_pdf_pages(self.pdf_pages)
        timeout_seconds = _normalize_timeout(self.timeout_seconds)

        if self.pdf_mode is not None and self.pdf_mode not in _PDF_MODES:
            raise ConfigError("Config.pdf_mode must be 'text', 'vision', or None") from None
        _require_boolean(self.pdf_allow_partial, field_name="pdf_allow_partial")
        _require_boolean(self.resume, field_name="resume")
        _require_boolean(self.overwrite, field_name="overwrite")

        _validate_optional_path(self.output_dir, field_name="output_dir")
        _validate_optional_path(self.temp_dir, field_name="temp_dir")
        _validate_optional_path(self.cache_dir, field_name="cache_dir")

        if self.resume and self.output_dir is None:
            raise ConfigError("Config.resume requires Config.output_dir") from None
        if self.resume and self.overwrite:
            raise ConfigError("Config.resume and Config.overwrite cannot both be true") from None

        extra = _freeze_extra(self.extra)
        object.__setattr__(self, "input_languages", input_languages)
        object.__setattr__(self, "output_language", output_language)
        object.__setattr__(self, "pdf_pages", pdf_pages)
        object.__setattr__(self, "timeout_seconds", timeout_seconds)
        object.__setattr__(self, "dashscope", dashscope)
        object.__setattr__(self, "preferences", preferences)
        object.__setattr__(self, "extra", extra)

    def output_directory(self) -> Path | None:
        """Return the configured output directory, or None for in-memory mode."""
        if self.output_dir is None:
            return None
        return Path(self.output_dir)


def _normalize_preferences(value: object) -> RecognitionPreferences:
    if type(value) is not RecognitionPreferences:
        raise ConfigError(
            "Config.preferences must be an exact RecognitionPreferences instance",
            code="CONFIG_INVALID",
        ) from None
    return RecognitionPreferences(
        draft_candidates=value.draft_candidates,
        review_passes=value.review_passes,
    )


def _validate_optional_nonempty_text(
    value: object | None,
    *,
    field_name: str,
    allow_object: bool = False,
) -> None:
    if value is None:
        return
    if allow_object:
        if type(value) is str:
            if not value.strip():
                raise ConfigError(
                    f"Config.{field_name} must be nonempty text when set"
                ) from None
            return
        if isinstance(value, str):
            raise ConfigError(
                f"Config.{field_name} must name an exact built-in provider "
                "or be a provider object"
            ) from None
        return
    if type(value) is not str or not value.strip():
        raise ConfigError(f"Config.{field_name} must be nonempty text when set") from None


def _validate_optional_text(value: object | None, *, field_name: str) -> None:
    if value is not None and type(value) is not str:
        raise ConfigError(f"Config.{field_name} must be text when set") from None


def _normalize_dashscope_pair(
    provider: object | None,
    dashscope: object | None,
) -> DashScopeSettings | None:
    if dashscope is not None and type(dashscope) is not DashScopeSettings:
        raise ConfigError(
            "Config.dashscope must be DashScopeSettings when set."
        ) from None

    uses_builtin_dashscope = type(provider) is str and provider == "dashscope"
    if uses_builtin_dashscope and dashscope is None:
        raise ConfigError(
            "Config.provider='dashscope' requires Config.dashscope settings.",
            code="CONFIG_MISSING",
        ) from None
    if not uses_builtin_dashscope and dashscope is not None:
        raise ConfigError(
            "Config.dashscope is valid only with the exact built-in provider 'dashscope'."
        ) from None
    if dashscope is None:
        return None

    # ``frozen=True`` prevents ordinary assignment, but callers can still use
    # ``object.__setattr__``. Reconstruct the nested value so Config owns a
    # freshly validated endpoint snapshot rather than trusting prior state.
    return DashScopeSettings(
        region=dashscope.region,
        base_url=dashscope.base_url,
        enable_thinking=dashscope.enable_thinking,
        vl_high_resolution_images=dashscope.vl_high_resolution_images,
        standalone_sign_scout_model=dashscope.standalone_sign_scout_model,
    )


def _validate_dashscope_scout_workflow(
    *,
    dashscope: DashScopeSettings | None,
    preferences: RecognitionPreferences,
) -> None:
    if dashscope is None or dashscope.standalone_sign_scout_model is None:
        return
    if preferences != RecognitionPreferences():
        raise ConfigError(
            "DashScope standalone-sign scouting requires default "
            "RecognitionPreferences",
            code="CONFIG_INVALID",
        ) from None


def _normalize_input_languages(value: object) -> tuple[str, ...]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise ConfigError(
            "Config.input_languages must be an ordered sequence of language tags"
        ) from None
    try:
        languages = tuple(value)
    except Exception:
        raise ConfigError("Config.input_languages could not be read safely") from None

    seen: set[str] = set()
    for language in languages:
        _validate_language_tag(language, field_name="input_languages")
        normalized = language.casefold()
        if normalized in seen:
            raise ConfigError("Config.input_languages must not contain duplicates") from None
        seen.add(normalized)
    return cast(tuple[str, ...], languages)


def _normalize_output_language(value: object | None) -> str | None:
    if value is None:
        return None
    _validate_language_tag(value, field_name="output_language")
    return cast(str, value)


def _validate_language_tag(value: object, *, field_name: str) -> None:
    if type(value) is not str or value != value.strip() or not value:
        raise ConfigError(f"Config.{field_name} contains an invalid language tag") from None

    subtags = value.split("-")
    first = subtags[0]
    ordinary_language = first.isalpha() and 2 <= len(first) <= 8
    private_or_grandfathered = first.casefold() in {"x", "i"} and len(subtags) > 1
    if not (ordinary_language or private_or_grandfathered):
        raise ConfigError(f"Config.{field_name} contains an invalid language tag") from None
    if any(_LANGUAGE_SUBTAG.fullmatch(subtag) is None for subtag in subtags):
        raise ConfigError(f"Config.{field_name} contains an invalid language tag") from None


def _normalize_pdf_pages(value: object | None) -> tuple[int, ...] | None:
    if value is None:
        return None
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise ConfigError("Config.pdf_pages must be an ordered sequence of page numbers") from None
    try:
        pages = tuple(value)
    except Exception:
        raise ConfigError("Config.pdf_pages could not be read safely") from None
    if not pages:
        raise ConfigError("Config.pdf_pages must not be empty when set") from None
    if any(isinstance(page, bool) or not isinstance(page, int) or page <= 0 for page in pages):
        raise ConfigError("Config.pdf_pages must contain positive one-based integers") from None
    if len(set(pages)) != len(pages):
        raise ConfigError("Config.pdf_pages must contain unique page numbers") from None
    return cast(tuple[int, ...], pages)


def _normalize_timeout(value: object) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ConfigError("Config.timeout_seconds must be a finite number") from None
    normalized = float(value)
    if not math.isfinite(normalized) or not 0 < normalized <= 600:
        raise ConfigError("Config.timeout_seconds must be in the interval (0, 600]") from None
    return normalized


def _require_boolean(value: object, *, field_name: str) -> None:
    if not isinstance(value, bool):
        raise ConfigError(f"Config.{field_name} must be a boolean") from None


def _validate_optional_path(value: object | None, *, field_name: str) -> None:
    if value is None or isinstance(value, Path):
        return
    if type(value) is not str or not value.strip():
        raise ConfigError(f"Config.{field_name} must be a nonempty path when set") from None


def _freeze_extra(value: object) -> Mapping[str, FrozenJSONValue]:
    if not isinstance(value, Mapping):
        raise ConfigError("Config.extra must be a JSON object") from None
    try:
        frozen = freeze_json_value(value)
    except (TypeError, ValueError):
        raise ConfigError("Config.extra must contain only finite JSON values") from None
    if not isinstance(frozen, Mapping):
        raise ConfigError("Config.extra must be a JSON object") from None
    return cast(Mapping[str, FrozenJSONValue], frozen)
