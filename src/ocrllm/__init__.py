"""Public OCRLLM library facade."""

from .config import Config
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
    QuotaExhausted,
    UnsupportedFormat,
)
from .recognize import recognize
from .recognize_batch import recognize_batch
from .result import RecognitionResult

__all__ = [
    "Cancelled",
    "Config",
    "ConfigError",
    "DependencyMissing",
    "InvalidSource",
    "NoSpeechDetected",
    "OCRLLMError",
    "OutputError",
    "OutputExists",
    "ProviderError",
    "QuotaExhausted",
    "RecognitionResult",
    "UnsupportedFormat",
    "recognize",
    "recognize_batch",
]

__version__ = "0.1.0"
