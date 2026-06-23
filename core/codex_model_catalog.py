"""Codex vision model defaults shared by config, CLI runner, and GUI."""

from __future__ import annotations

CODEX_VISION_DEFAULT_MODEL = "gpt-5.5"
CODEX_VISION_STALE_DEFAULT_MODELS = frozenset({
    "gpt-5.4-mini",
})
CODEX_VISION_MODEL_CHOICES = (
    CODEX_VISION_DEFAULT_MODEL,
    "gpt-5.4-mini",
    "gpt-5.4",
    "gpt-5.3-codex-spark",
)


def normalize_codex_vision_model(model: str | None) -> str:
    value = (model or "").strip()
    if not value:
        return CODEX_VISION_DEFAULT_MODEL
    return value


def migrate_stored_codex_vision_model(model: str | None) -> str:
    value = normalize_codex_vision_model(model)
    if value in CODEX_VISION_STALE_DEFAULT_MODELS:
        return CODEX_VISION_DEFAULT_MODEL
    return value
