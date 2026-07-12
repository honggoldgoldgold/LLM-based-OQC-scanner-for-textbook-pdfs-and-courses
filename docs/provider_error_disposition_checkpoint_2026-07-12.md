# Provider Error Disposition Checkpoint

Date: 2026-07-12.

Status: GO for the public taxonomy, generic disposition, injected-provider
boundary, worker transport, and current DashScope adapter.

## Outcome

The public error contract now distinguishes:

```text
PROVIDER_AUTHENTICATION         invalid, expired, or revoked credential
PROVIDER_PERMISSION_DENIED      credential lacks workflow/model/workspace access
PROVIDER_ACCOUNT_SUSPENDED      billing or account state requires external repair
PROVIDER_RATE_LIMITED           retryable request/token/burst pressure
PROVIDER_CONCURRENCY_LIMITED    retryable concurrent-work saturation
PROVIDER_QUOTA_EXHAUSTED        non-immediate quota exhaustion
PROVIDER_TIMEOUT                request timed out
PROVIDER_NETWORK                provider could not be reached
PROVIDER_UNAVAILABLE            transient provider/model service failure
PROVIDER_REQUEST_INVALID        provider rejected request/model/endpoint parameters
PROVIDER_CONTENT_BLOCKED        provider policy rejected submitted content
PROVIDER_RESPONSE_INVALID       unknown, malformed, or unusable provider result
```

New public typed subclasses are:

- `ProviderPermissionDenied`;
- `ProviderAccountSuspended`;
- `ConcurrencyLimited`;
- `ProviderRequestInvalid`; and
- `ProviderContentBlocked`.

Every provider error can be passed to
`get_provider_error_disposition(error)`, which returns immutable
`ProviderErrorDisposition(action, scope, retryable)`. This is policy evidence,
not a retry/pool implementation.

## Disposition Contract

```text
authentication          quarantine_credential / credential
permission denied       quarantine_credential / adapter-defined domain
account suspended       stop / account
rate limited            cooldown / adapter-defined domain
concurrency limited     cooldown / adapter-defined domain
quota exhausted         stop / account
timeout/network/service retry / provider
request invalid         fix_request / request
content blocked         change_source / request
response invalid        inspect_response / request
```

DashScope attaches safe `failure_scope` evidence:

- ordinary auth and workspace permission: `credential`;
- model/endpoint permission: `model`;
- unpurchased service, suspension, quota, rate, and concurrency: `account`;
- invalid request/content: `request`; and
- timeout/network/service failure: `provider`.

This prevents a future pool from treating another key in one Alibaba Cloud
account as fresh rate or quota. The classification does not choose a key,
sleep, retry, switch models, or alter the current operation.

## DashScope Mapping

Provider code has precedence over generic HTTP/SDK classification:

- arrearage, prepaid/postpaid overdue, and account-suspended families become
  account suspension;
- free-tier-only, free-quota, and commodity-not-purchased families become
  exhausted quota;
- `DataInspectionFailed` becomes content blocked;
- concurrency code families or the bounded private official concurrency
  message become concurrency limited;
- throttling/rate/burst/allocation/insufficient-quota families remain retryable
  rate limiting unless a more specific permanent/concurrency rule matched;
- access-denied families become permission denied with credential/model/account
  scope;
- documented timeout codes precede generic 5xx;
- 400/404/422 become provider request invalid;
- 413/415 remain source failures; and
- unknown failures remain provider response invalid.

The message fallback is read only for concurrency classification, is limited to
1,024 exact-string characters, and is never stored or emitted. Hostile
`status_code`, `code`, `body`, `request_id`, and `message` properties are caught
without exposing their values.

Current primary references:

- https://www.alibabacloud.com/help/en/model-studio/error-code
- https://www.alibabacloud.com/help/en/model-studio/base-url
- https://www.alibabacloud.com/help/en/model-studio/token-plan-faq

## Boundary Integration

- Injected providers may raise the five new typed errors or expose their stable
  `code`; the boundary reconstructs a redacted public error.
- Worker `ErrorEvent` accepts all five new stable codes and their retryability
  without a wire schema change.
- Error details remain copied, recursively frozen, and secret-key redacted.
- Unknown injected exceptions still become nonretryable
  `PROVIDER_RESPONSE_INVALID`; local OS errors are not guessed to be network
  failures.
- Successful provider requests, board prompts, quality scoring, and results did
  not change.

## Verification

Decision commit `c33f64e` and implementation commit `54e2e72` are pushed.

- Focused errors/disposition/DashScope/injected/worker suite: 158 passed before
  the final scope refinement; the complete pinned suite below includes it.
- Authoritative isolated full suite with Pillow 12.3.0: 960 passed, 1 optional
  RapidOCR-profile test skipped.
- Phase 1 generated fixtures: byte-identical.
- Ruff over `src` and `tests`, `compileall`, `git diff --check`, and lazy public
  import: passed.
- Clean Git archive at `54e2e72` builds a 122,440-byte wheel with SHA-256
  `f12096a51b2b7aa34d216c1430a0c85e7a4753c49fb483404ec43163324ae001`.
- Its no-dependency target is 571,649 bytes.
- Thirty measured imports after two discarded warmups pass the budget: wall
  median/p95/max `43.90145/48.7949/50.7916` ms and CPU
  median/p95/max `46.875/46.875/46.875` ms.
- Installed no-dependency code independently mapped `Arrearage`,
  `Model.AccessDenied`, and a documented concurrency-allocation message to
  account suspension, model-scoped permission denial, and account-scoped
  concurrency cooldown respectively. Raw exception text did not cross the
  boundary.

No external provider/API HTTP request was made. Private screenshots and
`docs/Textbook.pdf` were not staged or redistributed.

## Next Boundary

The currently enabled DashScope adapter now has a stable pool-facing taxonomy,
so a separate credential scheduler checkpoint may begin. It must still define
fair rotation, secret ownership, concurrency safety, cooldown clocks, quota
domains, last-use state, and cancellation without placing a tuple of keys back
inside Config.

Google/Codex settings and adapters remain unimplemented and require their own
official error mappings before joining any pool. Image resume remains after the
pool checkpoint. Automatic retry/model/provider switching remains forbidden
until separately approved.
