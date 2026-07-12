# Image Resume Checkpoint

Date: 2026-07-12.

Status: implemented, verified, and pushed. Phase 2A image-library completion is
GO. No PDF, audio, video, UI, or handwriting-specific route was activated.

## Result

`Config(resume=True, output_dir=...)` now protects one completed ordered image
group from repeated provider, scout, review, or local-OCR work when publication
is interrupted. The state is a versioned sibling JSON file such as
`lecture_board.ocrllm-state.json`; it is removed after the final Markdown is
durable.

Vision resume supports exact built-in `DashScopeSettings`. Local OCR uses the
same lifecycle. Identity-less injected providers remain available for normal
recognition but are rejected for resume because their implementation/version
cannot be proven stable.

## Implemented Boundary

- Exact validated snapshot bytes are hashed with ordered original file URIs and
  byte counts.
- Canonical request identity binds image mode, unified profile, languages,
  built-in provider/model settings, local OCR confidence, preferences,
  execution limits, timeout, and JSON extra settings.
- API keys, credential-pool keys/IDs/health, output/temp/cache paths,
  progress/cancellation objects, and environment state are excluded.
- A strict `ocrllm.image-resume.v1` document stores the completed
  `ProcessorOutput`, its processor identity, sources, and final Markdown hash.
- State JSON is bounded to 16 MiB and rejects duplicate keys, invalid UTF-8,
  invalid numbers/types/hashes, missing/unknown fields, and unsupported schema.
- State is saved through a unique sibling temporary file, flush plus `fsync`,
  and atomic replace before the existing Markdown writer runs.
- Matching state without output republishes with zero recognition calls.
- Matching state plus matching output closes the crash window between final
  publication and state deletion with zero recognition calls.
- Output without state, changed source/order/config/processor, corrupt state,
  and edited output fail closed through public `ResumeStateError` codes.
- A deletion failure cannot remove or invalidate a durable final artifact; the
  retained matching sidecar remains safe for the next resume attempt.

An image group remains one completed unit. No intermediate model draft, scout,
or half-request is checkpointed, and no hidden retry or credential switch was
introduced.

## Robustness Evidence

Focused tests cover:

- built-in DashScope interruption then resume with exactly one provider call;
- local OCR interruption then resume with exactly one backend call;
- post-publication/pre-deletion crash recovery;
- existing output without state;
- changed source bytes, ordered group order, timeout, and OCR confidence;
- corrupt JSON, duplicate keys, oversized state, and edited final output;
- atomic state-save failure with no output or leaked temporary state;
- identity-less injected-provider rejection before invocation;
- explicit API key and credential-pool key/ID exclusion.

The final working-tree gates passed:

```text
Ruff: passed
focused resume/config/output/provider tests: 173 passed
complete pinned Pillow 12.3.0 suite: 987 passed, 1 skipped
generated Phase 1 fixtures: byte-identical
compileall: passed
resume/lightweight/provider boundaries: 71 passed
```

The exact pushed commit was archived, built, installed outside the repository,
and probed without network access:

```text
wheel bytes: 143072
wheel SHA-256: 1003840efc84f1a1732be60ca1d523aaab8420255501b689154acd1445ec773b
isolated installed bytes: 678804
installed interruption plus resume: one provider call total
installed sidecar secret check: passed
base metadata/native-extension budget: passed
outside-repo import: passed
forbidden eager imports: Pillow, pypdfium2, openai, httpx, threading absent
OCRLLM environment import wall median/p95/max: 49.82045/52.3505/59.9181 ms
OCRLLM environment import CPU median/p95/max: 46.875/62.5/62.5 ms
base Anaconda import wall median/p95/max: 35.84945/38.0548/38.4234 ms
base Anaconda import CPU median/p95/max: 31.25/46.875/46.875 ms
```

Two earlier installed-probe wrappers failed before library execution: the first
had an invalid PowerShell here-string terminator and the second lost a Python
string literal through Windows native-argument quoting. Base64-encoding the
inline probe source fixed the harness. These were recorded rather than hidden;
neither failure exercised the installed library. All temporary archive, wheel,
install, and probe directories were removed after each attempt.

## Work And Git Ledger

- `bb75039`: freeze the sidecar/identity/atomic lifecycle before code.
- `f7465db`: implement state contracts, hashing, strict parsing, atomic state,
  facade integration, public error, and robustness tests.
- Primary agent performed the implementation and tests. No subagent changed
  files in this slice.
- The existing atomic Markdown writer remained the sole final publisher. No
  separate atomic-writer agent changed it; resume composes it after state save.
- Private `docs/Textbook.pdf` and four screenshots remain untracked.

## Recovery Position

The complete user-authorized current step is finished: unified board/image
recognition, local OCR through the same function, adapter/model/preferences and
execution configuration, stable provider errors, fair DashScope credential
scheduling, and image resume are all implemented and verified. The original
scope explicitly excluded PDF, audio, video, and UI, so no later phase is active.
