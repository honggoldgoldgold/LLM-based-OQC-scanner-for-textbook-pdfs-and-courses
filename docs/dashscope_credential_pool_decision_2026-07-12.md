# DashScope Credential Pool Decision

Date: 2026-07-12.

Status: implemented and verified by
`dashscope_credential_pool_checkpoint_2026-07-12.md`. This is scheduling and
health state, not automatic retry.

## Public Shape

```python
from ocrllm import (
    Config,
    CredentialPoolPolicy,
    DashScopeCredential,
    DashScopeCredentialPool,
    DashScopeSettings,
    VisionModelSettings,
)

pool = DashScopeCredentialPool(
    region="cn-beijing",
    credentials=(
        DashScopeCredential(credential_id="primary", api_key="..."),
        DashScopeCredential(credential_id="secondary", api_key="..."),
    ),
    policy=CredentialPoolPolicy(
        max_in_flight_per_credential=1,
        cooldown_seconds=60,
        selection_timeout_seconds=120,
    ),
)

config = Config(
    provider=DashScopeSettings(
        region="cn-beijing",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        credential_pool=pool,
    ),
    vision_model=VisionModelSettings(name="qwen3.7-plus-2026-05-26"),
)
```

`DashScopeSettings.api_key` and `credential_pool` are mutually exclusive. If
both are absent, the existing `DASHSCOPE_API_KEY` single-credential fallback
remains. A pool is region-bound and must match the settings region.

The pool is a separate stateful object referenced by immutable adapter settings.
Raw keys are never placed in Config as a tuple and are absent from repr,
reports, errors, and persisted state.

## Credential And Policy Values

`DashScopeCredential` is exact, frozen, slotted, and contains:

- a caller-selected, non-secret unique `credential_id`; and
- one secret `api_key`, omitted from repr.

Duplicate IDs and duplicate keys are rejected without echoing either key.
Coding Plan keys remain invalid for this OpenAI-compatible adapter.

`CredentialPoolPolicy` is exact, frozen, and bounded:

- `max_in_flight_per_credential`: `[1, 32]`, default `1`;
- `cooldown_seconds`: finite `[0, 600]`, default `60`; and
- `selection_timeout_seconds`: finite `(0, 600]`, default `120`.

The pool never creates threads. It coordinates caller/`recognize_batch()`
threads with one condition lock.

## Fair Selection

One acquisition chooses among eligible slots by:

1. lowest current in-flight count;
2. least-recent selection sequence; and
3. original credential order as a deterministic tie-break.

Selection increments in-flight state before releasing the lock. Completion or
failure decrements it and wakes waiters. When every healthy slot is at its
in-flight cap, the caller waits cancellation-aware until capacity appears or
the bounded selection timeout raises typed concurrency failure.

This provides fair round-robin behavior across serial work and balanced usage
under concurrent work. It does not claim multiple keys increase Alibaba Cloud
account quota; official limits aggregate across the account.

## Failure Updates

The adapter reports the final typed error to the lease exactly once. The pool
uses `ProviderErrorDisposition`:

- authentication/credential scope: quarantine only that credential;
- permission/model scope: block that model for this pool;
- permission/account scope, account suspension, or account quota exhaustion:
  block the account pool;
- rate or concurrency cooldown/account scope: delay all pool acquisitions;
- rate or concurrency cooldown/model scope: delay that model;
- rate or concurrency cooldown/credential scope: delay that slot;
- retry/provider, invalid request, content block, or response inspection:
  record the failure but do not change credential health.

The failing recognition raises its original error immediately. It is never
retried or switched inside the same call. A later independent call observes the
updated scheduler state.

Account/model blocks store only stable error codes. A blocked acquisition raises
a newly constructed redacted error of the same stable category. Cooldown waits
until recovery rather than rotating another key in the same account domain.

## Status Chart

`pool.snapshot()` returns immutable, ordered, secret-free slot reports with:

- credential ID;
- state: available, in-flight, cooldown, or quarantined;
- in-flight, selection, success, and failure counts;
- last stable error code; and
- rounded nonnegative cooldown remaining seconds.

The pool report also exposes region, account state/cooldown, and model blocks
without endpoint, key, request, or response content. Snapshot reads never load
an optional dependency or touch the network.

## Lifecycle And Cancellation

- Credential lease acquisition checks the Event-compatible Config cancellation
  signal at least every 50 milliseconds while waiting.
- A lease is closed in adapter cleanup even when client creation, request,
  parsing, cancellation, or client close fails.
- One lease cannot be completed twice.
- Unexpected adapter bugs release capacity but are recorded only as stable
  response-invalid failure at the public boundary.
- Pool state is in-memory only. Persistence, cross-process coordination, and
  resume are separate decisions.

## Gate

- exact value validation, secret/repr safety, duplicates, region matching;
- serial fairness proving selection does not restart at the first key;
- concurrent balance and in-flight caps;
- cancellation and bounded capacity timeout;
- credential quarantine, account/model block, and credential/model/account
  cooldown with no same-call retry;
- secret-free immutable status chart;
- adapter integration across primary and scout calls using the same pool;
- single-key/environment behavior byte-compatible when no pool is supplied;
- full pinned tests, fixtures, static/lazy checks, clean wheel/import, and an
  installed no-network pool probe;
- private assets remain untracked.

No automatic retry, model/provider switching, persistent pool state, Google/
Codex adapter, image resume, or later media work enters this checkpoint.
