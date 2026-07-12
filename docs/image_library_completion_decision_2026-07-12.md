# Image Library Completion Decision

Date: 2026-07-12.

Status: active. Local OCR, shared execution policy, adapter-owned
DashScope/model configuration, and provider error disposition are GO;
credential scheduling is current.

## Why The Roadmap Changes

The original user scope defines the current library step as image/board work,
including a no-LLM OCR mode through the same `recognize()` function, provider
workflow configuration, robust error classification, API credential pools, and
resumable work. It explicitly excludes PDF, audio, video, and UI from the
current step.

The earlier roadmap placed PDF immediately after the JSONL worker. Following
that order would leave explicit image-library requirements unfinished. Phase 3
therefore remains not started while a bounded **Phase 2A -- image library
completion** phase becomes active. Existing Phase 0/1/2 evidence and public
contracts remain valid.

## Mandatory Order

Phase 2A is implemented as independent vertical slices:

1. **Local OCR through `recognize()` -- GO.** Add an explicit recognition
   strategy, a maintained RapidOCR/ONNX Runtime adapter, typed local-OCR errors,
   deterministic Markdown, ordered multi-image handling, optional installation,
   and real offline screenshot evidence.
2. **Provider workflow configuration -- GO for the enabled adapter.** Separate immutable provider
   transport, model, execution, and recognition-preference policies. The shared
   `RecognitionExecutionPolicy` and adapter-owned DashScope/model checkpoints
   and provider error-disposition checkpoints are GO. Do not freeze the user's four examples as an
   exhaustive enum: OpenAI-compatible APIs, provider SDKs, Google SDKs, and
   Codex subprocess/session execution have different credential and lifecycle
   contracts.
3. **Credential pools -- current.** Add stateful fair rotation/cooldown only after each
   enabled provider category maps authentication, quota, rate limit,
   concurrency, invalid request, timeout, network, suspension, and malformed
   response failures into stable policy decisions. Do not broaden one immutable
   `api_key` field to an ambiguous scalar-or-tuple union.
4. **Image resume.** Define versioned source/config/result identity and atomic
   state before reusing any completed work. Resume must prove it avoids repeated
   provider/OCR work and rejects stale or corrupt state.

Only one slice is active at a time. Passing local OCR does not authorize pools
or resume prematurely.

## Local OCR Architecture Decision

The direct API remains:

```python
result = recognize(path_or_ordered_paths, config=config)
```

`Config.image_mode` chooses the recognition strategy:

- `"vision"` is the existing provider-backed unified `board.v17` workflow.
- `"ocr"` is local text detection/recognition with no API provider or network
  call.

OCR is a strategy, not an API provider. `provider="local_ocr"` is rejected
because it would mix execution mode with provider transport and make later
provider-pool policy ambiguous. `Config(image_mode="ocr")` constructs default
immutable RapidOCR settings; provider, API key, model, DashScope settings, and
LLM review/scout preferences are invalid in OCR mode.

The first real engine is the maintained `rapidocr` package with ONNX Runtime.
The obsolete `rapidocr_onnxruntime` import is not the new library dependency.
Official installation uses `rapidocr` plus `onnxruntime`, and the package ships
small detection/classification/recognition models:

- https://rapidai.github.io/RapidOCRDocs/main/install_usage/rapidocr/install/
- https://rapidai.github.io/RapidOCRDocs/main/install_usage/rapidocr/usage/
- https://rapidai.github.io/RapidOCRDocs/main/install_usage/rapidocr/parameters/

RapidOCR is isolated behind a private adapter. Its output classes, logging,
configuration names, and model paths are not public OCRLLM contracts.

## Local OCR GO Gates

Local OCR is GO only when all are true:

- `Config(image_mode="ocr")` reaches local OCR through the same public
  `recognize()` facade and makes no provider call.
- The default vision behavior and all Phase 1/2 fixtures remain byte-identical.
- `ocrllm[ocr]` installs maintained `rapidocr` and ONNX Runtime; neither is a
  base dependency or imported by plain `import ocrllm`.
- Missing dependency, backend initialization/inference failure, malformed
  backend output, and no retained text have distinct typed, secret-safe errors.
- PNG/JPEG, Unicode/spaces, caller order, confidence filtering, single/multiple
  images, optional atomic Markdown output, and snapshot cleanup have direct
  tests.
- RapidOCR logging is configured at `critical` so a library call does not write
  dependency chatter to stdout/stderr.
- Metadata reports engine/version, image/line counts, confidence aggregate,
  zero network/provider calls, and mode without storing source paths or raw
  boxes.
- At least two authorized untracked screenshots pass a real offline run. The
  evidence records hashes/counts, not private images or full recognized text.
- Documentation says local OCR is appropriate for inexpensive/offline text
  extraction but is not equivalent to the v17 vision workflow for formulas,
  tables, handwriting, or layout semantics.
- Full tests, fixture identity, compilation, Ruff, clean wheel, base import
  budgets, and a fresh `ocr` extra install pass.

The Phase 2 v1alpha1 worker remains DashScope-image-only. Adding OCR to the wire
contract requires a separately versioned command update after the direct API is
proven; it is not smuggled into the frozen v1alpha1 `provider="dashscope"`
shape.

## Recognition Execution Policy Checkpoint

`Config.execution` now owns immutable per-request image, parallel-job, and
provider-start cadence limits. Over-limit groups fail before source/provider
work, `recognize_batch()` bounds active futures and preserves result order, and
one monotonic gate covers every draft/review/scout call across a batch. The
first failure aborts provider calls that have not started. See
`phase2a_recognition_execution_policy_2026-07-12.md` for exact semantics,
verification, import budgets, and the next provider-configuration boundary.

The active provider/model migration is frozen in
`provider_workflow_configuration_decision_2026-07-12.md`. It replaces string
provider categories and duplicated DashScope fields with exact adapter settings
plus `VisionModelSettings`; it does not add a second provider or content route.
The implemented result and clean proof are in
`provider_workflow_configuration_checkpoint_2026-07-12.md`.

Provider error taxonomy and pool-facing disposition are GO, frozen in
`provider_error_disposition_decision_2026-07-12.md` and proven in
`provider_error_disposition_checkpoint_2026-07-12.md`. Credential scheduling
is the active checkpoint; no retry runtime is authorized by those decisions.
The concrete scheduler boundary is frozen in
`dashscope_credential_pool_decision_2026-07-12.md`.

## Explicit Do-Not-Do Items

- Do not start PDF, audio, video, UI, HarmonyOS, service, or Rust work.
- Do not import RapidOCR, ONNX Runtime, OpenCV, or NumPy during plain
  `import ocrllm`.
- Do not claim formula/layout fidelity from prose-oriented OCR evidence.
- Do not branch OCR behavior on handwriting versus board classification.
- Do not copy legacy processor or pool classes.
- Do not implement automatic model fallback or hidden retries in the OCR slice.
- Do not commit or redistribute the private PDF/screenshots.
