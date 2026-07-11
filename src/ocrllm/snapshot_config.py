"""Copy and revalidate one public configuration at call time."""

from __future__ import annotations

from dataclasses import replace

from .config import Config
from .errors import ConfigError


def snapshot_config(config: Config | None) -> Config:
    """Return an isolated validated Config for one public operation."""
    if config is None:
        return Config()
    if type(config) is not Config:
        raise ConfigError("config must be an exact Config instance", code="CONFIG_INVALID")

    try:
        return replace(config)
    except ConfigError:
        raise
    except Exception:
        raise ConfigError(
            "config could not be copied and validated safely",
            code="CONFIG_INVALID",
        ) from None
