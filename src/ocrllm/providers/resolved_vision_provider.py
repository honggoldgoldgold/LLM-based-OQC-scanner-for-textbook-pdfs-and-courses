"""Describe one resolved vision provider without exposing its runtime object."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True, kw_only=True)
class ResolvedVisionProvider:
    """Hold the callable provider plus safe execution metadata."""

    value: object = field(repr=False)
    name: str | None
    model: str | None
    built_in: bool
