"""Public OCRLLM library facade."""

from .api import recognize, recognize_batch
from .config import Config
from .errors import Cancelled, ConfigError, OCRLLMError, QuotaExhausted, UnsupportedFormat
from .result import RecognitionResult

__all__ = [
    "Cancelled",
    "Config",
    "ConfigError",
    "OCRLLMError",
    "QuotaExhausted",
    "RecognitionResult",
    "UnsupportedFormat",
    "recognize",
    "recognize_batch",
]

__version__ = "0.1.0"
