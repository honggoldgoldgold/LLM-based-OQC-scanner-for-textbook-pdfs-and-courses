"""Client that combines Google audio/text with non-Google visual routing."""

from __future__ import annotations

from threading import Event
from typing import Optional

from OCRLLM.config import AppConfig
from OCRLLM.core.llm_client import LLMClient
from OCRLLM.core.providers.google_provider import GoogleProviderClient


class HybridGoogleProviderClient:
    """Route visual calls through LLMClient and Google-only calls through Gemini."""

    def __init__(self, cfg: Optional[AppConfig] = None, cancel_event: Optional[Event] = None):
        self.cfg = cfg or AppConfig()
        self._google = GoogleProviderClient(cfg=self.cfg, cancel_event=cancel_event)
        self._visual = LLMClient(cfg=self.cfg, cancel_event=cancel_event)

    def set_cancel_event(self, cancel_event: Optional[Event]):
        self._google.set_cancel_event(cancel_event)
        self._visual.set_cancel_event(cancel_event)

    def last_successful_model(self, kind: str) -> str | None:
        return self._google.last_successful_model(kind)

    def chat_with_images(self, *args, **kwargs):
        return self._visual.chat_with_images(*args, **kwargs)

    def chat_with_images_contextual(self, *args, **kwargs):
        return self._visual.chat_with_images_contextual(*args, **kwargs)

    def probe_vision_model(self, *args, **kwargs):
        return self._visual.probe_vision_model(*args, **kwargs)

    def chat_text(self, *args, **kwargs):
        return self._google.chat_text(*args, **kwargs)

    def transcribe_long_audio(self, *args, **kwargs):
        return self._google.transcribe_long_audio(*args, **kwargs)

    def transcribe_short_audio(self, *args, **kwargs):
        return self._visual.transcribe_short_audio(*args, **kwargs)
