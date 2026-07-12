# Provider Error Disposition Decision

Date: 2026-07-12.

Status: implemented at `54e2e72`; see
`provider_error_disposition_checkpoint_2026-07-12.md`. The checkpoint passes
before a credential pool or another built-in provider adapter begins.

## Problem

The existing provider errors distinguish authentication, rate, quota, timeout,
network, availability, and malformed response. That is insufficient for pool
and workflow decisions:

- invalid credentials are not the same as valid credentials lacking workspace
  or model permission;
- account suspension/billing delinquency is not exhausted task quota;
- concurrency saturation is not ordinary request-rate throttling;
- a provider-rejected request is not an opaque malformed response; and
- content-policy rejection should not be retried unchanged.

Using one generic 403/429 bucket would cause wasteful key rotation, repeated
paid calls, and misleading “network” or “upload” diagnoses.

## New Stable Provider Codes

Add these non-overlapping public codes and typed subclasses:

| Code | Public type | Default retry |
|---|---|---:|
| `PROVIDER_PERMISSION_DENIED` | `ProviderPermissionDenied` | no |
| `PROVIDER_ACCOUNT_SUSPENDED` | `ProviderAccountSuspended` | no |
| `PROVIDER_CONCURRENCY_LIMITED` | `ConcurrencyLimited` | yes |
| `PROVIDER_REQUEST_INVALID` | `ProviderRequestInvalid` | no |
| `PROVIDER_CONTENT_BLOCKED` | `ProviderContentBlocked` | no |

Existing codes keep their meaning. In particular:

- `PROVIDER_AUTHENTICATION` means missing, invalid, expired, or revoked
  credential;
- `PROVIDER_RATE_LIMITED` means retryable request/token/burst rate pressure;
- `PROVIDER_QUOTA_EXHAUSTED` means capacity that will not recover through an
  immediate retry or another key in the same quota domain;
- `PROVIDER_RESPONSE_INVALID` means the provider returned no safely usable
  success or a failure that cannot yet be classified.

Unknown errors stay `PROVIDER_RESPONSE_INVALID`. Do not guess retryability from
arbitrary exception text.

## Public Disposition

`get_provider_error_disposition(error)` returns one exact immutable
`ProviderErrorDisposition`:

```python
ProviderErrorDisposition(
    action="cooldown",
    scope="account",
    retryable=True,
)
```

Allowed actions:

- `retry`: transient provider/network failure; retry policy may later decide;
- `cooldown`: stop new work in the affected rate/concurrency domain;
- `quarantine_credential`: do not select this credential for the workflow;
- `stop`: wait for an external account/quota state change;
- `fix_request`: caller/config/model/request must change;
- `change_source`: content/policy input must change or be handled explicitly;
- `inspect_response`: unknown/malformed result needs developer/provider audit.

Allowed scopes are `request`, `credential`, `model`, `account`, and `provider`.
Adapters may attach only an allowlisted safe `failure_scope` detail. The generic
function never parses raw provider messages or credentials.

The initial mapping is:

| Stable code | Action | Default scope |
|---|---|---|
| authentication | quarantine credential | credential |
| permission denied | quarantine credential | credential |
| account suspended | stop | account |
| rate limited | cooldown | provider |
| concurrency limited | cooldown | provider |
| quota exhausted | stop | account |
| timeout/network/unavailable | retry | provider |
| request invalid | fix request | request |
| content blocked | change source | request |
| response invalid | inspect response | request |

This object describes policy evidence only. It does not sleep, retry, switch a
model, select a key, or mutate a pool.

## DashScope Classification

Use provider code first, then exact SDK type/HTTP status. Inspect a provider
message only as a private, bounded fallback for the documented concurrency
phrase when no distinct code exists; never store or echo that text.

- invalid/expired token and HTTP 401: authentication;
- `AccessDenied` families and SDK/HTTP 403: permission denied;
- arrearage/bill-overdue/account-not-good-standing families: account suspended;
- free-tier-only/free-quota/commodity-not-purchased families: quota exhausted;
- concurrency code/message families: concurrency limited;
- throttling/rate/burst/allocation/insufficient-quota 429 families: rate
  limited unless a more specific permanent quota or concurrency rule matched;
- `DataInspectionFailed`: content blocked;
- documented timeout codes before generic 5xx: timeout;
- 400/404/422 request/model/endpoint rejection: provider request invalid;
- 413/415 remain typed source failures;
- 409/5xx and SDK internal failures: unavailable.

DashScope rate and concurrency scopes default to `account`, because the
official documentation says limits aggregate across account users, workspaces,
and keys. Rotating another key in that account must not be represented as fresh
quota.

Primary current references:

- https://www.alibabacloud.com/help/en/model-studio/error-code
- https://www.alibabacloud.com/help/en/model-studio/base-url
- https://www.alibabacloud.com/help/en/model-studio/token-plan-faq

## Safety And Compatibility

- Error details remain recursively frozen and secret-key redacted.
- Provider codes and request IDs retain the existing strict safe-character and
  length allowlists.
- Raw exception/body/message content never enters public messages, details,
  results, logs, or evidence.
- Injected providers may raise the new typed errors; the injected-provider
  boundary reconstructs and redacts them exactly as it does existing types.
- The JSONL worker already transports stable error strings and retryability; no
  command or event schema field changes.
- Existing evidence remains historical. The quality workflow and successful
  provider request path do not change.

## Gate

Before GO:

- every code/type/default retryability and disposition row has direct tests;
- DashScope code/type/status precedence covers authentication, permission,
  suspension, rate, concurrency, quota, timeout, network, unavailable, invalid
  request, content block, source limits, and unknown response;
- hostile properties/messages cannot leak or execute unsafe overrides;
- injected-provider and worker error serialization accept every new code;
- full pinned tests, fixtures, Ruff, compilation, clean wheel/import budgets,
  and a clean installed mapping probe pass;
- no external provider request is needed or made.

Credential selection, cooldown clocks, retry counts, provider switching, and
resume remain later checkpoints.
