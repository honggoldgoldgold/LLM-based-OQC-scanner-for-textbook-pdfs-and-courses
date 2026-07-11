"""Immutable quality-versus-cost preferences for one recognition workflow."""

from __future__ import annotations

from dataclasses import dataclass

from .errors import ConfigError


@dataclass(frozen=True, slots=True)
class RecognitionPreferences:
    """Select bounded optional work without changing provider configuration."""

    review_passes: int = 0

    def __post_init__(self) -> None:
        if type(self.review_passes) is not int or self.review_passes not in {0, 1}:
            raise ConfigError(
                "RecognitionPreferences.review_passes must be exactly 0 or 1",
                code="CONFIG_INVALID",
            ) from None
