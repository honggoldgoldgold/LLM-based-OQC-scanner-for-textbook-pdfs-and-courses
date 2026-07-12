"""Resolve exactly one DashScope credential without exposing its value."""

from __future__ import annotations

import os

from ...errors import ConfigError
from .provider_settings import DashScopeSettings


def resolve_dashscope_credential(settings: DashScopeSettings) -> str:
    """Use the explicit key, then ``DASHSCOPE_API_KEY``, or fail safely."""
    if type(settings) is not DashScopeSettings:
        raise ConfigError(
            "DashScope credential resolution requires exact DashScopeSettings.",
            code="CONFIG_INVALID",
        ) from None
    if settings.credential_pool is not None:
        raise ConfigError(
            "Pooled DashScope credentials require a credential lease.",
            code="CONFIG_INVALID",
        ) from None
    api_key = settings.api_key
    if api_key is None:
        api_key = os.environ.get("DASHSCOPE_API_KEY")
    if type(api_key) is not str or not api_key or api_key != api_key.strip():
        raise ConfigError(
            "DashScope requires DashScopeSettings.api_key or DASHSCOPE_API_KEY.",
            code="CONFIG_MISSING",
        ) from None
    if api_key.startswith("sk-sp-"):
        raise ConfigError(
            "DashScope Coding Plan credentials cannot authorize this library adapter.",
            code="CONFIG_INVALID",
        ) from None
    return api_key
