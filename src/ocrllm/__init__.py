"""Public OCRLLM library facade."""

from .config import Config
from .providers.dashscope.provider_settings import DashScopeSettings
from .errors import (
    Cancelled,
    ConfigError,
    DependencyMissing,
    InvalidSource,
    NoSpeechDetected,
    OCRLLMError,
    OutputError,
    OutputExists,
    ProviderError,
    ProviderUnavailable,
    QuotaExhausted,
    RateLimited,
    UnsupportedFormat,
)
from .recognize import recognize
from .recognize_batch import recognize_batch
from .recognition_preferences import RecognitionPreferences
from .result import RecognitionResult

__all__ = [
    "Cancelled",
    "Config",
    "ConfigError",
    "DashScopeSettings",
    "DependencyMissing",
    "InvalidSource",
    "NoSpeechDetected",
    "OCRLLMError",
    "OutputError",
    "OutputExists",
    "ProviderError",
    "ProviderUnavailable",
    "QuotaExhausted",
    "RateLimited",
    "RecognitionResult",
    "RecognitionPreferences",
    "UnsupportedFormat",
    "recognize",
    "recognize_batch",
]

__version__ = "0.1.0"
