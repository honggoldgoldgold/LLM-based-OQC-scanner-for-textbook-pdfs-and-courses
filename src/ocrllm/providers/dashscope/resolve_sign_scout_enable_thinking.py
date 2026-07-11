"""Resolve the fixed thinking mode for one DashScope sign-scout model."""

from __future__ import annotations

from ...errors import ConfigError
from .resolve_dashscope_model import DEFAULT_DASHSCOPE_MODEL


def resolve_sign_scout_enable_thinking(model: str) -> bool:
    """Return the evidence-backed thinking mode for a supported scout model."""

    if model == "qwen-vl-max":
        return False
    if model == DEFAULT_DASHSCOPE_MODEL:
        return True
    raise ConfigError(
        "The standalone-sign scout model has no fixed thinking-mode contract.",
        code="CONFIG_INVALID",
    ) from None
