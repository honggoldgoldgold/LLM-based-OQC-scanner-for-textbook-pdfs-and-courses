"""Provider router for OCRLLM model clients."""

from __future__ import annotations

from threading import Event
from typing import Optional

from OCRLLM.config import AppConfig


def build_llm_client(cfg: Optional[AppConfig] = None, cancel_event: Optional[Event] = None):
    cfg = cfg or AppConfig()
    if cfg.google_api.enabled:
        from OCRLLM.core.providers.google_provider import GoogleProviderClient
        return GoogleProviderClient(cfg=cfg, cancel_event=cancel_event)

    from OCRLLM.core.llm_client import LLMClient
    return LLMClient(cfg=cfg, cancel_event=cancel_event)
