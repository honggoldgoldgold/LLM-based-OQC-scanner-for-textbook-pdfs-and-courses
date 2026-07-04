"""Provider selection rules for visual and audio work."""

from __future__ import annotations

from OCRLLM.config import AppConfig


def uses_codex_for_vision(cfg: AppConfig) -> bool:
    return bool(cfg.codex_vision.enabled)


def uses_independent_vision_provider(cfg: AppConfig) -> bool:
    return bool(cfg.vision_api.enabled) and not uses_codex_for_vision(cfg)


def uses_google_for_vision(cfg: AppConfig) -> bool:
    return bool(cfg.google_api.enabled) and not (
        uses_codex_for_vision(cfg) or uses_independent_vision_provider(cfg)
    )


def uses_google_for_audio(cfg: AppConfig) -> bool:
    return bool(cfg.google_api.enabled)


def visual_batch_size(cfg: AppConfig) -> int:
    if uses_google_for_vision(cfg):
        return max(1, int(cfg.google_api.vision_batch_size))
    if uses_codex_for_vision(cfg):
        return max(1, int(cfg.codex_vision.vision_batch_size))
    return max(1, int(cfg.processing.batch_size))


def visual_video_frame_batch_size(cfg: AppConfig) -> int:
    if uses_google_for_vision(cfg):
        return max(1, int(cfg.google_api.video_frame_batch_size))
    if uses_codex_for_vision(cfg):
        return max(1, int(cfg.codex_vision.video_frame_batch_size))
    return max(1, int(cfg.video.batch_size))


def visual_parallel_requests(cfg: AppConfig) -> int:
    if uses_google_for_vision(cfg):
        return max(1, int(cfg.google_api.parallel_requests))
    if uses_codex_for_vision(cfg):
        return max(1, int(cfg.codex_vision.parallel_requests))
    return max(1, int(cfg.concurrency.llm_parallel_requests))


def visual_request_stagger_seconds(cfg: AppConfig) -> float:
    if uses_google_for_vision(cfg):
        return max(0.0, float(cfg.google_api.request_stagger_seconds))
    if uses_codex_for_vision(cfg):
        return max(0.0, float(cfg.codex_vision.request_stagger_seconds))
    return max(0.0, float(cfg.concurrency.llm_request_stagger_seconds))


def visual_allows_high_parallel(cfg: AppConfig) -> bool:
    return uses_google_for_vision(cfg) or uses_codex_for_vision(cfg)
