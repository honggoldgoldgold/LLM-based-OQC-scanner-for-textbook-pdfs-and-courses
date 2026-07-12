"""Resolve the strictest image count limit for one configured workflow."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .image_group_limits import MAX_IMAGE_GROUP_COUNT
from .providers.dashscope.provider_settings import DashScopeSettings
from .providers.dashscope.resolve_dashscope_maximum_images import (
    resolve_dashscope_maximum_images,
)
from .providers.dashscope.resolve_dashscope_model import resolve_dashscope_model

if TYPE_CHECKING:
    from .config import Config


def resolve_effective_image_limit(config: Config) -> tuple[int, str]:
    """Return the strictest pre-upload limit and its safe policy source."""
    candidates = [
        (MAX_IMAGE_GROUP_COUNT, "library_safety"),
        (
            config.execution.maximum_images_per_request,
            "recognition_execution_policy",
        ),
    ]
    configured_model_limit = config.vision_model.maximum_images_per_request
    if configured_model_limit is not None:
        candidates.append((configured_model_limit, "vision_model_settings"))
    if type(config.provider) is DashScopeSettings:
        model = resolve_dashscope_model(config.vision_model.name)
        candidates.append(
            (resolve_dashscope_maximum_images(model), "dashscope_model_capability")
        )
    return min(candidates, key=lambda candidate: candidate[0])
