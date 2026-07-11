"""Resolve the explicit or reproducibly pinned DashScope vision model."""

from __future__ import annotations

from ...errors import ConfigError


DEFAULT_DASHSCOPE_MODEL = "qwen3.7-plus-2026-05-26"
SUPPORTED_DASHSCOPE_MODELS = frozenset(
    {
        "qwen3.7-plus",
        DEFAULT_DASHSCOPE_MODEL,
        "qwen-vl-max",
    }
)


def resolve_dashscope_model(configured_model: str | None) -> str:
    """Return the caller's model or the fixed Phase 1 evidence baseline."""
    if configured_model is not None and type(configured_model) is not str:
        raise ConfigError(
            "Config.model must be an exact string for the DashScope adapter.",
            code="CONFIG_INVALID",
        ) from None
    model = DEFAULT_DASHSCOPE_MODEL if configured_model is None else configured_model
    if model not in SUPPORTED_DASHSCOPE_MODELS:
        raise ConfigError(
            "The Phase 1 DashScope adapter supports qwen3.7-plus, its "
            "2026-05-26 snapshot, and qwen-vl-max.",
            code="CONFIG_INVALID",
        ) from None
    return model
