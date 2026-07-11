"""Validate one public configuration without changing its identity."""

from __future__ import annotations

from .config import Config
from .snapshot_config import snapshot_config


def validate_config(config: Config | None) -> Config:
    """Return the caller's exact Config after a complete fresh validation."""
    if config is None:
        return Config()
    snapshot_config(config)
    return config
