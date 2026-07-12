# DashScope Credential Pool Checkpoint

Date: 2026-07-12.

Status: implemented, verified, and pushed. This is credential scheduling and
health memory, not automatic retry or provider fallback.

## Assumptions Revalidated

- Alibaba Cloud calls remain explicitly region-bound; current production
  examples use `cn-beijing` and its matching OpenAI-compatible base URL.
- Printed, projected, and handwritten images still use the single
  `board.v17` recognition workflow. The pool never selects a prompt, profile,
  or recognition route.
- One failed recognition is returned immediately. A different credential may
  be selected only by a later independent provider call.
- Multiple keys improve scheduling control but do not imply additional
  account-level quota.
- Private PDF and screenshot test inputs under `docs/` remain untracked.

## Paths Considered

Path A was to make a stateful credential collection masquerade as the complete
provider adapter. It would couple transport, endpoint, model, prompt workflow,
and credential health and make cold reading harder.

Path B was to keep immutable `DashScopeSettings` as adapter configuration and
reference a separate region-bound stateful scheduler. This was selected. It
keeps provider ownership explicit, preserves the single-key/environment path,
and lets one pool be shared by primary and omission-scout calls without adding
a second recognition workflow.

## Implemented Contract

- `DashScopeCredential` binds one non-secret operational ID to one API key;
  repr and errors never expose the key.
- `CredentialPoolPolicy` bounds per-key concurrency, cooldown, and selection
  wait time.
- `DashScopeCredentialPool` selects the least-loaded, least-recently-used slot
  with input order as a deterministic tie-break.
- Pool acquisition is cancellation-aware and uses caller threads only.
- Immutable `snapshot()` reports counters and health state without secrets.
- Credential quarantine and credential/model/account/provider cooldowns or
  blocks follow the stable `ProviderErrorDisposition` taxonomy.
- Recovery is explicit through credential, model, and account repair methods.
- `DashScopeSettings.api_key` and `credential_pool` are mutually exclusive and
  a pool must match the configured region.
- The adapter takes exactly one lease for each primary or scout request and
  closes it across SDK load, client creation, request, parse, cancellation,
  and cleanup failures.
- The existing single-key and `DASHSCOPE_API_KEY` fallback remain unchanged.

No retry loop, persistent pool state, cross-process scheduler, model fallback,
Google/Codex adapter, or resume behavior was added.

## Robustness Evidence

The focused tests cover exact validation, duplicate rejection, secret safety,
serial fairness, concurrent balancing and caps, cancellation, selection
timeout, credential quarantine and restore, model/account blocks and recovery,
all shared cooldown scopes, immutable status reports, primary/scout sharing,
and no same-call retry.

The final working-tree gates passed:

```text
Ruff: passed
targeted pool/config/adapter tests: 181 passed
complete pinned Pillow 12.3.0 suite: 975 passed, 1 skipped
generated Phase 1 fixtures: byte-identical
compileall: passed
lightweight import/provider boundaries: 59 passed
```

The first clean Git-archive wheel attempt correctly failed. The implementation
imported `validate_dashscope_api_key.py`, but the repository's broad
`*_api_key*` secret rule had ignored that source file. Working-tree tests could
not expose this because the file existed locally. Commit `a84bfb2` adds one
specific source-code exception while retaining the general secret rule, then
tracks the validator. This failure and repair are part of the checkpoint, not
discarded noise.

The rerun from exact pushed `HEAD` passed:

```text
wheel bytes: 130497
wheel SHA-256: c4ee5f9e4012a71aaa4df15c619bc100bbf1893792be4d361f017c1213c8faeb
isolated installed bytes: 622686
installed public pool probe: passed, first selection counts [1, 0]
base metadata/native-extension budget: passed
outside-repo import: passed
forbidden eager imports: Pillow, pypdfium2, openai, httpx, threading absent
OCRLLM environment import wall median/p95/max: 51.8566/55.9504/57.3752 ms
OCRLLM environment import CPU median/p95/max: 46.875/62.5/62.5 ms
base Anaconda import wall median/p95/max: 36.3125/38.6718/38.9137 ms
base Anaconda import CPU median/p95/max: 31.25/46.875/46.875 ms
```

The archive, wheel, install target, and probes were temporary and were removed
after verification.

## Work And Git Ledger

- `0cd2f56`: decision before implementation.
- `d4d444c`: scheduler, public values/reports, DashScope integration, and
  robustness tests. The pushed commit message records the complete gate.
- `a84bfb2`: clean-archive packaging repair and targeted verification.
- Primary agent performed this slice. No subagent changed files.
- No separate atomic-writer agent changed files. The existing atomic Markdown
  output path was not modified; the full suite verifies it remains intact.

## Recovery Position

The credential scheduler checkpoint is complete. The next mandatory Phase 2A
slice is image resume/checkpointing. Resume must compose the same `board.v17`
workflow and atomic final writer; it must not introduce handwriting-specific
state, prompt routing, automatic provider retry, PDF work, or legacy-app edits.

