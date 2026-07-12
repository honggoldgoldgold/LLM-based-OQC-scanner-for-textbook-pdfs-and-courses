"""Immutable secret-free status chart for a DashScope credential pool."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True, slots=True, kw_only=True)
class DashScopeCredentialSlotReport:
    credential_id: str
    state: Literal["available", "in_flight", "cooldown", "quarantined"]
    in_flight: int
    selection_count: int
    success_count: int
    failure_count: int
    last_error_code: str | None
    cooldown_remaining_seconds: float


@dataclass(frozen=True, slots=True, kw_only=True)
class DashScopeCredentialPoolReport:
    region: str
    account_state: Literal["available", "cooldown", "blocked"]
    account_error_code: str | None
    account_cooldown_remaining_seconds: float
    model_blocks: tuple[tuple[str, str], ...]
    model_cooldowns: tuple[tuple[str, float], ...]
    slots: tuple[DashScopeCredentialSlotReport, ...]
