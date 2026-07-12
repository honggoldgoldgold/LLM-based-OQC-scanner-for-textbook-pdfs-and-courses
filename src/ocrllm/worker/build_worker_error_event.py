"""Convert one typed library failure to a worker error event."""

from __future__ import annotations

from ocrllm.contracts.error_event import ErrorEvent
from ocrllm.contracts.validate_worker_request_id import validate_worker_request_id
from ocrllm.errors import OCRLLMError


def build_worker_error_event(error: OCRLLMError) -> ErrorEvent:
    """Recover a validated request ID and omit its duplicate detail entry."""

    if not isinstance(error, OCRLLMError):
        raise TypeError("error must be an OCRLLMError")
    details = dict(error.details)
    request_id_value = details.pop("request_id", None)
    try:
        request_id = validate_worker_request_id(request_id_value)
    except (TypeError, ValueError):
        request_id = None
    return ErrorEvent(
        request_id=request_id,
        code=error.code,
        message=str(error),
        retryable=error.retryable,
        details=details,
    )
