"""Map DashScope/OpenAI failures into stable secret-safe public errors."""

from __future__ import annotations

import re

from ...errors import (
    ConfigError,
    InvalidSource,
    OCRLLMError,
    ProviderError,
    ProviderUnavailable,
    QuotaExhausted,
    RateLimited,
)


_SAFE_PROVIDER_VALUE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
_NONRETRYABLE_QUOTA_CODES = frozenset(
    {
        "allocationquotafreetieronly",
        "arrearage",
        "commoditynotpurchased",
        "freequotaexceeded",
        "postpaidbilloverdue",
        "prepaidbilloverdue",
    }
)
_TIMEOUT_CODES = frozenset(
    {
        "internalerrortimeout",
        "requesttimeout",
        "responsetimeout",
    }
)


def map_dashscope_error(
    error: Exception,
    *,
    openai_module: object,
    model: str,
) -> OCRLLMError:
    """Classify one trusted-adapter failure without using exception text."""
    status = _safe_integer_attribute(error, "status_code")
    provider_code = _extract_provider_code(error)
    details: dict[str, str | int] = {
        "provider": "dashscope",
        "model": model,
    }
    if status is not None:
        details["http_status"] = status
    if provider_code is not None:
        details["provider_code"] = provider_code
    request_id = _safe_text_attribute(error, "request_id")
    if request_id is not None:
        details["request_id"] = request_id

    normalized_code = _normalize_provider_code(provider_code)
    if _is_nonretryable_quota_code(normalized_code):
        return QuotaExhausted(
            "The DashScope account cannot spend the requested quota.",
            details=details,
        )
    if normalized_code == "datainspectionfailed":
        return ProviderError(
            "DashScope rejected the request during provider data inspection.",
            code="PROVIDER_RESPONSE_INVALID",
            details=details,
        )
    if normalized_code in _TIMEOUT_CODES:
        return ProviderError(
            "The DashScope request timed out.",
            code="PROVIDER_TIMEOUT",
            details=details,
        )

    if _is_sdk_error(error, openai_module, "APITimeoutError") or isinstance(
        error, TimeoutError
    ) or status == 408:
        return ProviderError(
            "The DashScope request timed out.",
            code="PROVIDER_TIMEOUT",
            details=details,
        )
    if _is_sdk_error(error, openai_module, "APIConnectionError") or isinstance(
        error, ConnectionError
    ):
        return ProviderError(
            "The DashScope service could not be reached.",
            code="PROVIDER_NETWORK",
            details=details,
        )
    if (
        _is_sdk_error(error, openai_module, "AuthenticationError")
        or _is_sdk_error(error, openai_module, "PermissionDeniedError")
        or status in {401, 403}
    ):
        return ProviderError(
            "DashScope rejected authentication or authorization.",
            code="PROVIDER_AUTHENTICATION",
            details=details,
        )
    if _is_sdk_error(error, openai_module, "RateLimitError") or status == 429:
        return RateLimited(
            "DashScope temporarily rate-limited the request.",
            details=details,
        )
    if (
        _is_sdk_error(error, openai_module, "InternalServerError")
        or status == 409
        or status is not None
        and 500 <= status <= 599
    ):
        return ProviderUnavailable(
            "The DashScope model service is temporarily unavailable.",
            details=details,
        )
    if status == 413:
        return InvalidSource(
            "DashScope rejected the encoded image request as too large.",
            code="SOURCE_TOO_LARGE",
            details=details,
        )
    if status == 415:
        return InvalidSource(
            "DashScope rejected the encoded image media type.",
            code="SOURCE_INVALID",
            details=details,
        )
    if status in {400, 404, 422}:
        return ConfigError(
            "DashScope rejected the configured model, endpoint, or request parameters.",
            code="CONFIG_INVALID",
            details=details,
        )

    return ProviderError(
        "DashScope failed without a valid recognition response.",
        code="PROVIDER_RESPONSE_INVALID",
        details=details,
    )


def _is_sdk_error(error: Exception, module: object, class_name: str) -> bool:
    try:
        error_type = getattr(module, class_name, None)
    except Exception:
        return False
    return isinstance(error_type, type) and isinstance(error, error_type)


def _safe_integer_attribute(error: Exception, name: str) -> int | None:
    try:
        value = getattr(error, name, None)
    except Exception:
        return None
    if type(value) is int and 100 <= value <= 599:
        return value
    return None


def _safe_text_attribute(error: Exception, name: str) -> str | None:
    try:
        value = getattr(error, name, None)
    except Exception:
        return None
    if type(value) is str and _SAFE_PROVIDER_VALUE.fullmatch(value) is not None:
        return value
    return None


def _extract_provider_code(error: Exception) -> str | None:
    direct = _safe_text_attribute(error, "code")
    if direct is not None:
        return direct
    try:
        body = getattr(error, "body", None)
    except Exception:
        return None
    if type(body) is not dict:
        return None

    value = body.get("code")
    if type(value) is str and _SAFE_PROVIDER_VALUE.fullmatch(value) is not None:
        return value
    nested = body.get("error")
    if type(nested) is dict:
        value = nested.get("code")
        if type(value) is str and _SAFE_PROVIDER_VALUE.fullmatch(value) is not None:
            return value
    return None


def _normalize_provider_code(value: str | None) -> str | None:
    if value is None:
        return None
    return "".join(character for character in value.casefold() if character.isalnum())


def _is_nonretryable_quota_code(value: str | None) -> bool:
    if value is None:
        return False
    return (
        value in _NONRETRYABLE_QUOTA_CODES
        or "billoverdue" in value
        or "commoditynotpurchased" in value
        or "free" in value
        and "quota" in value
        and ("exceed" in value or "expire" in value)
    )
