"""Immutable bounds for credential scheduling and cooldown waits."""

from __future__ import annotations

import math
from dataclasses import dataclass

from .errors import ConfigError


@dataclass(frozen=True, slots=True)
class CredentialPoolPolicy:
    """Bound per-credential load, cooldown, and lease acquisition time."""

    max_in_flight_per_credential: int = 1
    cooldown_seconds: float = 60.0
    selection_timeout_seconds: float = 120.0

    def __post_init__(self) -> None:
        if (
            type(self.max_in_flight_per_credential) is not int
            or not 1 <= self.max_in_flight_per_credential <= 32
        ):
            raise ConfigError(
                "CredentialPoolPolicy.max_in_flight_per_credential must be an "
                "integer in [1, 32].",
                code="CONFIG_INVALID",
            ) from None
        object.__setattr__(
            self,
            "cooldown_seconds",
            _bounded_float(
                self.cooldown_seconds,
                field_name="cooldown_seconds",
                minimum=0.0,
            ),
        )
        object.__setattr__(
            self,
            "selection_timeout_seconds",
            _bounded_float(
                self.selection_timeout_seconds,
                field_name="selection_timeout_seconds",
                minimum=0.0,
                minimum_inclusive=False,
            ),
        )


def _bounded_float(
    value: object,
    *,
    field_name: str,
    minimum: float,
    minimum_inclusive: bool = True,
) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ConfigError(
            f"CredentialPoolPolicy.{field_name} must be a finite number.",
            code="CONFIG_INVALID",
        ) from None
    normalized = float(value)
    lower_valid = (
        normalized >= minimum if minimum_inclusive else normalized > minimum
    )
    if not math.isfinite(normalized) or not lower_valid or normalized > 600.0:
        interval = "[0, 600]" if minimum_inclusive else "(0, 600]"
        raise ConfigError(
            f"CredentialPoolPolicy.{field_name} must be in {interval}.",
            code="CONFIG_INVALID",
        ) from None
    return normalized
