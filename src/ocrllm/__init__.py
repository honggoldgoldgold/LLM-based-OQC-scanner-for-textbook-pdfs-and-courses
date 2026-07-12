"""Public OCRLLM library facade."""

from .config import Config
from .capability_report import CapabilityReport
from .providers.dashscope.provider_settings import DashScopeSettings
from .errors import (
    Cancelled,
    ConfigError,
    DependencyMissing,
    InvalidSource,
    NoTextDetected,
    NoSpeechDetected,
    OCRBackendError,
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
from .get_capabilities import get_capabilities
from .local_ocr_settings import LocalOCRSettings
from .recognition_preferences import RecognitionPreferences
from .recognition_execution_policy import RecognitionExecutionPolicy
from .vision_model_settings import VisionModelSettings
from .result import RecognitionResult

__all__ = [
    "Cancelled",
    "Config",
    "CapabilityReport",
    "ConfigError",
    "DashScopeSettings",
    "DependencyMissing",
    "InvalidSource",
    "LocalOCRSettings",
    "NoTextDetected",
    "NoSpeechDetected",
    "OCRBackendError",
    "OCRLLMError",
    "OutputError",
    "OutputExists",
    "ProviderError",
    "ProviderUnavailable",
    "QuotaExhausted",
    "RateLimited",
    "RecognitionResult",
    "RecognitionExecutionPolicy",
    "RecognitionPreferences",
    "UnsupportedFormat",
    "VisionModelSettings",
    "recognize",
    "recognize_batch",
    "get_capabilities",
]

__version__ = "0.1.0"
