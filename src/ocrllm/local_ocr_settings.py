"""Immutable settings for the local OCR recognition strategy."""

from __future__ import annotations

import math
from dataclasses import dataclass

from .errors import ConfigError


@dataclass(frozen=True, slots=True)
class LocalOCRSettings:
    """Configure confidence filtering without exposing backend internals."""

    minimum_confidence: float = 0.5

    def __post_init__(self) -> None:
        value = self.minimum_confidence
        if (
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not math.isfinite(value)
            or not 0 <= value <= 1
        ):
            raise ConfigError(
                "LocalOCRSettings.minimum_confidence must be in [0, 1].",
                code="CONFIG_INVALID",
            ) from None
        object.__setattr__(self, "minimum_confidence", float(value))
