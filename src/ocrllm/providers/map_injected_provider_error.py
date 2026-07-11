"""Map injected-provider failures without exposing provider text."""

from __future__ import annotations

from ..errors import (
    Cancelled,
    OCRLLMError,
    ProviderError,
    ProviderUnavailable,
    QuotaExhausted,
    RateLimited,
)


def map_injected_provider_error(error: Exception, *, model: str | None) -> OCRLLMError:
    """Return a redacted public error for one injected-provider failure."""
    details = {"model": model}
    try:
        raw_code = getattr(error, "code", None)
    except Exception:
        raw_code = None
    code = raw_code if type(raw_code) is str else None

    if isinstance(error, Cancelled) or code == "CANCELLED":
        return Cancelled("Recognition was cancelled before a provider result was available.")
    if isinstance(error, QuotaExhausted) or code == "PROVIDER_QUOTA_EXHAUSTED":
        return QuotaExhausted(
            "The configured provider quota is exhausted.",
            details=details,
        )
    if isinstance(error, RateLimited) or code == "PROVIDER_RATE_LIMITED":
        return RateLimited(
            "The configured provider temporarily rate-limited the request.",
            details=details,
        )
    if isinstance(error, TimeoutError) or code == "PROVIDER_TIMEOUT":
        return ProviderError(
            "The configured provider timed out.",
            code="PROVIDER_TIMEOUT",
            retryable=True,
            details=details,
        )
    if isinstance(error, ConnectionError) or code == "PROVIDER_NETWORK":
        return ProviderError(
            "The configured provider could not be reached.",
            code="PROVIDER_NETWORK",
            retryable=True,
            details=details,
        )
    if code == "PROVIDER_AUTHENTICATION":
        return ProviderError(
            "The configured provider rejected authentication.",
            code="PROVIDER_AUTHENTICATION",
            details=details,
        )
    if isinstance(error, ProviderUnavailable) or code == "PROVIDER_UNAVAILABLE":
        return ProviderUnavailable(
            "The configured provider is temporarily unavailable.",
            details=details,
        )

    return ProviderError(
        "The configured provider failed without a valid recognition response.",
        code="PROVIDER_RESPONSE_INVALID",
        details=details,
    )
