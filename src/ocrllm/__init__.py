"""Public OCRLLM library facade."""

from .config import Config
from .capability_report import CapabilityReport
from .providers.dashscope.provider_settings import DashScopeSettings
from .errors import (
    Cancelled,
    ConcurrencyLimited,
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
    ProviderAccountSuspended,
    ProviderContentBlocked,
    ProviderPermissionDenied,
    ProviderRequestInvalid,
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
from .provider_error_disposition import (
    ProviderErrorDisposition,
    get_provider_error_disposition,
)
from .result import RecognitionResult

__all__ = [
    "Cancelled",
    "ConcurrencyLimited",
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
    "ProviderAccountSuspended",
    "ProviderContentBlocked",
    "ProviderErrorDisposition",
    "ProviderPermissionDenied",
    "ProviderRequestInvalid",
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
    "get_provider_error_disposition",
]

__version__ = "0.1.0"
