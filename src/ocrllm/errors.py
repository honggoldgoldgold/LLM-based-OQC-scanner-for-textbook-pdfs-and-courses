"""Public OCRLLM exception types."""


class OCRLLMError(Exception):
    """Base class for public OCRLLM errors."""


class ConfigError(OCRLLMError):
    """Configuration is missing or invalid."""


class QuotaExhausted(OCRLLMError):
    """All configured model quota options were exhausted."""


class UnsupportedFormat(OCRLLMError):
    """The input format is not supported by the library facade."""


class Cancelled(OCRLLMError):
    """Recognition was cancelled by the caller."""
