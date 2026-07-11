"""Create one no-retry synchronous OpenAI client for DashScope."""

from __future__ import annotations

from types import ModuleType
from typing import Any

from .provider_settings import DashScopeSettings


def create_dashscope_openai_client(
    openai_module: ModuleType,
    *,
    api_key: str,
    settings: DashScopeSettings,
    timeout_seconds: float,
) -> Any:
    """Construct the client with an explicit endpoint and no SDK retries."""
    return openai_module.OpenAI(
        api_key=api_key,
        base_url=settings.base_url,
        timeout=timeout_seconds,
        max_retries=0,
    )
