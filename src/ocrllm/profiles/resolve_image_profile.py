"""Resolve the one registered Phase 0 image profile."""

from __future__ import annotations

from ..errors import ConfigError


def resolve_image_profile(configured_profile: str | None) -> str:
    """Return ``board`` or reject an unregistered image profile."""
    profile = "board" if configured_profile is None else configured_profile
    if profile != "board":
        raise ConfigError(
            "Config.profile must be 'board' for image recognition.",
            code="CONFIG_INVALID",
        )
    return profile
