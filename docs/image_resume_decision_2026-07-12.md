# Image Resume Decision

Date: 2026-07-12.

Status: active implementation decision. This completes Phase 2A; it does not
start PDF, audio, video, or a second handwriting workflow.

## Goal And Assumptions

An ordered image group is one recognition unit. The library cannot honestly
resume half of one provider or OCR inference call. It can durably preserve a
completed `ProcessorOutput` before final publication so an interruption or
output-write failure does not repeat any provider, scout, review, or OCR work.

Printed, projected, and handwritten inputs continue through the same
`board.v17` vision processor. Resume identity contains no content-class route.

## Paths Considered

Path A treats the final Markdown file as the resume marker. This is rejected:
it cannot prove source order, source bytes, model/prompt/config identity,
processor version, output integrity, or complete result metadata.

Path B uses a versioned sibling JSON sidecar containing source/request identity
and one completed image result, then keeps the existing atomic Markdown writer
as the only final publisher. This is selected because stale, corrupt, edited,
or mismatched work can fail closed before recognition.

## Scope

- `resume=False` remains byte-compatible.
- `resume=True` still requires `output_dir` and conflicts with `overwrite=True`.
- Vision resume supports exact built-in `DashScopeSettings`. Arbitrary injected
  provider objects are rejected because the current protocol exposes no stable
  implementation/version identity.
- Local OCR resume is supported by the same public facade and state lifecycle.
- A new resumable run with neither state nor output performs recognition once,
  saves the completed result atomically, publishes Markdown atomically, then
  deletes state.
- Matching state without output republishes the stored completed result with
  zero provider/OCR calls.
- Matching state plus matching output handles the crash window after publish,
  returns the stored result with zero calls, then deletes state.
- Output without state, corrupt state, source/config/processor mismatch, and a
  final-output hash mismatch fail closed.

## State And Identity

For final output `lecture_board.md`, state is the sibling
`lecture_board.ocrllm-state.json`. The exact state version is
`ocrllm.image-resume.v1`.

The state contains:

- ordered source file URI, byte count, and SHA-256;
- canonical request SHA-256;
- processor name and version;
- completed Markdown plus media type, profile, status, hotwords, warnings, and
  JSON metadata;
- final Markdown SHA-256.

The request identity includes source identity/order, image mode, resolved
profile, languages, model, provider region/base URL and output-affecting
DashScope flags, local OCR confidence, quality preferences, execution bounds,
timeout, and JSON `extra` settings. It excludes API keys, credential pool
contents/state, output/temp/cache locations, resume/overwrite flags, progress,
and cancellation objects.

State loading is strict and bounded. Unknown/missing fields, duplicate JSON
keys, invalid UTF-8/JSON/types/hashes, and unsupported versions raise
`RESUME_STATE_INVALID`. Correctly formed but different source, request, or
processor identity and edited final output raise `RESUME_STATE_MISMATCH`.
Neither error reports private Markdown, source paths, credentials, or raw JSON.

## Atomic Lifecycle

1. Preflight deterministic output/state paths and current source/request
   identity before optional provider/OCR work.
2. If reusable state exists, validate it and reconstruct `ProcessorOutput`.
3. Otherwise run the existing image processor exactly once.
4. Atomically save completed state including final Markdown hash.
5. If matching final output already exists, skip publication; otherwise call
   the existing atomic Markdown writer.
6. Delete validated state only after final output is durable.
7. Build the public result from the reconstructed or fresh processor output.

State-save or publication failure leaves no false successful result. A state
deletion failure after durable output is recoverable through the matching
state-plus-output path and must not destroy the final artifact.

## Gate

- vision and local-OCR interrupted-publication resumes make zero repeated calls;
- ordered source bytes/order, profile, model/provider settings, OCR confidence,
  preferences, safety limits, timeout, and extra settings are identity-bound;
- API keys and credential-pool keys/state never enter JSON, repr, or errors;
- corrupt/oversized/duplicate-key/schema-drift state and output hash edits fail;
- atomic state-save failure publishes no output; atomic Markdown behavior stays
  owned by the existing writer;
- matching state plus output completes the post-publish crash window;
- normal non-resume behavior and unified `board.v17` evidence remain unchanged;
- full pinned tests, fixtures, Ruff, compilation, clean wheel/import, and an
  installed no-network resume probe pass;
- private PDF/screenshots remain untracked.

No partial provider-pass checkpoint, automatic retry, model/key/provider
switching, persistent credential pool, cross-process lock, PDF/audio/video
state, worker wire change, legacy edit, or handwriting-specific state enters
this checkpoint.

