"""Provider router for OCRLLM model clients."""

from __future__ import annotations

from threading import Event
from typing import Optional

from OCRLLM.config import AppConfig
from OCRLLM.core.provider_selection import uses_google_for_audio, uses_google_for_vision


def build_llm_client(cfg: Optional[AppConfig] = None, cancel_event: Optional[Event] = None):
    cfg = cfg or AppConfig()
    if uses_google_for_vision(cfg):
        from OCRLLM.core.providers.google_provider import GoogleProviderClient
        return GoogleProviderClient(cfg=cfg, cancel_event=cancel_event)
    if uses_google_for_audio(cfg):
        from OCRLLM.core.providers.hybrid_google_provider import HybridGoogleProviderClient
        return HybridGoogleProviderClient(cfg=cfg, cancel_event=cancel_event)

    from OCRLLM.core.llm_client import LLMClient
    return LLMClient(cfg=cfg, cancel_event=cancel_event)
