from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from ocrllm import (
    ConcurrencyLimited,
    ProviderAccountSuspended,
    ProviderContentBlocked,
    ProviderErrorDisposition,
    ProviderPermissionDenied,
    ProviderRequestInvalid,
    ProviderUnavailable,
    QuotaExhausted,
    RateLimited,
    get_provider_error_disposition,
)
from ocrllm.errors import ProviderError


@pytest.mark.parametrize(
    ("error", "action", "scope", "retryable"),
    [
        (
            ProviderError(code="PROVIDER_AUTHENTICATION"),
            "quarantine_credential",
            "credential",
            False,
        ),
        (
            ProviderPermissionDenied(),
            "quarantine_credential",
            "credential",
            False,
        ),
        (ProviderAccountSuspended(), "stop", "account", False),
        (RateLimited(), "cooldown", "provider", True),
        (ConcurrencyLimited(), "cooldown", "provider", True),
        (QuotaExhausted(), "stop", "account", False),
        (ProviderError(code="PROVIDER_TIMEOUT"), "retry", "provider", True),
        (ProviderError(code="PROVIDER_NETWORK"), "retry", "provider", True),
        (ProviderUnavailable(), "retry", "provider", True),
        (ProviderRequestInvalid(), "fix_request", "request", False),
        (ProviderContentBlocked(), "change_source", "request", False),
        (ProviderError(), "inspect_response", "request", False),
    ],
)
def test_every_provider_error_has_one_stable_disposition(
    error,
    action,
    scope,
    retryable,
) -> None:
    disposition = get_provider_error_disposition(error)

    assert disposition == ProviderErrorDisposition(
        action=action,
        scope=scope,
        retryable=retryable,
    )


def test_adapter_owned_safe_failure_scope_overrides_generic_default() -> None:
    error = RateLimited(details={"failure_scope": "account"})

    disposition = get_provider_error_disposition(error)

    assert disposition.action == "cooldown"
    assert disposition.scope == "account"
    assert disposition.retryable is True


def test_unknown_failure_scope_is_ignored_without_echo() -> None:
    secret = "UNTRUSTED-SCOPE-SECRET-441"
    error = RateLimited(details={"failure_scope": secret})

    disposition = get_provider_error_disposition(error)

    assert disposition.scope == "provider"
    assert secret not in repr(disposition)


def test_disposition_is_frozen_slotted_and_exactly_validated() -> None:
    disposition = ProviderErrorDisposition(
        action="retry",
        scope="provider",
        retryable=True,
    )

    assert not hasattr(disposition, "__dict__")
    with pytest.raises(FrozenInstanceError):
        disposition.action = "stop"  # type: ignore[misc]
    with pytest.raises(ValueError, match="action"):
        ProviderErrorDisposition(
            action="unknown",  # type: ignore[arg-type]
            scope="provider",
            retryable=False,
        )
    with pytest.raises(ValueError, match="scope"):
        ProviderErrorDisposition(
            action="stop",
            scope="unknown",  # type: ignore[arg-type]
            retryable=False,
        )
    with pytest.raises(TypeError, match="boolean"):
        ProviderErrorDisposition(
            action="stop",
            scope="account",
            retryable=1,  # type: ignore[arg-type]
        )


def test_disposition_rejects_non_provider_errors() -> None:
    with pytest.raises(TypeError, match="ProviderError"):
        get_provider_error_disposition(RuntimeError("raw"))  # type: ignore[arg-type]
