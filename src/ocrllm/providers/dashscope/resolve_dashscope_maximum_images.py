"""Resolve the documented image count cap for one supported DashScope model."""

from __future__ import annotations

from ...errors import ConfigError
from .resolve_dashscope_model import SUPPORTED_DASHSCOPE_MODELS


_MAXIMUM_IMAGES_BY_MODEL = {
    model: 10 for model in SUPPORTED_DASHSCOPE_MODELS
}


def resolve_dashscope_maximum_images(model: str) -> int:
    """Return the pre-upload image cap for one already resolved model."""
    try:
        return _MAXIMUM_IMAGES_BY_MODEL[model]
    except (KeyError, TypeError):
        raise ConfigError(
            "The DashScope vision model has no approved image-count capability.",
            code="CONFIG_INVALID",
        ) from None
