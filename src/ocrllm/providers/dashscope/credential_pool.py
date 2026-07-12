"""Fair concurrency-safe in-memory scheduling for DashScope credentials."""

from __future__ import annotations

import time
from collections.abc import Sequence
from dataclasses import dataclass

from ...credential_pool_policy import CredentialPoolPolicy
from ...errors import (
    ConcurrencyLimited,
    ConfigError,
    ProviderAccountSuspended,
    ProviderError,
    ProviderPermissionDenied,
    QuotaExhausted,
)
from ...provider_error_disposition import get_provider_error_disposition
from ...raise_if_cancelled import raise_if_cancelled
from .credential import DashScopeCredential
from .credential_pool_report import (
    DashScopeCredentialPoolReport,
    DashScopeCredentialSlotReport,
)
from .supported_regions import SUPPORTED_DASHSCOPE_REGIONS


_CANCELLATION_POLL_SECONDS = 0.05
_MAX_CREDENTIALS = 64


@dataclass(slots=True)
class _CredentialSlot:
    credential: DashScopeCredential
    in_flight: int = 0
    last_selected_sequence: int = -1
    selection_count: int = 0
    success_count: int = 0
    failure_count: int = 0
    last_error_code: str | None = None
    cooldown_until: float = 0.0
    quarantined: bool = False


class DashScopeCredentialPool:
    """Lease credentials fairly and retain only secret-safe health state."""

    __slots__ = (
        "_account_block_code",
        "_account_cooldown_until",
        "_condition",
        "_model_blocks",
        "_model_cooldowns",
        "_policy",
        "_region",
        "_selection_sequence",
        "_slots",
    )

    def __init__(
        self,
        *,
        region: str,
        credentials: Sequence[DashScopeCredential],
        policy: CredentialPoolPolicy | None = None,
    ) -> None:
        from threading import Condition, Lock

        if type(region) is not str or region not in SUPPORTED_DASHSCOPE_REGIONS:
            raise ConfigError(
                "DashScopeCredentialPool.region must be a supported canonical region.",
                code="CONFIG_INVALID",
            ) from None
        if isinstance(credentials, (str, bytes)) or not isinstance(
            credentials, Sequence
        ):
            raise ConfigError(
                "DashScopeCredentialPool.credentials must be an ordered sequence.",
                code="CONFIG_INVALID",
            ) from None
        try:
            supplied_credentials = tuple(credentials)
        except Exception:
            raise ConfigError(
                "DashScopeCredentialPool.credentials could not be read safely.",
                code="CONFIG_INVALID",
            ) from None
        if not 1 <= len(supplied_credentials) <= _MAX_CREDENTIALS:
            raise ConfigError(
                "DashScopeCredentialPool requires 1-64 credentials.",
                code="CONFIG_INVALID",
            ) from None

        copied: list[DashScopeCredential] = []
        for credential in supplied_credentials:
            if type(credential) is not DashScopeCredential:
                raise ConfigError(
                    "DashScopeCredentialPool requires exact DashScopeCredential values.",
                    code="CONFIG_INVALID",
                ) from None
            copied.append(
                DashScopeCredential(
                    credential_id=credential.credential_id,
                    api_key=credential.api_key,
                )
            )
        if len({item.credential_id for item in copied}) != len(copied):
            raise ConfigError(
                "DashScopeCredentialPool credential IDs must be unique.",
                code="CONFIG_INVALID",
            ) from None
        if len({item.api_key for item in copied}) != len(copied):
            raise ConfigError(
                "DashScopeCredentialPool API keys must be unique.",
                code="CONFIG_INVALID",
            ) from None

        selected_policy = CredentialPoolPolicy() if policy is None else policy
        if type(selected_policy) is not CredentialPoolPolicy:
            raise ConfigError(
                "DashScopeCredentialPool.policy must be exact CredentialPoolPolicy.",
                code="CONFIG_INVALID",
            ) from None
        self._policy = CredentialPoolPolicy(
            max_in_flight_per_credential=(
                selected_policy.max_in_flight_per_credential
            ),
            cooldown_seconds=selected_policy.cooldown_seconds,
            selection_timeout_seconds=selected_policy.selection_timeout_seconds,
        )
        self._region = region
        self._slots = tuple(_CredentialSlot(item) for item in copied)
        self._condition = Condition(Lock())
        self._selection_sequence = 0
        self._account_cooldown_until = 0.0
        self._account_block_code: str | None = None
        self._model_cooldowns: dict[str, float] = {}
        self._model_blocks: dict[str, str] = {}

    @property
    def region(self) -> str:
        return self._region

    @property
    def policy(self) -> CredentialPoolPolicy:
        return self._policy

    def __repr__(self) -> str:
        return (
            "DashScopeCredentialPool("
            f"region={self._region!r}, credential_count={len(self._slots)}, "
            f"policy={self._policy!r})"
        )

    def snapshot(self) -> DashScopeCredentialPoolReport:
        """Return an immutable ordered status chart without credential values."""
        now = time.monotonic()
        with self._condition:
            self._expire_model_cooldowns(now)
            account_remaining = max(0.0, self._account_cooldown_until - now)
            account_state = (
                "blocked"
                if self._account_block_code is not None
                else "cooldown"
                if account_remaining > 0.0
                else "available"
            )
            slots = tuple(self._slot_report(slot, now=now) for slot in self._slots)
            model_blocks = tuple(sorted(self._model_blocks.items()))
            model_cooldowns = tuple(
                sorted(
                    (model, max(0.0, until - now))
                    for model, until in self._model_cooldowns.items()
                    if until > now
                )
            )
            return DashScopeCredentialPoolReport(
                region=self._region,
                account_state=account_state,
                account_error_code=self._account_block_code,
                account_cooldown_remaining_seconds=account_remaining,
                model_blocks=model_blocks,
                model_cooldowns=model_cooldowns,
                slots=slots,
            )

    def restore_credential(self, credential_id: str) -> None:
        """Make one credential selectable after the host repairs it externally."""
        with self._condition:
            slot = self._find_slot(credential_id)
            slot.quarantined = False
            slot.cooldown_until = 0.0
            slot.last_error_code = None
            self._condition.notify_all()

    def clear_model_block(self, model: str) -> None:
        """Clear one model block/cooldown after an external state change."""
        _validate_model(model)
        with self._condition:
            self._model_blocks.pop(model, None)
            self._model_cooldowns.pop(model, None)
            self._condition.notify_all()

    def clear_account_block(self) -> None:
        """Clear account block/cooldown after an external account repair."""
        with self._condition:
            self._account_block_code = None
            self._account_cooldown_until = 0.0
            self._condition.notify_all()

    def _acquire(
        self,
        *,
        model: str,
        cancellation: object | None,
    ) -> _DashScopeCredentialLease:
        _validate_model(model)
        deadline = time.monotonic() + self._policy.selection_timeout_seconds
        while True:
            raise_if_cancelled(cancellation)
            with self._condition:
                now = time.monotonic()
                self._expire_model_cooldowns(now)
                if self._account_block_code is not None:
                    raise _blocked_error(
                        self._account_block_code,
                        failure_scope="account",
                    )
                model_block_code = self._model_blocks.get(model)
                if model_block_code is not None:
                    raise _blocked_error(model_block_code, failure_scope="model")

                account_wait = max(0.0, self._account_cooldown_until - now)
                model_wait = max(0.0, self._model_cooldowns.get(model, 0.0) - now)
                eligible = (
                    []
                    if account_wait > 0.0 or model_wait > 0.0
                    else [
                        (index, slot)
                        for index, slot in enumerate(self._slots)
                        if not slot.quarantined
                        and slot.cooldown_until <= now
                        and slot.in_flight
                        < self._policy.max_in_flight_per_credential
                    ]
                )
                if eligible:
                    index, slot = min(
                        eligible,
                        key=lambda item: (
                            item[1].in_flight,
                            item[1].last_selected_sequence,
                            item[0],
                        ),
                    )
                    sequence = self._selection_sequence
                    self._selection_sequence += 1
                    slot.in_flight += 1
                    slot.selection_count += 1
                    slot.last_selected_sequence = sequence
                    lease = _DashScopeCredentialLease(
                        pool=self,
                        slot_index=index,
                        model=model,
                        api_key=slot.credential.api_key,
                    )
                else:
                    lease = None

                if lease is None and all(slot.quarantined for slot in self._slots):
                    codes = {slot.last_error_code for slot in self._slots}
                    code = (
                        "PROVIDER_AUTHENTICATION"
                        if codes == {"PROVIDER_AUTHENTICATION"}
                        else "PROVIDER_PERMISSION_DENIED"
                    )
                    raise _blocked_error(code, failure_scope="credential")
                if lease is None:
                    remaining = deadline - now
                    if remaining <= 0.0:
                        raise ConcurrencyLimited(
                            "No DashScope credential became available before the "
                            "pool selection timeout.",
                            details={
                                "provider": "dashscope",
                                "failure_scope": "credential",
                                "pool_state": "capacity_wait_timeout",
                            },
                        ) from None
                    waits = [remaining, _CANCELLATION_POLL_SECONDS]
                    waits.extend(
                        wait
                        for wait in (account_wait, model_wait)
                        if wait > 0.0
                    )
                    waits.extend(
                        slot.cooldown_until - now
                        for slot in self._slots
                        if not slot.quarantined and slot.cooldown_until > now
                    )
                    self._condition.wait(timeout=min(waits))
                    continue

            try:
                raise_if_cancelled(cancellation)
            except BaseException:
                lease._finish(None, succeeded=False)
                raise
            return lease

    def _finish(
        self,
        *,
        slot_index: int,
        model: str,
        error: ProviderError | None,
        succeeded: bool,
    ) -> None:
        with self._condition:
            slot = self._slots[slot_index]
            if slot.in_flight <= 0:
                raise RuntimeError("credential lease accounting is inconsistent")
            slot.in_flight -= 1
            if error is None and succeeded:
                slot.success_count += 1
                self._condition.notify_all()
                return
            if error is None:
                self._condition.notify_all()
                return

            slot.failure_count += 1
            slot.last_error_code = error.code
            disposition = get_provider_error_disposition(error)
            if disposition.action == "quarantine_credential":
                if disposition.scope == "credential":
                    slot.quarantined = True
                elif disposition.scope == "model":
                    self._model_blocks[model] = error.code
                elif disposition.scope == "account":
                    self._account_block_code = error.code
            elif disposition.action == "stop":
                if disposition.scope == "model":
                    self._model_blocks[model] = error.code
                else:
                    self._account_block_code = error.code
            elif disposition.action == "cooldown":
                until = time.monotonic() + self._policy.cooldown_seconds
                if disposition.scope == "credential":
                    slot.cooldown_until = max(slot.cooldown_until, until)
                elif disposition.scope == "model":
                    self._model_cooldowns[model] = max(
                        self._model_cooldowns.get(model, 0.0),
                        until,
                    )
                else:
                    self._account_cooldown_until = max(
                        self._account_cooldown_until,
                        until,
                    )
            self._condition.notify_all()

    def _slot_report(
        self,
        slot: _CredentialSlot,
        *,
        now: float,
    ) -> DashScopeCredentialSlotReport:
        cooldown_remaining = max(0.0, slot.cooldown_until - now)
        state = (
            "quarantined"
            if slot.quarantined
            else "cooldown"
            if cooldown_remaining > 0.0
            else "in_flight"
            if slot.in_flight > 0
            else "available"
        )
        return DashScopeCredentialSlotReport(
            credential_id=slot.credential.credential_id,
            state=state,
            in_flight=slot.in_flight,
            selection_count=slot.selection_count,
            success_count=slot.success_count,
            failure_count=slot.failure_count,
            last_error_code=slot.last_error_code,
            cooldown_remaining_seconds=cooldown_remaining,
        )

    def _find_slot(self, credential_id: str) -> _CredentialSlot:
        if type(credential_id) is not str:
            raise ConfigError(
                "credential_id must be exact text.",
                code="CONFIG_INVALID",
            ) from None
        for slot in self._slots:
            if slot.credential.credential_id == credential_id:
                return slot
        raise ConfigError(
            "credential_id does not identify a pool slot.",
            code="CONFIG_INVALID",
        ) from None

    def _expire_model_cooldowns(self, now: float) -> None:
        expired = [
            model for model, until in self._model_cooldowns.items() if until <= now
        ]
        for model in expired:
            del self._model_cooldowns[model]


class _DashScopeCredentialLease:
    __slots__ = (
        "_api_key",
        "_finish_lock",
        "_finished",
        "_model",
        "_pool",
        "_slot_index",
    )

    def __init__(
        self,
        *,
        pool: DashScopeCredentialPool,
        slot_index: int,
        model: str,
        api_key: str,
    ) -> None:
        from threading import Lock

        self._pool = pool
        self._slot_index = slot_index
        self._model = model
        self._api_key = api_key
        self._finished = False
        self._finish_lock = Lock()

    @property
    def api_key(self) -> str:
        return self._api_key

    def __repr__(self) -> str:
        return "_DashScopeCredentialLease(api_key=[REDACTED])"

    def _finish(self, error: ProviderError | None, *, succeeded: bool) -> None:
        with self._finish_lock:
            if self._finished:
                raise RuntimeError("credential lease was already finished")
            self._finished = True
        self._pool._finish(
            slot_index=self._slot_index,
            model=self._model,
            error=error,
            succeeded=succeeded,
        )
        self._api_key = "[REDACTED]"


def _validate_model(model: object) -> None:
    if type(model) is not str or not model or model != model.strip():
        raise ConfigError(
            "credential pool model must be nonempty exact text.",
            code="CONFIG_INVALID",
        ) from None


def _blocked_error(code: str, *, failure_scope: str) -> ProviderError:
    details = {
        "provider": "dashscope",
        "failure_scope": failure_scope,
        "pool_state": "blocked",
    }
    if code == "PROVIDER_AUTHENTICATION":
        return ProviderError(
            "The DashScope credential pool has no authenticated credential.",
            code=code,
            details=details,
        )
    if code == "PROVIDER_PERMISSION_DENIED":
        return ProviderPermissionDenied(
            "The DashScope credential pool is blocked by provider permission.",
            details=details,
        )
    if code == "PROVIDER_ACCOUNT_SUSPENDED":
        return ProviderAccountSuspended(
            "The DashScope credential pool account is suspended.",
            details=details,
        )
    if code == "PROVIDER_QUOTA_EXHAUSTED":
        return QuotaExhausted(
            "The DashScope credential pool quota is exhausted.",
            details=details,
        )
    return ProviderError(
        "The DashScope credential pool is blocked.",
        code="PROVIDER_RESPONSE_INVALID",
        details=details,
    )
