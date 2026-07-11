# Provider Cost And Reliability Policy

Status: user-confirmed operational policy.

Decision date: 2026-07-11.

This file records account-specific cost and reliability facts that influence
future provider selection. It does not make a deferred provider available and
does not replace the phase gates in `ocrllm_library_go_no_go.md`.

## Active Phase 1 Decision

- The user's Aliyun/DashScope API workflows use the Beijing region. For the
  current credential, use canonical region `cn-beijing` with the confirmed
  OpenAI-compatible endpoint
  `https://dashscope.aliyuncs.com/compatible-mode/v1`.
- Qwen image recognition is billed independently by usage. The fixed Phase 1
  quality gate is authorized to make exactly 13 zero-retry calls. A failed call
  is evidence; do not retry only that fixture or silently spend more quota.
- The Phase 1 model remains `qwen3.7-plus-2026-05-26` unless the authoritative
  decision is changed before collecting a new complete evidence set.

## Future Provider Inputs

These are user-supplied account facts, not universal pricing claims. Reconfirm
entitlements and current product terms before a large run.

- Aliyun FileTrans ASR is covered by the user's previously purchased token
  package plan and is suitable for large audio robustness tests without
  incremental usage cost under that account. FileTrans remains Phase 4 work;
  this policy does not authorize audio implementation during Phase 1.
- Google models are available without usage cost to the user but have been less
  stable. A future Google adapter must prove its own error and quality gates;
  price does not compensate for unreliable completion.
- The user describes Codex Mini 5.4 as inexpensive and very stable, but not
  free. Treat that name as a user-facing provider choice until a future adapter
  decision pins an exact API model identifier and verifies current availability.

## Library Architecture Consequences

- Do not hard-code prices, token-package balances, or free-tier assumptions in
  the recognition core. They drift and may be account-specific.
- Keep provider capability, cost preference, stability preference, rate policy,
  and media processing as separate responsibilities. A future execution-policy
  object may rank approved workflows, but it must not turn one `Config` into an
  implicit multi-provider state machine.
- Provider pools, automatic switching, Google, Codex, and FileTrans remain
  behind their phase decisions. Complete the current one-provider image gate
  before activating any of them.
- Every paid or quota-consuming evidence run records its exact call plan before
  dispatch and preserves failures rather than cherry-picking a better result.

## Change Rule

Update this file and the authoritative GO/NO-GO decision together when a
provider's billing, entitlement, model identifier, region, or observed
reliability changes. Never commit credentials or account balances.
