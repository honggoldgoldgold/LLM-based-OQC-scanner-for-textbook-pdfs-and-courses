# OCRLLM Library Go/No-Go Execution Decision

Status: active and authoritative.

Decision date: 2026-07-09.

This file is the execution contract for new work in `src/ocrllm/`. If another
planning document conflicts with this file, this file wins. Tests and runtime
trials establish evidence and gate status; they do not override a NO-GO or
deferred boundary. Only an explicit update to this decision can change a
boundary.

## Implementation Directive

Use the following as the prompt for every active-library change:

> Work only in the current phase. Preserve proven user-visible behavior, not
> legacy class or file structure. Write the public behavior and failure tests
> first. Put each function in a file named for that function and give each file
> one responsibility. Keep `import ocrllm` free of optional media, provider,
> GUI, server, and downloader imports. Do not claim a modality is supported
> until its GO gate passes with real input. Do not return success with empty
> Markdown, missing required artifacts, swallowed provider failures, or stale
> paths. Do not import from `legacy_app`. For active PDF work use PDFium through
> `pypdfium2`; do not add PyMuPDF. Stop when a required dependency, credential,
> license notice, fixture, or runtime proof is unavailable and record the
> blocker instead of substituting an untested design.

Before coding:

1. Read `START_HERE.md`, `MIGRATION_STATUS.md`, and this file.
2. Identify the current phase in `MIGRATION_STATUS.md`.
3. State which behavior is being preserved and which legacy files are only
   references.
4. State the pass/fail gate before editing.
5. Reject work that crosses a deferred or NO-GO boundary below.

After coding:

1. Run the phase's offline tests.
2. Run the phase's real smoke test when the gate requires one.
3. Build and install a wheel in an isolated target.
4. Prove `import ocrllm` did not load optional heavy modules.
5. Update `MIGRATION_STATUS.md` with commands, results, and remaining NO-GO
   items.

## Product Decision

GO:

- A Python-first recognition engine under `src/ocrllm/`.
- A small direct Python API.
- Optional image, PDF, audio, video, and provider dependencies.
- A versioned JSON-safe contract established before non-Python adapters depend
  on the engine.
- A one-job JSONL worker for Electron after the real image slice passes.
- PDFium through `pypdfium2` as the only active PDF rendering and text-layer
  engine.
- Porting one tested behavior slice at a time from the legacy app.

NO-GO:

- Copying legacy processors, provider clients, server modules, or configuration
  modules into `src/ocrllm/`.
- PyMuPDF, `fitz`, MuPDF, or another AGPL PDF engine in the active package.
- GUI, FastAPI, social downloader, browser automation, or launcher behavior in
  the core library.
- Returning placeholder Markdown or treating partial/missing required output as
  success.
- A Rust/PyO3 rewrite.
- A single bundle advertised as lightweight while it contains every modality,
  provider, GUI, server, and media dependency.
- Publishing empty extras such as `ocrllm[pdf-text]` before they install and
  enable a tested feature.

DEFERRED:

- HarmonyOS and ArkTS integration. Do not implement it in the active phases and
  do not claim compatibility. A future decision may evaluate an HTTP client or
  a separate native bridge after the Python, Electron, PDF, audio, and video
  contracts are stable.
- Browser React service integration. Preserve a JSON-safe contract now; build a
  service only after the core modalities are useful and a service product is
  explicitly requested. A browser React app cannot import a Python wheel
  directly, so no direct React compatibility claim is technically honest.
- Offline VLM/ASR models, GPU packages, Office documents, social downloads, and
  native/WASM engines.

## Current Truth

Phase 0 transition evidence and current Phase 1 implementation truth, as of
2026-07-10:

- Phase 0 is GO at commit `5018ad0`; Phase 1 is the current and only authorized
  implementation phase.
- The active package validates and decodes PNG/JPEG sources before invoking an
  injected provider, rejects empty provider output, returns canonical
  `source_type="image"`, and represents board recognition as `profile="board"`.
- The active image path snapshots validated source bytes for the provider. The
  provider call returns before snapshot cleanup begins, so providers must consume
  the paths synchronously and must not retain them. Snapshot creation/write and
  otherwise-successful cleanup failures raise typed `OUTPUT_WRITE_FAILED`; when a
  typed recognition failure is already active, it remains primary and records
  redacted `snapshot_cleanup_failed=true` detail.
- The built-in DashScope adapter and its offline boundary tests now exist. The
  injected and built-in `image.board.png`, `image.board.jpeg`, and
  `provider.dashscope.vision` implementations are `experimental`, not
  `available`. Offline checkpoint `e328253` supplies the licensed corpus,
  deterministic generators, scorers, and manifest-authenticated live-scoring
  gate, but the live smoke and two independent full runs have not happened.
  Phase 0 itself made no recognition capability available, and Phase 1 remains
  NO-GO.
- PDF, audio, and video remain unsupported by the active package.
- At the Phase 0 transition, package metadata had no base runtime requirements
  and advertised exactly `dev,image`. The current Phase 1 tree still has no base
  requirements and now advertises exactly `dev,image,dashscope`; `image`
  installs `Pillow>=10.4,<13`, and `dashscope` installs `openai>=2.30,<3`. No
  empty PDF, audio, video, or `all` extra is published. The Phase 0 wheel
  measurements below predate the `dashscope` extra and remain historical
  Phase 0 evidence.
- `Config` repr omits provider objects, `api_key`, `dashscope`, `pdf_password`,
  `progress`, `cancellation`, and `extra`. Boundary tests use unique sentinels so
  these values cannot leak through repr, public errors, or results.
- Every public `recognize()` call rejects `Config` subclasses and freshly
  revalidates the exact caller `Config` before source/provider work. Injected
  providers receive that original object identity. For a named built-in
  provider, image processing snapshots config as its first action, before
  provider/model resolution, prompt construction, or cancellation inspection;
  the adapter revalidates that isolated snapshot again. Nested
  `DashScopeSettings` are reconstructed at each snapshot, so callback mutation
  or `object.__setattr__` cannot diverge the request from its metadata or smuggle
  an endpoint past the allowlist.
- The current offline quality checkpoint is commit `e328253`. Its byte-frozen
  manifest is exactly `35,400` bytes with SHA-256
  `f0df9e7cd1dab282bec73a75717af150ecf34b3cd04567a2bef300b38a39df42`.
  It authenticates 20 committed artifacts, including 5 images, totaling
  `17,914,515` bytes with `8,299,885` bytes of headroom below the 25 MiB corpus
  ceiling. The checkpoint contains the exact licensed corpus, deterministic
  generators, provenance, per-language/token, critical-slot, formula, table,
  and ordered-anchor scorers, and integrated manifest-authenticated
  live-scoring gate.
- The scorer entrypoint authenticates the caller's manifest against a freshly
  strict-loaded byte-frozen manifest before scoring. It fails closed for
  non-applicable channels instead of treating missing evidence as a pass. On the
  pinned OCRLLM environment, the full offline suite passed `546` tests, the
  generator reproduced every committed generated image byte-for-byte, and
  `compileall` passed.
- The guarded evidence runner is committed at `fb23d1e` (full commit
  `fb23d1e40d4594ed1da8e244945ae7ccb9568efd`). Offline fake/evidence tests and
  direct no-network live preflight passed without a provider/API call. Preflight
  bound the strict manifest and artifacts, exact import origins, closed public
  signature, and clean Git identity for 98 tracked relevant files to that full
  commit.
- Phase 1 is still NO-GO solely because the caller has not supplied the
  credential's exact region and `base_url`, the fixed 13-call live plan has not
  run, its two complete six-dispatch runs therefore have no passing evidence,
  and the final clean-profile/GO-decision update is pending.
- Pushed packaging hotfix `3414f47` corrected a filename-ignore defect without
  weakening secret-ignore patterns. The legitimate
  `resolve_dashscope_api_key.py` / `resolve_dashscope_api_key` names matched the
  existing `*_api_key*` protection, so the hotfix renamed them to
  `resolve_dashscope_credential.py` / `resolve_dashscope_credential` and updated
  all imports, tests, and documentation. A clean Git-archive build from full
  commit `3414f47e5b44a6d5fe2023012ebf2cf361f96a61` produced a `50,094`-byte
  wheel; its isolated no-deps install passed an explicit test-key resolver
  round-trip without a provider network call.
- The historical Phase 1 adapter-only implementation checkpoint is commit
  `a6a8b18`. Its final offline gate passed `283` tests, `compileall`, and
  `git diff --check`. The wheel was `50,970` bytes with SHA-256
  `5502B5ED58D9D049F3640F3AF9AF5C4A8732426C14EA630D01125BD2556245AE`,
  `53` entries, no native/bytecode payload, and no base runtime requirement. Its
  isolated no-deps target was `233,115` bytes. Fresh CPython 3.10.20 and 3.14.3
  imports left `PIL`, `pypdfium2`, `openai`, and `httpx` unloaded.
- The clean `ocrllm[image]` empty-target install was `15,907,554` bytes and
  passed a generated-PNG recognition call through the injected-provider path
  with Pillow 12.3.0. The separate clean `ocrllm[image,dashscope]` empty-target
  install was `40,727,895` bytes, below the 64 MiB gate. Its offline adapter
  probe used Pillow 12.3.0, OpenAI 2.45.0, and HTTPX 0.28.1, constructed the real
  client with `max_retries=0`, and sent no HTTP request.
- The exact clean Phase 0 gate on the final phase-transition tree reported 141
  tests passed. The wheel was 31,151 bytes with SHA-256
  `FD983CA90944F545A4B670F33A8ABF015712E1DDAC8F866BB4703E0A465C707D`; its
  isolated no-deps target was 135,213 bytes, with no base requirements or native
  files. An outside-repository import reported version `0.1.0` and
  `forbidden modules []`.
- The same clean gate measured Python 3.10 fresh-import wall
  median/p95/max 58.6417/108.1609/114.8606 ms and process-CPU
  46.875/78.125/78.125 ms. Python 3.13 measured wall
  22.86505/30.8795/31.0431 ms and process-CPU 23.4375/31.25/31.25 ms.
- A fresh `ocrllm[image]` environment installed Pillow 12.3.0 with a
  15,814,896-byte delta. Pillow remained absent after base import, and a
  deterministically generated temporary PNG completed recognition through an
  injected provider.
- A real `qwen-vl-max` image call succeeded in an earlier isolated trial, but
  Alibaba now lists that model as legacy. The historical trial remains
  feasibility evidence only; it is neither the Phase 1 model baseline nor a
  capability gate.
- A Windows/Python 3.13 PDFium trial passed with pypdfium2 5.11.0 and PDFium
  151.0.7920.0: text extraction distinguished a text page from a raster-only
  page, both pages rendered at 1224 by 1584, and malformed input raised
  `PdfiumError` with error code 3. Python 3.10 installation remains a Phase 3
  gate.
- The tested Windows amd64 pypdfium2 wheel was 3,778,234 bytes compressed and
  8,306,352 bytes installed. Twenty warm-cache fresh-process imports had a
  98.442 ms median; the first cold-cache observation was 279.718 ms. This is an
  optional feature cost, not part of the base import budget.
- An earlier pre-Phase-0 baseline verification built a 9,283-byte wheel with
  SHA-256
  `166ACEC563B88203A7C8D1F616AB5838192D40501DC8837A5AA99B78EF865D0C` and
  installed to 26,152 bytes. Thirty measured fresh processes after two warm-ups
  gave CPython 3.10.20 wall median/p95 39.768/45.556 ms and CPU
  31.250/46.875 ms; CPython 3.13.5 gave wall 26.265/37.334 ms and CPU
  31.250/31.250 ms. Pillow, pypdfium2, and openai were absent from `sys.modules`
  after every base import; metadata had no base runtime requirement or native
  binary.
- The reference host for those import thresholds is Windows 11 Home x64 build
  10.0.26200, Intel Core i7-1260U, 16,890,388,480 visible bytes of RAM, using the
  two AMD64 CPython interpreters above. A different reference host must record
  its own baseline; it does not erase the absolute size or lazy-import gates.
- A later 20-process Python 3.10 repeat measured 48.978 ms median but one
  155.312 ms maximum and failed the draft maximum-100-ms rule. Because a single
  scheduler/antivirus outlier made that rule non-repeatable, the hard timing gate
  now uses 30 measured processes, median, and nearest-rank p95; maximum remains
  recorded diagnostic evidence rather than the pass/fail statistic.
- A subsequent post-build run reached 70.477 ms wall median and 108.311 ms p95,
  while a separate 30-process CPU/wall probe of the unchanged package measured
  Python 3.10 wall 36.382/40.744 ms median/p95 and CPU 31.250/46.875 ms. The gate
  therefore measures both process CPU and user-visible wall time: CPU catches
  package work; the wider wall ceiling tolerates bounded host scheduling noise.
- Direct installed distribution payloads already present on the reference host
  measured Pillow 12.2.0 at 16,070,317 bytes and pypdfium2 5.11.0 at 8,306,352
  bytes in the Python 3.13 environment, and openai 2.30.0 at 6,836,075 bytes in
  the Python 3.10 environment. Python 3.10 did not have pypdfium2 installed.
  These figures exclude transitive dependencies and therefore are evidence, not
  complete profile sizes.
- Legacy behavior is evidence only; it is not an active import or service
  boundary.

Therefore contract honesty is complete and real board/image work is the current
phase. The current phase is not PDF migration, audio migration, video migration,
service work, local-OCR work, or native work.

Capability status vocabulary is fixed:

- `available`: the implementation, packaging, deterministic tests, and required
  real gate all pass in the reported environment.
- `experimental`: deterministic tests pass, but a required live, packaging, or
  downstream proof remains.
- `unavailable`: implementation, dependency, configuration, or required proof
  is absent.
- `deferred`: intentionally outside the active phases.

Do not use `supported` as a synonym for `experimental`, `unavailable`, or
`deferred`.

Capability names are a fixed lowercase dot-separated registry, not free-form
marketing labels. Report atomic capabilities so one passing format cannot hide
another failing format. Initial names are:

```text
image.board.png
image.board.jpeg
provider.dashscope.vision
provider.dashscope.audio-short
provider.dashscope.filetrans
worker.jsonl.v1alpha1
worker.jsonl.v1alpha2
pdf.text
pdf.vision
pdf.text.resume
pdf.vision.resume
audio.short.wav-pcm-s16
audio.short.mp3-mpeg-layer3
audio.short.m4a-aac-lc
audio.long.wav-pcm-s16
audio.long.mp3-mpeg-layer3
audio.long.m4a-aac-lc
video.mp4-h264
video.mp4-h264-aac
```

Add a registry name in this file before implementing another profile, format,
codec, provider, or worker version. `get_capabilities()` returns every known
name with one four-state status and a concrete reason; it never reports an
aggregate `audio=available` when only one audio format passed.

`get_capabilities(config: Config | None = None)` performs no network call and
does not import optional packages. With `config=None`, it reports local
installation/gate state and reports built-in DashScope as requiring explicit
region/endpoint settings; `DASHSCOPE_API_KEY` presence cannot safely select a
region. With a named provider/model and `DashScopeSettings`, it evaluates that
exact configuration. An injected provider object proves protocol shape offline
but is `experimental` at most unless it exposes a stable capability identity
matching recorded live evidence. The worker `capabilities` command uses the
zero-argument semantics and never returns secret values.

Canonical transport media types are `image`, `pdf`, `audio`, and `video`.
`board` is an image recognition profile and prompt mode; it is not a transport
media type.

PDFium evidence sources:

- [pypdfium2 project, installation, and licensing](https://github.com/pypdfium2-team/pypdfium2)
- [pypdfium2 Python API and thread-safety rules](https://pypdfium2.readthedocs.io/en/stable/python_api.html)
- [PDFium license](https://pdfium.googlesource.com/pdfium/+/refs/heads/main/LICENSE)

## Runtime Boundaries

```text
Python caller
    -> ocrllm public facade
       -> source validation and routing
       -> one modality processor
       -> optional local helpers
       -> one provider capability
       -> RecognitionResult

Electron main process (after Phase 2)
    -> one-job JSONL worker
       -> the same ocrllm public facade

legacy_app
    -> behavior reference and compatibility app only
    -> never imported by src/ocrllm
```

The processor owns the modality workflow. A provider owns authentication,
request construction, response parsing, provider retry classification, and
provider error mapping. A local helper owns one conversion or inspection task.
An output helper owns one output operation. No layer may silently perform the
responsibility of another layer.

## Target File Responsibilities

Create files only when their phase begins. Do not create empty architecture
scaffolding.

### Public facade and contracts

```text
src/ocrllm/__init__.py
    Re-export documented public names only. No logic and no optional imports.

src/ocrllm/recognize.py
    Define recognize(). Validate, route once, call one processor, call output
    helpers if requested, and return one built RecognitionResult.

src/ocrllm/recognize_batch.py
    Define recognize_batch(). Preserve input order and apply explicit batch
    failure policy. Do not duplicate recognize().

src/ocrllm/config.py
    Define immutable caller configuration and compose provider-specific settings.
    No implicit file loading or network access.

src/ocrllm/validate_config.py
    Freshly validate one exact public Config while preserving its identity for
    injected providers.

src/ocrllm/snapshot_config.py
    Create an isolated freshly validated Config for a trusted built-in adapter.

src/ocrllm/raise_if_cancelled.py
    Inspect one Event-compatible cancellation signal and raise typed CANCELLED.

src/ocrllm/result.py
    Direct-Python compatibility re-export only after contract DTOs are added.

src/ocrllm/processor_output.py
    Define the internal immutable media type, complete/partial status, Markdown,
    artifacts, hotwords, warnings, and metadata returned by every processor.

src/ocrllm/build_recognition_result.py
    Combine one ProcessorOutput and optional final Markdown URI into the public
    RecognitionResult. Validate that every public artifact exists.

src/ocrllm/errors.py
    Define public typed failures. Messages must not contain secrets.

src/ocrllm/get_capabilities.py
    Define get_capabilities(config=None). Report what is installed, configured,
    and proven using exactly available, experimental, unavailable, or deferred.

src/ocrllm/contracts/image_recognition_request.py
    Define the exact `ocrllm.v1alpha1` image command, ordered image sources,
    DashScope provider/model, languages, board profile, and allowed options.

src/ocrllm/contracts/pdf_recognition_request.py
    Define the exact `ocrllm.v1alpha2` one-PDF command with nullable
    provider/model/profile and the allowed PDF/common options.

src/ocrllm/contracts/recognition_request.py
    Export only the ImageRecognitionRequest | PdfRecognitionRequest type union.
    Add a new concrete request file before extending this union.

src/ocrllm/contracts/source_descriptor.py
    Define one absolute RFC 8089 file URI and canonical image, PDF, audio, or
    video media type. Do not store provider objects or open file handles.

src/ocrllm/contracts/worker_protocol_version.py
    Define the exact `ocrllm.v1alpha1` | `ocrllm.v1alpha2` version union used by
    shared commands and events.

src/ocrllm/contracts/capabilities_command.py
    Define the version, `capabilities` command literal, and request ID.

src/ocrllm/contracts/cancel_command.py
    Define the version, `cancel` command literal, and active recognition ID.

src/ocrllm/contracts/recognition_result.py
    Define protocol_version, request_id, complete/partial status, Markdown,
    source media type, output URI, artifacts, warnings, and JSON-safe metadata.

src/ocrllm/contracts/artifact.py
    Define one final user-meaningful artifact URI, kind, and media type.

src/ocrllm/contracts/progress_event.py
    Define the `progress` event literal, request_id, stage, completed, total,
    and unit.

src/ocrllm/contracts/warning_event.py
    Define request_id, stable warning code, redacted message, and JSON-safe
    redacted details for degraded-but-successful work.

src/ocrllm/contracts/error_event.py
    Define the `error` event literal, nullable request_id, stable error code,
    redacted message, retryable flag, and JSON-safe redacted details.

src/ocrllm/contracts/capability_report.py
    Define one capability status and reason using the fixed four-state
    vocabulary.

src/ocrllm/contracts/accepted_event.py
    Define the `accepted` event literal and active request ID.

src/ocrllm/contracts/capabilities_event.py
    Define the `capabilities` event literal and capability reports.

src/ocrllm/contracts/result_event.py
    Define the `result` event literal and one RecognitionResult payload.

src/ocrllm/contracts/source_fingerprint.py
    Define source URI, byte size, and SHA-256 used to reject stale resume state.

src/ocrllm/contracts/completed_unit.py
    Define one completed page/segment/frame unit, ordered Markdown, artifact
    fingerprints, and JSON-safe metadata.

src/ocrllm/contracts/remote_task.py
    Define provider, task kind, remote task ID, source fingerprint, and exact
    submitted/running/succeeded/failed/cancelled state.

src/ocrllm/contracts/transcript_segment.py
    Define text, start/end seconds, BCP-47 language, confidence, and provider
    segment ID for one ordered segment.

src/ocrllm/contracts/transcription_result.py
    Define complete/partial status, ordered transcript segments, warnings, and
    JSON-safe metadata. It is structured data, not Markdown.

src/ocrllm/contracts/job_state.py
    Define `ocrllm.job.v1`, request fingerprint, processor/version, sources,
    completed units, remote tasks, and optional final Markdown SHA-256.
```

Initial stable error codes:

```text
SOURCE_NOT_FOUND
SOURCE_UNREADABLE
SOURCE_INVALID
SOURCE_TOO_LARGE
UNSUPPORTED_FORMAT
DEPENDENCY_MISSING
CONFIG_MISSING
CONFIG_INVALID
PROVIDER_AUTHENTICATION
PROVIDER_RATE_LIMITED
PROVIDER_QUOTA_EXHAUSTED
PROVIDER_TIMEOUT
PROVIDER_NETWORK
PROVIDER_UNAVAILABLE
PROVIDER_RESPONSE_INVALID
PDF_BACKEND_UNAVAILABLE
PDF_PASSWORD_REQUIRED
PDF_PASSWORD_INVALID
PDF_INVALID
PDF_PAGE_RANGE_INVALID
NO_SPEECH_DETECTED
OUTPUT_EXISTS
OUTPUT_PATH_INVALID
OUTPUT_WRITE_FAILED
RESUME_STATE_INVALID
RESUME_STATE_MISMATCH
CANCELLED
PROTOCOL_UNSUPPORTED
COMMAND_INVALID
WORKER_BUSY
REQUEST_NOT_ACTIVE
```

Processors may add structured redacted details, but callers must branch on the
stable code rather than message text.

The Phase 0 facade split is complete at commit `5018ad0`. Phase 1 builds on
`recognize.py`, `recognize_batch.py`, and `processors/recognize_images.py`; do
not recreate or expand the removed `api.py` or `processors/board.py` stubs.

### Source validation and routing

```text
src/ocrllm/detect_source_type.py
    Map an allowed extension to one canonical media type. Do not open content or
    call providers; the modality validator must confirm the content.

src/ocrllm/validate_source.py
    Enforce existence, regular-file status, readable size limits, and extension
    policy before processor or provider work.

src/ocrllm/validate_same_type_group.py
    Reject mixed groups passed to recognize(). Accept multi-source groups only
    for image recognition and preserve caller order; PDF, audio, and video
    accept exactly one source in their first approved slices.
```

### Image slice

```text
src/ocrllm/imaging/decode_image.py
    Read one caller or snapshot path into a bounded byte buffer.

src/ocrllm/imaging/decode_image_bytes.py
    Decode and validate exactly one bounded image byte buffer through Pillow.

src/ocrllm/imaging/decoded_image_info.py
    Hold only validated image dimensions, pixel count, and decoded format.

src/ocrllm/imaging/snapshot_image_group.py
    Copy an ordered image group into bounded provider-visible snapshots after
    validation. Yield stable paths only for the synchronous provider call, then
    remove them after that call returns. Map snapshot write/cleanup failures to
    typed errors without replacing an already-active typed recognition failure.

src/ocrllm/imaging/normalize_image.py
    Convert only formats the chosen provider cannot consume directly.

src/ocrllm/imaging/resize_image.py
    Enforce measured provider pixel and byte limits while preserving aspect.

src/ocrllm/profiles/build_board_prompt.py
    Build the board-recognition prompt from validated BCP-47 input/output
    languages. Do not call a provider.

src/ocrllm/processors/recognize_images.py
    Preserve ordered multi-image context, apply the selected image profile
    (initially board), call one vision capability, reject empty output, and
    return ProcessorOutput. Never write final output.
```

Do not port automatic crop, perspective correction, contrast, or HEIC behavior
until a failing representative fixture proves it is required. Then extract only
the needed operation into its own named file.

Initial image safety limits are 25 MiB per source, 24,000,000 decoded pixels per
image, 10 images per same-context group, 100 MiB aggregate source bytes, and
64,000,000 aggregate decoded pixels. For the Phase 1 OpenAI-compatible adapter,
read each validated snapshot and construct a MIME-correct Base64 data URL; never
put a local filesystem path in the remote JSON. Each complete data URL is at
most `10,000,000` UTF-8 bytes. The fully serialized provider JSON request,
including every data URL and the prompt, is at most 20 MiB (`20,971,520` bytes).
Validate every group member, complete data URL, and final serialized size before
the first provider call. Decode, normalize, and close images sequentially; never
retain the whole group's decoded pixel buffers. These are fixed version-1 caps,
not caller overrides.

The DashScope adapter also rejects before dispatch when either dimension is at
most 10 pixels, the long-side/short-side ratio exceeds 200:1, the longest side
exceeds `7,680` pixels, or the selected model's pixel/image limits are violated.
For the pinned
`qwen3.7-plus-2026-05-26` baseline with
`vl_high_resolution_images=true`, the initial provider ceiling is `16,777,216`
pixels per image. The repository's 10-image group cap remains the controlling,
stricter quantity limit. Decode and Base64-encode the same bounded byte buffer;
then recompute the final group's `64,000,000` aggregate-pixel cap from those
exact bytes. A caller-path or snapshot replacement must not create a
time-of-check/time-of-use bypass.

The provider receives only validated snapshot paths, not caller-owned paths.
Those paths remain valid until the synchronous provider method returns and are
deleted before `recognize()` returns or writes final output. A provider must not
return while background work still needs a snapshot. An otherwise-successful
cleanup failure is `OUTPUT_WRITE_FAILED`; if another typed failure is already
active, preserve it and attach only redacted cleanup-failure detail.

Phase 0 and Phase 1 accept `.png`, `.jpg`, and `.jpeg` only. Add BMP, WebP, TIFF,
HEIC, or HEIF only after a valid fixture passes decoder, provider, packaging,
and clean-install tests. HEIC/HEIF remains unavailable while no approved decoder
dependency exists.

`decode_image.py` opens with Pillow, reads dimensions, rejects nonpositive or
over-limit dimensions before full decode, runs `verify()`, reopens, and calls
`load()` inside a closed context. Map `UnidentifiedImageError`, truncated input,
and decoder failures to `SOURCE_INVALID`; map `DecompressionBombWarning` and
`DecompressionBombError` to `SOURCE_TOO_LARGE`. Do not change Pillow's global
pixel-limit setting.

### Quality test files

```text
tests/fakes/fake_vision_provider.py
    Return deterministic Markdown for processor and worker tests only.

tests/fixtures/phase1/manifest.json
    Byte-freeze licenses, hashes, languages, dispatches, expected content,
    critical slots, formulas, tables, and ordered anchors.

tests/quality/generators/generate_phase1_fixtures.py
    Regenerate four repo-owned images and byte-check them against the corpus.

tests/quality/load_fixture_manifest.py
    Strictly parse and validate the frozen Phase 1 evidence contract.

tests/quality/verify_fixture_artifacts.py
    Verify every artifact's path, size, hash, license, and corpus budget.

tests/quality/normalize_content_units.py
    Apply only the fixed NFKC, newline, whitespace, and declared-equivalence
    normalization rules.

tests/quality/calculate_language_token_metrics.py
    Calculate required-token recall and content-unit precision per language.

tests/quality/score_critical_slots.py
    Require exact identifiers, numbers, signs, units, names, and dates.

tests/quality/score_formula_signatures.py
    Compare formula identifiers, values, operators, relations, exponents, and
    subscripts.

tests/quality/score_table_cells.py
    Compare normalized cells by row and column coordinate.

tests/quality/score_ordered_anchors.py
    Require unique anchors to appear in source order.

tests/quality/score_recognition_result.py
    Integrate every Phase 1 scorer only after authenticating the supplied
    manifest against a freshly strict-loaded frozen manifest.

tests/quality/assert_quality_thresholds.py
    Apply only the frozen Phase 1 per-fixture and per-language thresholds.

tests/quality/run_phase1_quality.py
    Execute and checkpoint the guarded smoke plus two full Phase 1 runs.
```

These files stay outside `src/ocrllm` and do not add runtime dependencies.
Audio/video WER, CER, and timestamp scorers remain future phase work; do not
misread their quality contracts below as current files.

### Phase 1 evidence runner checkpoint

Commit `fb23d1e` freezes one 13-call plan: dispatch 0 is the clean-slide smoke,
then run A executes all six manifest dispatches, then run B independently
executes the same six. Both runner and SDK retry counts are zero. A provider,
identity, result-contract, or internal scorer failure aborts without another
call; a scored threshold failure is recorded and the already frozen plan
continues, never retries that fixture, and cannot be hidden by choosing a better
run.

The public live signature is exactly
`(region, base_url, evidence_path, confirm_paid_calls, repository_root)`. Its
real environment, recognizer, clocks, and Git identity reader are closed over
and cannot be injected through that interface. The private simulated entrypoint
accepts fakes for offline tests, records `mode="simulated"` plus every injected
dependency, and can set only `simulated_plan_passed`; it can never set
`phase1_gate_passed`. Even monkeypatching mutable module globals cannot turn
simulated output into live evidence.

At startup the runner verifies repository import origins, the strict byte-frozen
manifest and all artifacts, the code bundle, the clean Git HEAD/index/working
blobs for every relevant file, and `DASHSCOPE_API_KEY`. Before and after each
call it rechecks the applicable manifest, input, code/Git, and credential
invariants; final postflight repeats full artifact and import-origin checks. The
committed direct preflight at full commit
`fb23d1e40d4594ed1da8e244945ae7ccb9568efd` authenticated 98 tracked relevant
files and made no provider/API call. The CLI confirmation guard also rejects
any value other than 13 before settings or preflight; the recorded `12` check
exited safely, created no evidence, and made no call. An example shared endpoint
used by offline tests is not evidence of the caller's region or `base_url`.

The runner writes an initial checkpoint, a pre-call checkpoint naming the active
attempt and incremented invocation count, and a post-call checkpoint containing
raw Markdown, its byte count/hash, result metadata, elapsed time, and complete
serialized scorer metrics. Credential and full `base_url` values are rejected
from evidence. Each JSON update is written to a temporary file, flushed and
file-`fsync`ed; initial publication uses an exclusive hard link and later
updates use normal atomic `os.replace`. There is no explicit containing-directory
`fsync`, so this is the normal atomic link/replace guarantee, not a promise of
checkpoint persistence across sudden power loss.

Current Phase 1 provider-boundary tests are:

```text
tests/test_lightweight_import.py
    Keep PIL, openai, and httpx absent after plain public import.

tests/test_dashscope_settings.py
    Prove exact settings types, region/endpoint pairs, and nested copies.

tests/test_dashscope_provider_boundaries.py
    Prove model/key resolution, typed error precedence, Config snapshots,
    metadata, cancellation, and dependency/client boundaries.

tests/test_build_dashscope_image_request.py
    Prove ordered exact-buffer preflight, payload serialization, and all limits.

tests/test_dashscope_adapter.py
    Prove one no-retry raw-response call, strict parsing, cleanup, and redaction.
```

### Provider layer

```text
src/ocrllm/providers/vision_provider.py
    Define the vision capability protocol.

src/ocrllm/providers/short_audio_provider.py
    Define the synchronous short-audio capability protocol in Phase 4.

src/ocrllm/providers/long_audio_provider.py
    Define the submit, poll, and result-fetch lifecycle for resumable long audio
    in Phase 4.

src/ocrllm/providers/resolve_vision_provider.py
    Resolve an injected object or a documented built-in provider name. Never
    silently switch to a different paid provider.

src/ocrllm/providers/resolved_vision_provider.py
    Hold one resolved callable plus safe provider/model identity metadata.

src/ocrllm/providers/map_injected_provider_error.py
    Convert untrusted injected-provider failures into secret-safe public errors.

src/ocrllm/providers/validate_provider_markdown.py
    Require nonempty non-control-only text from any vision provider.

src/ocrllm/providers/dashscope/provider_settings.py
    Validate immutable routing and evidence-affecting settings without loading
    a credential, dependency, or network client.

src/ocrllm/providers/dashscope/resolve_dashscope_credential.py
    Resolve Config.api_key, then DASHSCOPE_API_KEY, and reject Coding Plan keys.

src/ocrllm/providers/dashscope/resolve_dashscope_model.py
    Accept only the Phase 1 floating alias or pinned snapshot and choose the
    pinned snapshot when Config.model is omitted.

src/ocrllm/providers/dashscope/build_dashscope_image_request.py
    Read exact snapshot bytes, validate provider limits, build ordered Base64
    data URLs plus prompt, and measure the JSON body before dispatch.

src/ocrllm/providers/dashscope/create_dashscope_openai_client.py
    Construct one synchronous OpenAI-compatible client with max_retries=0.

src/ocrllm/providers/dashscope/load_openai.py
    Lazy-load and version-check openai>=2.30,<3 or raise DependencyMissing.

src/ocrllm/providers/dashscope/parse_dashscope_raw_response.py
    Reject provider partial-response headers and parse the raw response safely.

src/ocrllm/providers/dashscope/parse_dashscope_image_response.py
    Require the requested model and one complete non-refusal assistant choice.

src/ocrllm/providers/dashscope/recognize_images.py
    Perform one DashScope vision request and parse one response.

src/ocrllm/providers/dashscope/transcribe_short_audio.py
    Perform one synchronous short-audio request and return TranscriptionResult.

src/ocrllm/providers/dashscope/submit_filetrans.py
    Submit one long-audio FileTrans task and return RemoteTask.

src/ocrllm/providers/dashscope/poll_filetrans.py
    Poll one persisted FileTrans task and return its updated RemoteTask.

src/ocrllm/providers/dashscope/download_filetrans_result.py
    Fetch and validate one terminal TranscriptionResult.

src/ocrllm/providers/dashscope/map_dashscope_error.py
    Map authentication, temporary rate limit, permanent quota/billing, timeout,
    network, service availability, invalid request, and malformed response to
    public errors.
```

Provider model queues and key pools are NO-GO until one-provider error handling
is complete and tests prove why the extra policy is needed.

Future provider architecture is recorded here without authorizing it:

- A recognition profile such as `board` describes the task and prompt; the
  execution engine is an orthogonal choice. A local OCR engine is neither a
  board profile nor an approved capability or active-phase task.
- Do not freeze four provider categories now. OpenAI-compatible transport,
  direct provider SDKs, local engines, and subprocess/session tools have
  different contracts and are not a closed current enum. In particular, a
  future Codex session/subprocess adapter cannot require an API key.
- If measured need later justifies richer configuration, immutable provider,
  model, execution, retry, and recognition-preferences policies stay separate
  from a stateful credential pool. Do not broaden `api_key` to a scalar-or-tuple
  field.
- A future credential pool requires an explicit decision covering fair
  selection, cooldown, and provider/model quota and error domains. It remains
  NO-GO until the single-provider path and its error classification are proven.

Phase 1 provider policy is concrete:

- The first vision adapter uses DashScope's OpenAI-compatible Chat Completions
  API through lazy `openai>=2.30,<3`. Do not add the DashScope SDK to the image
  path.
- For image recognition, `Config.provider` accepts an injected vision-capable
  object or the exact built-in name `"dashscope"`. `None` raises `ConfigError`;
  the library never initiates an implicit paid request. PDF `text` mode is local
  and requires no provider or API key.
- `Config(provider="dashscope")` requires an immutable `DashScopeSettings` with
  explicit `region` and full OpenAI-compatible `base_url`. Prefer the
  workspace-dedicated endpoint for that region. Validate the endpoint/region
  pair because API keys are region-specific; never infer a region or endpoint.
  Existing shared DashScope domains are accepted only when the caller explicitly
  selects the matching legacy endpoint.
- `DashScopeSettings` has exactly these Phase 1 fields: `region`, `base_url`,
  `enable_thinking=False`, and `vl_high_resolution_images=True`. Supported
  workspace regions are `ap-northeast-1`, `ap-southeast-1`, `cn-beijing`,
  `cn-hongkong`, and `eu-central-1`, using exact URL shape
  `https://{workspace-id}.{region}.maas.aliyuncs.com/compatible-mode/v1`.
  Explicit shared compatibility pairs are:

  | Region | Exact shared base URL |
  |---|---|
  | `ap-southeast-1` | `https://dashscope-intl.aliyuncs.com/compatible-mode/v1` |
  | `cn-beijing` | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
  | `cn-hongkong` | `https://cn-hongkong.dashscope.aliyuncs.com/compatible-mode/v1` |
  | `us-east-1` | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |

  Reject non-HTTPS URLs, ports, credentials, query/fragment text, alternate
  paths, unknown regions, and mismatched region/host pairs.
- Credential order is explicit `Config.api_key`, then `DASHSCOPE_API_KEY`, then
  `ConfigError`. Reject `sk-sp-` Coding Plan credentials because they cannot
  authorize this adapter.
- The built-in DashScope adapter uses `Config.model` when set and otherwise uses
  the pinned `qwen3.7-plus-2026-05-26` baseline. The exact allowlist is that
  snapshot plus the explicit floating alias `qwen3.7-plus`; every other model is
  `CONFIG_INVALID`. `qwen-vl-max` is legacy and must not be the default. Evidence
  for the pinned snapshot does not transfer to the floating alias. Invalid model
  text is never echoed in a public error message or detail.
- The initial quality request sets `enable_thinking=false` and
  `vl_high_resolution_images=true`. These choices remain subject to corpus
  evidence; changing either invalidates affected live evidence.
- Preserve caller image order, append the board prompt after every image, set
  `temperature=0`, and set `max_completion_tokens=16,384`.
- Default request timeout is 120 seconds.
- Perform no automatic model switch, key rotation, paid-provider fallback, or
  hidden retry in the first adapter.
- Construct the synchronous `OpenAI` client with `max_retries=0`; the SDK's
  built-in retry default is not allowed to create undisclosed extra paid calls.
- Map temporary throttling/HTTP 429 to retryable `PROVIDER_RATE_LIMITED`;
  permanent billing, purchase, and free-quota provider codes to nonretryable
  `PROVIDER_QUOTA_EXHAUSTED`; timeout to retryable `PROVIDER_TIMEOUT`; connection
  failure to retryable `PROVIDER_NETWORK`; and HTTP 409/5xx service failures to
  retryable `PROVIDER_UNAVAILABLE`. Inspect safe provider codes before generic
  status mapping so a permanent account limit is not mislabeled as
  authentication or temporary throttling. Provider codes `RequestTimeOut`,
  `InternalError.Timeout`, and `ResponseTimeout` map to retryable
  `PROVIDER_TIMEOUT` before generic 5xx handling. Do not perform the retry here.
- Add retry/backoff only in a later decision with retry-classification tests and
  cancellation-aware delays.
- Direct-Python cancellation is checked before provider preflight, between
  ordered image preflights, and immediately before dispatch. The synchronous
  adapter does not claim it can interrupt an in-flight HTTP call. Phase 2 adds
  hard cancellation by terminating the isolated worker job process.
- Call `chat.completions.with_raw_response.create` and treat the response as
  complete only when `x-dashscope-partialresponse` is absent or normalizes to
  `false`. Header value `true` or any other value is
  `PROVIDER_RESPONSE_INVALID`.
- Parsed output must report the exact requested model and exactly one choice
  with index 0, role `assistant`, `refusal=None`, and `finish_reason="stop"`.
  Any malformed shape, different model, refusal, non-text content, truncation
  such as `finish_reason="length"`, or final empty/control-only Markdown maps to
  `PROVIDER_RESPONSE_INVALID`. Never publish truncated Markdown as complete or
  partial success.
- Successful image metadata includes `provider`, `model`,
  `prompt_version="board.v1"`, `profile`, `image_count`, `provider_region`,
  `enable_thinking`, and `vl_high_resolution_images`; it never includes a key,
  endpoint credential, request body, or source content.
- Always close a constructed client. If request processing and close both fail,
  preserve the primary typed error and add only the safe boolean detail
  `provider_client_cleanup_failed=true`; a close-only failure is
  `PROVIDER_RESPONSE_INVALID`.

Primary evidence for this policy is Alibaba's [visual-understanding model and
limit reference](https://www.alibabacloud.com/help/en/model-studio/vision-model),
[OpenAI-compatible Chat Completions
reference](https://www.alibabacloud.com/help/en/model-studio/qwen-api-via-openai-chat-completions),
and [region/workspace base URL
reference](https://www.alibabacloud.com/help/en/model-studio/base-url), plus the
OpenAI Python client's [retry configuration](https://github.com/openai/openai-python#retries).

### PDFium slice

```text
src/ocrllm/pdf/require_pdfium.py
    Lazy-import pypdfium2, enforce the tested version range, and raise a typed
    dependency error. Do not open documents.

src/ocrllm/pdf/pdfium_lock.py
    Own the one process-wide lock that serializes every PDFium call.

src/ocrllm/pdf/inspect_pdf.py
    Validate/open one PDF, return JSON-safe page metadata, and close it.

src/ocrllm/pdf/extract_pdf_page_text.py
    Extract one page with get_text_bounded(), normalize it, and close text/page
    objects. Do not use get_text_range(), which cannot represent full Unicode.

src/ocrllm/pdf/calculate_pdf_render_scale.py
    Enforce DPI, longest-side, and total-pixel limits for one page.

src/ocrllm/pdf/render_pdf_page.py
    Render and losslessly encode one bounded page, close bitmap/page/document
    objects, and return one internal rendered-page descriptor.

src/ocrllm/pdf/rendered_pdf_page.py
    Define one temporary PNG path, one-based page index, width, and height. It is
    not a public Artifact and must be deleted after image recognition.

src/ocrllm/pdf/classify_pdf_page.py
    Future auto-mode classifier. Do not create this file until an auto-mode
    fixture corpus and gate are approved.

src/ocrllm/processors/recognize_pdf.py
    Validate page selection, call text extraction or compose the proven image
    processor with the board profile over rendered pages, add stable page
    markers, and return ProcessorOutput. Never write final output.
```

PDF rules:

- The verified optional dependency target is
  `pypdfium2>=5.11.0,<5.12` plus `Pillow>=10.4,<13`.
- CI locks the first implementation trial to pypdfium2 5.11.0 and records the
  bundled PDFium build before widening the range.
- `pypdfium2` imports only inside PDF modules.
- Do not call PDFium concurrently from multiple threads. Use serialized calls
  behind one process-wide lock. Use process-based parallelism only after
  benchmarks justify it; each process renders and saves its own page and returns
  only a path/descriptor, never a full bitmap through multiprocessing.
- Ship the pypdfium2, PDFium, and bundled dependency license notices with every
  binary distribution.
- PDFium's permissive license is the reason it replaces PyMuPDF here, but this
  decision is not blanket legal approval. If the exact wheel's notices/SBOM
  cannot be reproduced in the distributed artifact, PDF packaging is NO-GO.
- Initial internal render limits are 200 DPI, 4096 pixels on the longest side,
  and 16,777,216 rendered pixels per page. They are fixed in the first PDF
  contract; changing them requires boundary-test evidence and a decision update.
- Reject a PDF larger than 100 MiB or more than 500 pages with
  `SOURCE_TOO_LARGE` before rendering or provider calls. These are safety caps,
  not claims that a 500-page recognition job is cheap.
- Version 1 PDF modes are explicit: `text` or `vision`. Do not silently publish
  an `auto` mode before the classifier corpus passes.
- `text` mode fails if a selected page has no usable text unless the caller
  explicitly permits partial results.
- `text` mode preserves PDFium text in page order but does not claim paragraph,
  table, formula, or reading-order reconstruction. Callers requiring those use
  `vision` mode.
- `vision` mode renders every selected page and reuses the image provider path
  with the board profile.
- Start with lossless PNG page artifacts. JPEG remains NO-GO until formula,
  small-text, and handwriting accuracy is compared.
- Calculate render scale exactly as:

  ```python
  scale = min(
      dpi / 72,
      max_side / max(width_points, height_points),
      (max_pixels / (width_points * height_points)) ** 0.5,
  )
  ```
- Reject nonpositive page width or height as `PDF_INVALID` before calculating
  scale.
- Every page begins with `<!-- ocrllm:page index=N -->` in returned Markdown.
- Page indices in the public API are one-based. Internal PDFium indices are
  zero-based and must not leak.
- Check cancellation before opening and between pages. Do not claim that an
  in-process native render can be interrupted safely mid-call.
- Encrypted, malformed, empty, out-of-range, and oversized PDFs have typed
  failures before provider calls.
- Never return `PdfDocument`, `PdfPage`, `PdfTextPage`, `PdfBitmap`, or a PIL
  view backed by a live PDFium buffer across the PDF helper boundary. Copy or
  save the page before closing every native object.
- Direct Python Phase 3 fields are `pdf_mode`, `pdf_pages`, `pdf_password`, and
  `pdf_allow_partial`. `pdf_mode` is required; `pdf_pages=None` selects every
  page, otherwise pages are unique positive one-based indices in requested
  order. Passwords are never logged or echoed. `pdf_allow_partial` defaults to
  false.
- The Phase 3 worker extension is `ocrllm.v1alpha2`, not
  `ocrllm.v1alpha1`. It carries exactly one PDF `file:` URI and `profile=null`.
  Its `provider`/`model` are both `null` for PDF `text` mode; PDF `vision` uses
  `provider="dashscope"` and a model string or `null` for the documented default.
  Its only new option keys are `pdf_mode`, `pdf_pages`, `pdf_password`,
  `pdf_allow_partial`, and `resume`; unknown keys fail with `CONFIG_INVALID`.
  `resume` defaults false, requires a non-null `output_directory_uri`, and
  conflicts with `overwrite=true`. Add its JSON fixtures only after the Python
  PDF contract passes; do not alter the frozen `v1alpha1` image fixtures.

### Audio slice

```text
src/ocrllm/media/find_ffmpeg.py
    Locate ffmpeg and ffprobe or raise a typed dependency error.

src/ocrllm/media/probe_media_duration.py
    Return duration from ffprobe with a documented fallback and timeout.

src/ocrllm/media/convert_audio.py
    Convert unsupported provider input to a documented mono/sample-rate format.

src/ocrllm/media/split_audio.py
    Split long audio with explicit overlap and ordered segment metadata.

src/ocrllm/media/merge_transcript_segments.py
    Merge timestamped transcript segments in source order and mark partial gaps.

src/ocrllm/processors/recognize_audio.py
    Orchestrate the short or long provider flow, reject all-failed segments, and
    return the merged transcript in ProcessorOutput. Never write final output.
```

Preserve the legacy distinction between short ASR and resumable long FileTrans,
including persisted remote task IDs. Rewrite the implementation. Do not port the
2,000-line legacy processor, its inheritance, or its failure-text placeholders.
The Phase 4 trial set is WAV/PCM signed 16-bit, MP3/MPEG Layer III, and
M4A/AAC-LC. Do not advertise a format until its licensed fixture passes probe,
conversion, live provider, packaging, and cleanup gates. Hotword extraction is
deferred; `RecognitionResult.hotwords` remains empty in the first audio slice.
Provider adapters return `TranscriptionResult` with structured segments; do not
parse timestamps or task state back out of provider prose or Markdown.

### Video slice

```text
src/ocrllm/media/extract_video_audio.py
    Extract the audio track with ffmpeg and validate the output.

src/ocrllm/media/extract_video_frames.py
    Extract ordered candidate frames with timestamps.

src/ocrllm/media/deduplicate_video_frames.py
    Remove near-identical frames using a tested threshold.

src/ocrllm/media/merge_video_recognition.py
    Merge timestamped visual recognition and transcript streams in source order.

src/ocrllm/processors/recognize_video.py
    Compose the proven image and audio processors. Require the outputs requested
    by the caller, delegate ordered assembly without fabricating paths, and
    return ProcessorOutput. Never write final output.
```

Video does not own generic audio recognition, ffmpeg discovery, image decoding,
or provider retry policy. Video is NO-GO until the image and audio processors
are both GO. The first Phase 5 format is MP4 with H.264 video and optional AAC
audio. Do not advertise another container/codec pair until its own licensed
fixture passes probe, extraction, recognition, packaging, and cleanup gates.

### Output and resume

```text
src/ocrllm/output/build_output_path.py
    Build deterministic, Windows-safe names without overwriting by accident.

src/ocrllm/output/write_markdown_atomically.py
    Atomically write ProcessorOutput.markdown only when output_dir is set. It is
    called by the public facade, never by a processor or provider.

src/ocrllm/output/load_job_state.py
    Load explicit versioned resume state for long jobs.

src/ocrllm/output/save_job_state_atomically.py
    Atomically persist versioned resume state beside caller-selected output.

src/ocrllm/output/delete_job_state.py
    Delete validated state after final output is durable.

src/ocrllm/output/build_job_state_path.py
    Append `.ocrllm-state.json` to the final Markdown stem.

src/ocrllm/fingerprint_recognition_request.py
    SHA-256 canonical JSON for sources, processor/version, provider/model,
    languages, profile/mode, selection, and safety settings, excluding secrets,
    output location, progress, and cancellation objects.

src/ocrllm/freeze_json_value.py
    Deep-copy JSON mappings to MappingProxyType and arrays to tuples; reject
    unsupported objects and non-finite floats.

src/ocrllm/thaw_json_value.py
    Convert frozen JSON mappings/tuples to fresh dicts/lists for serialization.
```

Do not use package-relative output directories. Do not treat Markdown as the
only state store until task IDs, source hashes, processor version, and requested
phases can be represented and validated. A completed result must name only final
artifacts that exist.

Resume policy is fixed:

- Long processors may call job-state helpers at unit boundaries; only the
  public facade calls the final Markdown writer/result builder.
- `resume=False` is the default. `resume=True` requires `output_dir` and cannot
  be combined with `overwrite=True`.
- State is sibling JSON named `{final_markdown_stem}.ocrllm-state.json`; callers
  do not choose a hidden package/cache path in version 1.
- State version is `ocrllm.job.v1`. It stores source URI/size/SHA-256, canonical
  request fingerprint, processor name/version, ordered completed units, remote
  task IDs, and an optional final Markdown SHA-256. It never stores API keys,
  PDF passwords, environment values, or raw provider request headers.
- Completed-unit Markdown is plaintext beside the caller-selected output. The
  caller owns that directory's permissions. For an encrypted PDF, reopen and
  authenticate the unchanged source with the currently supplied password before
  reading or reusing state; a missing/wrong password fails even when hashes
  match. The request fingerprint stores only `password_supplied=true/false`,
  never the password.
- Save state after every completed page/segment and immediately after receiving
  a remote FileTrans task ID. A resumed run reuses only completed units whose
  source, request, processor, and artifact fingerprints all match.
- Corrupt state raises `RESUME_STATE_INVALID`. Any source/request/processor
  mismatch raises `RESUME_STATE_MISMATCH`; do not silently start over or reuse
  partial data.
- Before final output, save state with the final Markdown SHA-256, atomically
  write the Markdown, then delete state. If a crash leaves both files, matching
  hashes complete without provider work; a mismatch raises
  `RESUME_STATE_MISMATCH`.

Output policy is fixed for the initial image contract:

- `output_dir=None` writes nothing.
- A single image uses `{source_stem}_{profile}.md`.
- An ordered image group uses `{first_stem}_plus_{additional_count}_{profile}.md`.
- A PDF uses `{source_stem}_{pdf_mode}.md` (`text` or `vision`).
- Audio uses `{source_stem}_transcript.md`.
- Video uses `{source_stem}_video.md`.
- If the target exists and neither explicit resume nor `overwrite=True` applies,
  raise `OUTPUT_EXISTS`. Never overwrite or add an unreported suffix silently.
- Normalize the source stem to Unicode NFC, replace ASCII control characters
  and Windows-forbidden `< > : " / \\ | ? *` with `_`, strip trailing spaces and
  dots, use `source` if empty, and cap the stem at 96 Unicode code points.
  Profiles are registered internal ASCII slugs, never raw user filename text.
- An invalid/non-directory output location raises `OUTPUT_PATH_INVALID`.
- Atomic writes use a unique sibling temporary file, UTF-8, flush plus `fsync`,
  then `os.replace`. Remove the temporary file after a failed write and raise
  `OUTPUT_WRITE_FAILED` without reporting a final artifact.

### Electron worker

```text
src/ocrllm/worker/read_jsonl_command.py
    Read exactly one UTF-8 versioned command from stdin.

src/ocrllm/worker/write_jsonl_event.py
    Write accepted, progress, warning, result, or error events to stdout.

src/ocrllm/worker/run_worker_job.py
    Execute one recognition request in an isolated child process and relay its
    events.

src/ocrllm/worker/run_worker_control_loop.py
    Read commands, allow one child job, answer capabilities, and enforce the
    5-second cancellation process-tree kill.

src/ocrllm/worker/__main__.py
    Call the control loop with the production provider resolver. Parse no
    secrets from command-line arguments.

tests/worker_fixture_entrypoint.py
    Call the same control loop with a deterministic fake provider for the Node
    protocol harness. This file is test-only and is not a public provider.
```

Stdout is protocol-only. Diagnostics go to stderr. The Electron renderer never
spawns the worker and never receives provider credentials; the Electron main
process owns both responsibilities.

The initial protocol version is `ocrllm.v1alpha1`. Every stdin and stdout record
is one UTF-8 JSON object followed by `\n`; embedded newlines are JSON-escaped.
The worker accepts only these command shapes:

| `command` | Required fields | Behavior |
|---|---|---|
| `capabilities` | `protocol_version`, `command`, `request_id` | Return capability reports without starting recognition. |
| `recognize` | `protocol_version`, `command`, `request_id`, nonempty ordered `sources`, `provider`, `model`, `input_languages`, `output_language`, `profile`, `options` | Start one isolated recognition job. |
| `cancel` | `protocol_version`, `command`, active recognition `request_id` | Terminate that job's process tree within 5 seconds and emit `CANCELLED`. |

The worker emits only these event shapes:

| `event` | Required fields |
|---|---|
| `capabilities` | `protocol_version`, `event`, `request_id`, `capabilities` |
| `accepted` | `protocol_version`, `event`, `request_id` |
| `progress` | `protocol_version`, `event`, `request_id`, `stage`, `completed`, `total`, `unit` |
| `warning` | `protocol_version`, `event`, `request_id`, `code`, `message`, `details` |
| `result` | `protocol_version`, `event`, `request_id`, `result` |
| `error` | `protocol_version`, `event`, `request_id`, `code`, `message`, `retryable`, `details` |

For `ocrllm.v1alpha1`, `request_id` is a canonical UUID string; every source is
an absolute RFC 8089 `file:` URI with media type `image`; `provider` is exactly
`dashscope`; and `profile` is exactly `board`. The only option keys are:

| Option | Type and default |
|---|---|
| `output_directory_uri` | Absolute `file:` URI or `null`; default `null`. |
| `overwrite` | Boolean; default `false`. |
| `timeout_seconds` | Number in `(0, 600]`; default `120`. |

Missing options use those defaults. Unknown keys fail with `CONFIG_INVALID` and
are never ignored. Provider credentials are absent from commands, arguments,
stdout, and results. The Electron main process passes `DASHSCOPE_API_KEY` only
in the worker environment.

At most one recognition is in flight; a second `recognize` command returns
`WORKER_BUSY`. Cancelling a different ID returns `REQUEST_NOT_ACTIVE`. An
unsupported version returns `PROTOCOL_UNSUPPORTED`. Invalid JSON or an invalid
command returns `COMMAND_INVALID`; `request_id` is `null` only when no valid ID
can be recovered. During Phase 2, invalid/unsupported input errors use the
worker's own `ocrllm.v1alpha1` as the output `protocol_version`. The control loop
continues reading `capabilities` and `cancel` while recognition runs.

## Legacy Migration Matrix

| Legacy area | Preserve | Rewrite in active library | Reject or defer |
|---|---|---|---|
| `processors/board.py` | Ordered image context and nonempty Markdown outcome | `recognize_images.py`, validation, profiles, provider call, ProcessorOutput construction | Processor class, inheritance, implicit output |
| `imaging/preprocess.py` | Only operations proven by failing fixtures | One operation per named file | Wholesale preprocessing pipeline |
| `imaging/pdf_renderer.py` | Page order, selection, bounded render size | Entire renderer with PDFium/pypdfium2 | PyMuPDF/fitz implementation |
| `processors/pdf.py` | Text-versus-vision modes, page markers, resumable long work | Entire processor as composition over PDFium and the image path | RapidOCR in first PDF slice, legacy inheritance, empty success |
| `processors/audio.py` | Short/long split, timestamps, FileTrans task-ID resume | Probe, convert, split, submit, poll, merge as separate files | Failure text presented as transcript, processor class |
| `processors/video_pipeline.py` | Ordered phase semantics and timestamped frames | Composition over image/audio/media helpers | Fabricated artifact paths, success with missing required phase |
| `core/llm_client.py` | Provider capability concepts and typed quota intent | Small provider adapters and public error mapping | Monolithic client, global fallback policy, broad catches |
| incremental writer/checkpoints | Resume after interruption and atomic writes | Explicit versioned job state and atomic output helpers | Package-hidden state and unverified Markdown-only checkpoints |
| `api/server.py` | Submit/status/cancel concepts as product research | A future separately authorized service | Current server, wildcard CORS, arbitrary host paths, in-memory jobs |
| GUI, CLI launchers, social processors | Nothing required by core recognition | Nothing | Keep in `legacy_app` only |
| Codex and Google modes | Behavior reference only | Future optional adapters after a real gate is approved | Phase 1 implementation |

Migration means reusing a tested behavior statement and fixture. It never means
copying a legacy file and renaming imports.

## Recognition Quality Evidence

Commit `e328253` provides the licensed Phase 1 recognition corpus, deterministic
generators, exact scorers, and integrated manifest-authenticated live-scoring
gate. Its byte-frozen manifest is `35,400` bytes with SHA-256
`f0df9e7cd1dab282bec73a75717af150ecf34b3cd04567a2bef300b38a39df42`.
The 20 authenticated artifacts include 5 images and total `17,914,515` bytes,
leaving `8,299,885` bytes below the 25 MiB limit. The pinned full suite passed
`546` tests, the generator byte-identity check passed, and `compileall` passed.
The integrated scorer
strict-loads the frozen manifest again, requires exact manifest equality, and
fails closed for non-applicable score channels before it can apply thresholds.
The guarded evidence runner is committed separately at `fb23d1e`; its offline
fake/evidence tests pass without a provider/API call.

That offline evidence does not make image recognition `available`. Phase 1
still has no live clean-slide smoke or two independently dispatched full-corpus
runs. It remains NO-GO solely pending the caller's exact region and `base_url`,
the runner's 13 live calls and two passing full runs, and the final
clean-profile/GO-decision update. PDFium remains only a backend feasibility
spike; PDF, audio, and video recognition remain unavailable under their later
gates.

The user-supplied screenshots currently present under `docs/` are local,
supplemental, non-redistributable, and remain untracked. Keep them uncommitted.
They may support manual inspection but cannot be scored gate fixtures, modify
thresholds, or supplement the committed licensed Phase 1 corpus in pass/fail
evidence.

Rules for every recognition-quality gate:

- Keep scorers and fixtures under root `tests/`; never modify or import legacy
  tests. The committed corpus is at most 25 MiB. Generate long audio and
  synthetic video locally from committed licensed components.
- Before a live run, commit a manifest containing fixture ID, SHA-256, source or
  deterministic generator, SPDX license or explicit repo-owned permission,
  redistribution status, BCP-47 languages, expected content units, critical
  values, and expected timestamps. Do not use private legacy outputs or
  unverified downloaded course material.
- Normalize scorer input with Unicode NFKC, normalized line endings, and
  collapsed whitespace. Case-fold only fields declared case-insensitive. Never
  discard digits, decimal points, signs, relations, units, exponents, or
  subscripts. Declare equivalent forms such as `×` and `\times` before a run.
- `required_token_recall = matched_expected_tokens / expected_tokens`. Critical
  identifiers, numbers, signs, units, dates, and names require accuracy `1.00`.
- `content_unit_precision = matched_expected_units / recognized_scored_units`.
  The manifest may exclude neutral Markdown scaffolding declared before the
  run, but not arbitrary explanatory prose added after seeing output. Any
  unreferenced identifier, number, sign, relation, unit, date, table data cell,
  or formula term is a critical false insertion and fails the fixture.
- Formula signatures compare identifiers, numbers, operators, relations,
  exponents, and subscripts against predeclared equivalents. Table scoring uses
  normalized `(row, column)` cells; a correct value in the wrong cell fails.
- Latin speech uses conventional word error rate. CJK speech uses character
  error rate. Report each language independently. Timestamp error is absolute
  recognized-versus-reference boundary error; report median and maximum.
- Thresholds apply per fixture and per language. A corpus average cannot hide a
  failed handwriting, formula, table, or language fixture. Scorer unit tests
  must deliberately alter digits, signs, cell coordinates, order, and
  timestamps and prove those outputs fail.
- Offline fake-provider tests prove validation, routing, scoring, ordering,
  errors, and artifacts, but not recognition. One live smoke proves auth,
  transport, parsing, and nonempty output, but permits `experimental` at most.
  `available` requires two independently dispatched full-corpus live runs, and
  every fixture must pass in both runs. Do not retry only failed fixtures or
  select the better run.
- Record hashes, provider/model, request configuration, prompt/profile version,
  dependency versions, UTC time, elapsed time, and every metric. Never record
  secrets. A provider, model, prompt, preprocessing, render, segmentation, or
  frame-cadence change invalidates affected live evidence.
- Never use another LLM as the pass/fail judge. A threshold failure is NO-GO;
  fix the implementation or explicitly narrow product scope instead of lowering
  a threshold after seeing the output.

### Phase 1 image quality corpus

Checkpoint `e328253` commits the required five fixtures: a synthetic
English/Simplified-Chinese slide with at least 50 scored text units and 8
critical slots; a deterministic perspective, glare, and JPEG derivative; a
CC0/repo-owned handwritten board with at least 25 units and 5 critical slots; a
synthetic board with at least 10 formulas; and a synthetic table with at least
20 data cells, full headers, and 5 critical numeric cells. The frozen dispatch
plan also scores one ordered two-image request with unique first/last anchors.

Both full live runs must meet all of these:

- Printed-slide token recall is at least `0.95` and content-unit precision at
  least `0.90`; handwriting recall is at least `0.85` and precision at least
  `0.85`; critical-slot accuracy is `1.00` on every fixture.
- Formula-signature accuracy is at least `0.90`, with every equality,
  inequality, sign, exponent, subscript, and critical numeric value correct;
  formula content-unit precision is at least `0.90`.
- Table cell accuracy by coordinate is at least `0.95`; all row/column headers
  and critical numeric cells are exact, with no unexpected data cell and no
  row/column transposition.
- The ordered request contains all unique anchors and their first appearances
  follow source order. Markdown is nonempty, but prose/whitespace is not compared
  byte-for-byte.

These results authorize only the tested provider, model, profile, languages,
and fixture classes. They do not prove general handwriting, formula, table, or
language accuracy.

### Phase 3 PDF quality corpus

Keep separate capability evidence for `pdf.text` and `pdf.vision`. Use a
deterministic selected/unselected-page text PDF with at least 100 Latin tokens,
100 CJK characters, supplementary-Unicode sentinels, rotation, and crop boxes;
the mixed text/raster PDF; and a vision PDF generated from the Phase 1 printed,
handwriting, formula, and table fixtures. Encrypted, malformed, empty, and
oversized fixtures are functional failures, not quality-score inputs.

Text-mode acceptance requires token recall at least `0.99` on every selected
text page and content-unit precision at least `0.99`; exact critical values and
Unicode sentinels; one ordered one-based page marker per selected page; no
unexpected critical insertion or anchor from an unselected page; and identical
content units on repeated runs with the pinned PDFium build. A raster-only page
must fail or be named in an explicitly requested partial result. Text mode does
not claim semantic formula/table reconstruction or human reading order.

Vision-mode acceptance requires each page to pass the matching Phase 1 absolute
threshold and score no more than `0.05` below the corresponding direct-image
score from the same run. Critical values remain exact; markers, anchors, and
sections remain in page order. One live smoke and two independent full vision
PDF runs must pass, recording render limits, PDFium build, provider, and model.

### Phase 4 audio quality corpus

Use redistributable real `en-US`, `zh-CN`, and code-switching clips totaling at
most 180 seconds, with at least 100 English words, 150 Chinese characters, and
12 human-checked utterance boundaries. Derive long audio by concatenating the
licensed clips with one-second silences and unique spoken segment IDs. Add
silence and corrupt fixtures for failure behavior.

Both full live runs must meet all of these:

- English WER and Chinese CER are each at most `0.15`; code-switch Latin WER and
  CJK CER are each at most `0.20`; names, numbers, units, and segment IDs are
  exact.
- Short-audio timestamp median error is at most `0.75 s` and maximum `1.50 s`.
  Long-audio WER/CER is at most `0.20`, timestamp median at most `1.00 s`, and
  maximum `2.00 s`.
- Every long-audio segment ID occurs exactly once in order. Partial results name
  missing segments; all-failed input is an error. Silence returns
  `NO_SPEECH_DETECTED`, never invented text or empty success.
- One short live smoke and one FileTrans live smoke pass. If the provider cannot
  supply the required timestamp granularity, timestamp-preserving audio is
  NO-GO; do not fabricate timestamps from order.

### Phase 5 video quality corpus

Generate a deterministic 36-second 1280x720 MP4 with three 12-second H.264
slides, hard cuts, unique slide IDs, scored text, a formula, a table, and six
timestamped licensed utterances. Add one redistributable 60-90 second lecture
excerpt with at least three annotated visual changes, 30 visual content units,
100 spoken words or 150 CJK characters, one formula/table, and eight timeline
events.

With a fixed two-second cadence, the synthetic clip must represent all three
slides, remove duplicates, preserve slide/utterance IDs exactly once in order,
and pass the Phase 1 visual plus Phase 4 audio thresholds. Visual-event error is
at most `2.00 s`; merged-event median is at most `1.00 s` and maximum `2.00 s`.

Both independent real-video live runs require visual token recall at least
`0.90`; formula/table accuracy at least `0.90`; exact critical values and
headers; English WER or CJK CER at most `0.20`; every annotated stable scene;
selected-frame precision at least `0.80`; exact event order; timestamp median at
most `1.00 s` and maximum `2.00 s`; and both requested streams plus final
existing artifacts. Cancellation/resume tests are separate and cannot count as
completed quality evidence.

## Go Gates By Phase

Only one phase may be active at a time.

Capability status and phase advancement are separate decisions:

- An atomic capability becomes `available` when its own implementation,
  packaging, deterministic, and live-quality subgate passes. It does not wait
  for unrelated optional formats in the same phase.
- A phase advances only when every mandatory capability below passes plus every
  cross-cutting bullet in that phase. A phase may remain active while one
  capability is already available.
- Phase 1 mandatory capabilities are `image.board.png`, `image.board.jpeg`, and
  `provider.dashscope.vision`. Phase 2 requires `worker.jsonl.v1alpha1`.
- Phase 3 requires `pdf.text`, `pdf.vision`, `pdf.text.resume`,
  `pdf.vision.resume`, and `worker.jsonl.v1alpha2`; track each status separately
  even though all are mandatory for phase advance.
- Phase 4 requires the WAV/PCM-S16 short and long capabilities plus
  `provider.dashscope.audio-short` and `provider.dashscope.filetrans`. MP3 and
  M4A short/long capabilities are optional atomic subgates; a failure leaves
  only that exact name unavailable and does not block Phase 5.
- Phase 5 requires both `video.mp4-h264` and `video.mp4-h264-aac`.
- Phase 0 is a contract gate and makes no recognition capability available.

### Phase 0: Contract honesty -- GO at `5018ad0`

GO when all are true:

- `ocrllm[image]` installs `Pillow>=10.4,<13`; Pillow is imported lazily only
  when validating/decoding an image.
- Missing, unreadable, empty, oversized, unsupported, and invalid image inputs
  fail before provider invocation.
- Empty provider output fails.
- Provider exceptions are typed and secret-safe.
- Config repr/error/result tests use unique sentinels for provider object, API
  key, PDF password, and provider `extra`; no sentinel appears in output. Event
  sentinel proof is N/A in Phase 0 because event DTOs do not exist; it begins
  with the Phase 2 event contracts.
- `RecognitionResult` metadata is JSON-safe and immutable to callers. Tests
  mutate the caller's original nested dict/list and attempt mutation through the
  result; neither can change stored state.
- Result/source tests use canonical media type `image`; `board` appears only as
  a recognition profile.
- Output collision policy is explicit and tested.
- Empty PDF, audio, video, and all extras are removed from package metadata.
- The isolated base wheel/target and fresh-process import probes pass every Base
  numeric budget in `Dependency Profiles` on both recorded Python versions.

GO is recorded by the exact clean evidence in `Current Truth`. Regress Phase 0
to NO-GO if any condition above stops passing.

### Phase 1: Real board/image -- current

GO when all are true:

- Offline tests use valid PNG/JPEG files, not arbitrary bytes.
- Tests hit one-below/at/one-above every per-image, aggregate-source,
  aggregate-pixel, group-count, complete-data-URL, and serialized-request cap and
  prove rejection occurs before provider invocation. DashScope tests also cover
  both dimensions around the greater-than-10-pixel minimum, the 200:1 aspect
  ratio, `7,680`-pixel longest side, selected model's pixel limit, and final
  exact-buffer aggregate-pixel recheck.
- A committed, licensed five-class corpus contains the handwriting, projected
  slide, mixed text/formula, table, and ordered multi-image fixtures. Local user
  screenshots remain untracked, supplemental, and uncommitted.
- One lazy real provider adapter passes authentication, quota, timeout,
  temporary-rate-limit, unavailable-service, malformed/truncated response,
  pre-dispatch cancellation, endpoint/region validation, Config mutation,
  exact-model/raw-header parsing, client-cleanup precedence, metadata, and
  redaction tests. It constructs `OpenAI(max_retries=0)`; its synchronous
  in-flight call is documented as non-interruptible. Injected providers keep
  caller Config identity; the built-in adapter uses a freshly validated isolated
  copy.
- One live feasibility smoke returns nonempty structured Markdown for the clean
  slide; this permits `experimental` at most.
- The committed Phase 1 scorer rejects its deliberate corruptions, and two
  independently dispatched full-corpus runs pass every image threshold in
  `Recognition Quality Evidence` without per-fixture retries. Both runs use the
  pinned `qwen3.7-plus-2026-05-26`, `enable_thinking=false`, and
  `vl_high_resolution_images=true`, unless a replacement configuration is
  explicitly decided before collecting new evidence. Truncation fails the run.
- A committed evidence runner passes no-network tests, authenticates the frozen
  manifest and artifacts before dispatch, writes evidence atomically, and
  performs exactly one clean-slide smoke followed by two independent complete
  six-dispatch runs. Any call failure invalidates its complete run; it never
  retries only a failed fixture.
- Plain `import ocrllm` does not import Pillow, the provider SDK/client, or
  transitive `httpx`.
- Clean Image and Image + DashScope installs pass the 25 MiB and 64 MiB profile
  budgets.

Status after offline checkpoint `e328253`, packaging hotfix `3414f47`, and
runner checkpoint `fb23d1e`: the corpus, generators, artifact authentication,
scorers, deliberate-corruption tests, guarded evidence runner, provider
boundary, lazy import, and clean profile work are integrated. The pinned full
suite reports `546 passed`; generator bytes and `compileall` pass, with no
provider/API call. Phase 1 remains **NO-GO solely** because the caller has not
supplied the exact region and `base_url`, none of the 13 required paid no-retry
calls has been recorded, the two full six-dispatch runs therefore have no
passing live evidence, and the final clean-profile/GO-decision update remains.

### Phase 2: JSON contract and Electron worker

GO when all are true:

- Frozen JSON fixtures cover all three commands and all six event shapes,
  including literals, nullable invalid-command request IDs, defaults, unknown
  option rejection, and the fallback protocol version.
- A Node harness launches the worker without a shell and validates every stdout
  line. Offline schema/result tests launch `tests/worker_fixture_entrypoint.py`;
  one opt-in live smoke launches `python -m ocrllm.worker` with DashScope.
- Chinese, emoji, spaces, and long Windows paths round-trip.
- Cancellation stops provider and child media processes within the declared
  5-second grace by terminating the isolated recognition job process tree. The
  test fails if the job or any descendant remains alive after 5 seconds.
- Phase 2 is development-only and requires an explicitly configured Python
  executable. Do not claim end-user Electron compatibility until the Phase 6
  clean-machine packaged-worker gate passes.

### Phase 3: PDFium PDF

GO when all are true:

- `ocrllm[pdf-text]` installs pypdfium2 without Pillow;
  `ocrllm[pdf-vision]` installs pypdfium2 plus Pillow.
- The first reproducible CI lock is pypdfium2 5.11.0 and Pillow 12.2.0.
- The full backend fixture suite passes in clean Windows AMD64 CPython 3.10 and
  3.13 environments. A passing 3.13 spike does not waive the 3.10 gate.
- A clean environment can open, text-extract, and render with PDFium.
- Fixtures cover text-layer, image-only scan, formula-heavy, mixed-language,
  encrypted, malformed, empty, and out-of-range selection cases.
- Fixtures also cover CJK plus supplementary Unicode, rotation, crop boxes,
  transparency, correct and incorrect passwords, and a huge-page pixel limit.
- On a mixed text/scanned fixture, `text` mode fails at the raster-only selected
  page unless the caller explicitly permits a partial result; `vision` mode
  renders every selected page. `auto` remains deferred.
- Text and vision modes preserve page order and page markers.
- `pdf.text` passes every deterministic text-corpus threshold and `pdf.vision`
  passes both independent full-corpus live runs in `Recognition Quality
  Evidence`. Track the two capability statuses separately.
- Vision mode composes the Phase 1 image path with the board profile; it does
  not implement a second vision client.
- PDFium calls are serialized or process-isolated; no unsafe threaded calls.
- A deterministic five-page fake-provider run is interrupted after page two;
  resume makes zero new calls for pages one/two and produces the same ordered
  final Markdown as an uninterrupted run. Separate tests reject corrupt state,
  changed source bytes, changed page selection/model/profile/processor version,
  missing state artifacts, a mismatched final-output hash, and resume of an
  encrypted PDF with a missing or incorrect password.
- `ocrllm.v1alpha2` Node fixtures prove PDF `resume` default/conflict rules and
  the sibling state-file URI round-trip.
- Wheel/application artifacts contain required PDFium dependency notices.
- Plain `import ocrllm` does not import pypdfium2 or Pillow.
- Clean PDF text and PDF vision + DashScope installs pass the 35 MiB and 96 MiB
  profile budgets.
- Windows can delete the source and temporary page files immediately after
  document/bitmap closure.
- A deterministic 120-page PDF is processed twice sequentially. Peak working
  set stays below 512 MiB; after garbage collection, process handles are no more
  than baseline plus 5; and post-pass private bytes grow by no more than 64 MiB
  from pass one to pass two. All source/temp files are immediately deletable.

### Phase 4: Audio

GO when all are true:

- Licensed speech, multilingual speech, silence, corrupt, and long-audio
  fixtures exist.
- Short ASR and long FileTrans each pass a real opt-in provider test.
- The audio scorer rejects deliberate transcript/timestamp corruptions, and two
  independently dispatched short/long corpus runs pass every WER/CER,
  critical-slot, timestamp, and ordering threshold in `Recognition Quality
  Evidence`.
- WAV/PCM signed 16-bit passes short/long probe, conversion, live transcription,
  packaging, and cleanup tests; this is mandatory for phase advance.
- MP3/MPEG Layer III and M4A/AAC-LC are optional atomic subgates. List each
  short/long name as available only after its own probe, conversion, live
  transcription, packaging, and cleanup tests pass; failure does not block the
  phase.
- All-failed segments fail the job; partial success is explicit.
- Timestamps and segment order survive merge.
- FileTrans task IDs survive interruption without duplicate submission.
- A fake FileTrans run stops immediately after atomic task-ID persistence; the
  restarted run polls the same ID with zero new submissions. Corrupt state and
  changed source/provider/model/segmentation settings fail explicitly.
- Missing ffmpeg/ffprobe produces a typed capability error.
- The clean Audio Python install delta is at most 64 MiB; ffmpeg is measured and
  reported separately as an external capability.

### Phase 5: Video

GO when all are true:

- Video reuses the Phase 1 image and Phase 4 audio processors.
- MP4/H.264 with no audio and MP4/H.264 with AAC audio each pass probe,
  extraction, recognition, packaging, and cleanup tests. No other
  container/codec pair is advertised by this phase.
- A synthetic clip proves deterministic extraction and ordering.
- A licensed real lecture excerpt proves frame selection, visual recognition,
  audio transcription, merge, cancellation, resume, and cleanup.
- A deterministic fake-provider run interrupted after one completed frame
  resumes without re-extracting/re-recognizing completed units; changed source,
  frame cadence, provider/model, or processor version rejects state.
- The video scorer rejects deliberate frame/order/timestamp corruptions, and
  two independent real-lecture runs pass every visual, speech, selection, and
  timeline threshold in `Recognition Quality Evidence`.
- Requested visual/audio results cannot be missing from a successful result.
- Returned artifact paths exist and are final.
- The clean Video Python install delta is at most 64 MiB; ffmpeg is not bundled.

### Phase 6: Distribution and downstream proof

GO when all are true:

- Base, image, PDF, audio, video, provider, and worker profiles have recorded
  wheel/bundle size, installed-size delta, cold start, and peak memory, and each
  passes the numeric budget recorded below or a stricter budget added before
  that phase's implementation.
- A clean Python project imports the wheel without `legacy_app`.
- A clean Electron test app consumes the packaged worker.
- An SBOM and third-party license-notice bundle are produced.
- GUI, FastAPI, social downloaders, and unused modalities are absent from
  feature-specific bundles.

HarmonyOS remains deferred after Phase 6 unless a new decision explicitly
activates it.

## Dependency Profiles

Target extras, created only in their phase:

```text
ocrllm                 Public facade and injected fake-provider tests.
ocrllm[image]          Phase 0: Pillow>=10.4,<13 for lazy decode validation.
ocrllm[pdf-text]       pypdfium2>=5.11.0,<5.12 only.
ocrllm[pdf-vision]     pypdfium2>=5.11.0,<5.12 plus Pillow>=10.4,<13.
ocrllm[dashscope]      Phase 1 vision starts with lazy openai>=2.30,<3.
ocrllm[audio]          Not created until the Phase 4 spike identifies and tests
                       exact Python requirements; ffmpeg stays external.
ocrllm[video]          Not created until Phase 5; it includes approved audio
                       requirements and does not bundle ffmpeg.
ocrllm[all]            Only after every included extra is individually GO.
ocrllm[dev]            Tests, build, lint, and fixture tools.
```

The current Phase 1 metadata declares exactly `dev`, `image`, and `dashscope`;
the later extras in this target list do not exist yet. The base distribution has
no runtime requirements.

The base target uses fresh-process imports after two discarded warm-ups, not an
unmeasured cold-cache claim. The actual hard budgets are:

| Profile | Installed-size budget | Import/bundle rule |
|---|---:|---|
| Base | Wheel <= 256 KiB; no-deps target <= 1 MiB | Zero base runtime requirements, zero native binaries, no PIL/pypdfium2/openai/httpx imports; 30 measured fresh processes after two warm-ups. Wall median <= 100 ms and p95 <= 200 ms; process-CPU median <= 60 ms and p95 <= 100 ms. Record maxima diagnostically. |
| Image | Clean installed delta <= 25 MiB | Pillow remains lazy. |
| Image + DashScope | Clean installed delta <= 64 MiB | Pillow, openai, and transitive httpx remain lazy on base import. |
| PDF text | Clean installed delta <= 12 MiB | pypdfium2 remains lazy; Pillow is absent. |
| PDF vision | Clean installed delta <= 35 MiB | pypdfium2 and Pillow remain lazy. |
| PDF vision + DashScope | Clean installed delta <= 96 MiB | Same lazy-import rule; no second vision client. |
| Audio | Python installed delta <= 64 MiB | ffmpeg is an external capability, not bundled. |
| Video | Python installed delta <= 64 MiB | Reuses audio; ffmpeg is not bundled. |

The self-contained Electron worker bundle has no proven size budget yet. Phase
6 is NO-GO until a packaging spike records its runtime, provider, and image
profile sizes and this decision approves a numeric bundle ceiling. Do not call
that bundle lightweight before the ceiling exists and passes. A small base
wheel does not make a media or application bundle lightweight.

## Verification Commands

The exact pinned offline corpus/scorer checkpoint checks are:

```powershell
uv run --no-project --isolated --with 'Pillow==12.3.0' `
  --with 'pytest>=8,<10' --with 'openai>=2.30,<3' `
  --python 'D:\Anaconda\envs\OCRLLM\python.exe' `
  python -m pytest -q -p no:cacheprovider
if ($LASTEXITCODE -ne 0) { throw "pytest failed" }
uv run --no-project --isolated --with 'Pillow==12.3.0' `
  --python 'D:\Anaconda\envs\OCRLLM\python.exe' `
  python -m tests.quality.generators.generate_phase1_fixtures --check
if ($LASTEXITCODE -ne 0) { throw "generated fixture bytes drifted" }
& 'D:\Anaconda\envs\OCRLLM\python.exe' -m compileall -q src tests
if ($LASTEXITCODE -ne 0) { throw "compileall failed" }
```

Do not simplify the generator command to the base environment's bare Python.
That environment currently has Pillow 12.1.1; the frozen image bytes were
verified with the explicit Pillow 12.3.0 overlay above.

For packaging hotfix `3414f47`, the clean-source proof used this method rather
than the working directory:

```powershell
$proofRoot = Join-Path $env:TEMP ("ocrllm-3414f47-" + [guid]::NewGuid())
$archivePath = Join-Path $proofRoot 'source.zip'
$archiveRoot = Join-Path $proofRoot 'source'
$wheelDir = Join-Path $proofRoot 'wheel'
$targetDir = Join-Path $proofRoot 'target'
New-Item -ItemType Directory -Path $proofRoot | Out-Null
New-Item -ItemType Directory -Path $archiveRoot, $wheelDir, $targetDir | Out-Null

git archive --format=zip --output=$archivePath 3414f47
if ($LASTEXITCODE -ne 0) { throw "git archive failed" }
Expand-Archive -LiteralPath $archivePath -DestinationPath $archiveRoot
uv run --no-project --isolated --with 'build>=1.2' `
  --python 'D:\Anaconda\envs\OCRLLM\python.exe' `
  python -m build --wheel --outdir $wheelDir $archiveRoot
if ($LASTEXITCODE -ne 0) { throw "clean archive wheel build failed" }
$wheel = Get-ChildItem -LiteralPath $wheelDir -Filter *.whl | Select-Object -First 1
if ($null -eq $wheel) { throw "wheel build produced no wheel" }
& D:\Anaconda\envs\OCRLLM\python.exe -m pip install --no-deps --target $targetDir $wheel.FullName
if ($LASTEXITCODE -ne 0) { throw "isolated wheel install failed" }

$env:OCRLLM_WHEEL_TARGET = $targetDir
Push-Location $env:TEMP
try {
    & D:\Anaconda\envs\OCRLLM\python.exe -I -c "import os,sys; sys.path.insert(0,os.environ['OCRLLM_WHEEL_TARGET']); from ocrllm import Config; from ocrllm.providers.dashscope.resolve_dashscope_credential import resolve_dashscope_credential; key='offline-package-probe'; assert resolve_dashscope_credential(Config(provider=object(),api_key=key)) == key"
    if ($LASTEXITCODE -ne 0) { throw "isolated credential resolver probe failed" }
} finally {
    Pop-Location
    Remove-Item Env:OCRLLM_WHEEL_TARGET -ErrorAction SilentlyContinue
}
```

Result: full commit `3414f47e5b44a6d5fe2023012ebf2cf361f96a61`,
wheel size `50,094` bytes, isolated explicit-key round-trip passed, and no
provider network call was made.

For a future committed active-library checkpoint, run the complete clean gate
from the repository root. The tests exercise the working tree; the packaging
steps intentionally archive `HEAD`, so do not report the combined result as a
clean checkpoint until the intended changes are committed:

```powershell
$sourceArchive = Join-Path $env:TEMP ("ocrllm-source-" + [guid]::NewGuid() + ".zip")
$sourceRoot = Join-Path $env:TEMP ("ocrllm-source-" + [guid]::NewGuid())
$wheelDir = Join-Path $env:TEMP ("ocrllm-wheel-" + [guid]::NewGuid())
$targetDir = Join-Path $env:TEMP ("ocrllm-target-" + [guid]::NewGuid())
New-Item -ItemType Directory -Path $sourceRoot, $wheelDir, $targetDir | Out-Null

uv run --no-project --isolated --with 'Pillow==12.3.0' `
  --with 'pytest>=8,<10' --with 'openai>=2.30,<3' `
  --python 'D:\Anaconda\envs\OCRLLM\python.exe' `
  python -m pytest -q -p no:cacheprovider
if ($LASTEXITCODE -ne 0) { throw "pytest failed" }
uv run --no-project --isolated --with 'Pillow==12.3.0' `
  --python 'D:\Anaconda\envs\OCRLLM\python.exe' `
  python -m tests.quality.generators.generate_phase1_fixtures --check
if ($LASTEXITCODE -ne 0) { throw "generated fixture bytes drifted" }
& 'D:\Anaconda\envs\OCRLLM\python.exe' -m compileall -q src tests
if ($LASTEXITCODE -ne 0) { throw "compileall failed" }
git archive --format=zip --output=$sourceArchive HEAD
if ($LASTEXITCODE -ne 0) { throw "git archive failed" }
Expand-Archive -LiteralPath $sourceArchive -DestinationPath $sourceRoot
& D:\Anaconda\python.exe -m build --wheel --outdir $wheelDir $sourceRoot
if ($LASTEXITCODE -ne 0) { throw "wheel build failed" }
$wheel = Get-ChildItem -LiteralPath $wheelDir -Filter *.whl | Select-Object -First 1
if ($null -eq $wheel) { throw "wheel build produced no wheel" }
if ($wheel.Length -gt 262144) { throw "Base wheel exceeds 256 KiB: $($wheel.Length)" }
& D:\Anaconda\envs\OCRLLM\python.exe -m pip install --no-deps --target $targetDir $wheel.FullName
if ($LASTEXITCODE -ne 0) { throw "isolated wheel install failed" }
$installedBytes = (Get-ChildItem -LiteralPath $targetDir -Recurse -File | Measure-Object Length -Sum).Sum
if ($installedBytes -gt 1048576) { throw "Base target exceeds 1 MiB: $installedBytes" }

$env:OCRLLM_WHEEL_TARGET = $targetDir
Push-Location $env:TEMP
try {
    & D:\Anaconda\envs\OCRLLM\python.exe -I -c "import os,sys; sys.path.insert(0,os.environ['OCRLLM_WHEEL_TARGET']); import ocrllm; loaded={n.split('.')[0] for n in sys.modules}; forbidden={'PIL','pypdfium2','openai','httpx'}; assert not loaded & forbidden, loaded & forbidden; print(ocrllm.__version__)"
    if ($LASTEXITCODE -ne 0) { throw "outside-repo import failed" }

    $metadataProbe = "import importlib.metadata as m,sys; d=next(x for x in m.distributions(path=[sys.argv[1]]) if x.metadata['Name']=='ocrllm'); reqs=d.requires or []; base=[r for r in reqs if 'extra ==' not in r]; native=[str(p) for p in (d.files or []) if str(p).lower().endswith(('.pyd','.dll','.so','.dylib','.exe'))]; assert not base, base; assert not native, native"
    & D:\Anaconda\envs\OCRLLM\python.exe -I -c $metadataProbe $targetDir
    if ($LASTEXITCODE -ne 0) { throw "base metadata budget failed" }

    $timingProbe = "import json,sys,time; sys.path.insert(0,sys.argv[1]); c=time.process_time_ns(); w=time.perf_counter_ns(); import ocrllm; wall=(time.perf_counter_ns()-w)/1e6; cpu=(time.process_time_ns()-c)/1e6; loaded={n.split('.')[0] for n in sys.modules}; forbidden={'PIL','pypdfium2','openai','httpx'}; assert not loaded & forbidden, loaded & forbidden; print(json.dumps({'wall':wall,'cpu':cpu}))"
    foreach ($python in @('D:\Anaconda\envs\OCRLLM\python.exe', 'D:\Anaconda\python.exe')) {
        $samples = @()
        foreach ($iteration in 0..31) {
            $raw = & $python -I -c $timingProbe $targetDir
            if ($LASTEXITCODE -ne 0) { throw "import timing probe failed: $python" }
            $samples += ($raw | ConvertFrom-Json)
        }
        $wall = @($samples[2..31].wall | Sort-Object)
        $cpu = @($samples[2..31].cpu | Sort-Object)
        $wallMedian = ($wall[14] + $wall[15]) / 2
        $wallP95 = $wall[28]
        $cpuMedian = ($cpu[14] + $cpu[15]) / 2
        $cpuP95 = $cpu[28]
        if ($wallMedian -gt 100 -or $wallP95 -gt 200 -or $cpuMedian -gt 60 -or $cpuP95 -gt 100) {
            throw "Import budget failed for ${python}: wall=${wallMedian}/${wallP95}ms cpu=${cpuMedian}/${cpuP95}ms"
        }
        "${python}: wall median/p95/max=$wallMedian/$wallP95/$($wall[29])ms; CPU median/p95/max=$cpuMedian/$cpuP95/$($cpu[29])ms"
    }
} finally {
    Pop-Location
    Remove-Item Env:OCRLLM_WHEEL_TARGET
}
```

The isolated import command is the base-profile heavy-module guard. Add the
phase's optional modules to `forbidden` whenever a new extra is introduced.

To reproduce the Phase 0 clean image-extra proof, generate the fixture inside
the fresh environment rather than depending on a repository `valid.png` file:

```powershell
$imageVenv = Join-Path $env:TEMP ("ocrllm-image-venv-" + [guid]::NewGuid())
& D:\Anaconda\envs\OCRLLM\python.exe -m venv $imageVenv
$imagePython = Join-Path $imageVenv 'Scripts\python.exe'
$imageSitePackages = & $imagePython -I -c "import site; print(site.getsitepackages()[0])"
$imageBaselineBytes = (Get-ChildItem -LiteralPath $imageSitePackages -Recurse -File | Measure-Object Length -Sum).Sum
& $imagePython -m pip install "$($wheel.FullName)[image]"
if ($LASTEXITCODE -ne 0) { throw "image extra install failed" }
$imageAfterBytes = (Get-ChildItem -LiteralPath $imageSitePackages -Recurse -File | Measure-Object Length -Sum).Sum
$imageDeltaBytes = $imageAfterBytes - $imageBaselineBytes
if ($imageDeltaBytes -gt 26214400) { throw "Image profile exceeds 25 MiB: $imageDeltaBytes" }
& $imagePython -I -c "import importlib.metadata as m,sys; import ocrllm; assert 'PIL' not in sys.modules; v=m.version('Pillow'); parts=tuple(map(int,v.split('.')[:2])); assert parts >= (10,4) and parts < (13,0), v; print(v)"
if ($LASTEXITCODE -ne 0) { throw "image extra lazy-import proof failed" }

$imageFixture = Join-Path $imageVenv 'generated-valid.png'
$imageSmoke = @'
from pathlib import Path
import sys

from PIL import Image
from ocrllm import Config, recognize

path = Path(sys.argv[1])
Image.new("RGB", (8, 6), color=(32, 96, 160)).save(path, format="PNG")

class Provider:
    def recognize_images(self, image_paths, *, prompt, config):
        assert image_paths[0] != path
        with Image.open(image_paths[0]) as image:
            image.verify()
        return "# Generated fixture recognized\n"

result = recognize(path, config=Config(provider=Provider()))
assert result.status == "complete"
assert result.source_type == "image"
assert result.profile == "board"
assert result.markdown == "# Generated fixture recognized\n"
print(result.status)
'@
$imageSmoke | & $imagePython -I - $imageFixture
if ($LASTEXITCODE -ne 0) { throw "generated image recognition proof failed" }
```

Each later extra uses a separate new venv and real phase fixture. Phase 1 must
install `[image,dashscope]`; Phase 3 must independently install `[pdf-text]` and
`[pdf-vision]`, assert Pillow is absent from the text venv and present in the
vision venv, then run text extraction/rendering; Phase 4 installs `[audio]`; and
Phase 5 installs `[video]`. Installing metadata without executing the capability
fixture is a failed gate.

For every clean profile venv, measure `site-packages` immediately after venv
creation and again after installing the wheel plus extra; the installed delta is
`after - baseline` and includes OCRLLM plus all transitive packages while
excluding the venv's bootstrap pip. Use these exact byte ceilings:

```powershell
$profileLimitBytes = @{
    'image' = 26214400
    'image,dashscope' = 67108864
    'pdf-text' = 12582912
    'pdf-vision' = 36700160
    'pdf-vision,dashscope' = 100663296
    'audio' = 67108864
    'video' = 67108864
}

$profilesByPhase = @{
    'phase0' = @('image')
    'phase1' = @('image', 'image,dashscope')
    'phase3' = @('pdf-text', 'pdf-vision', 'pdf-vision,dashscope')
    'phase4' = @('audio')
    'phase5' = @('video')
}

$expectedDistributions = @{
    'image' = @('Pillow')
    'image,dashscope' = @('Pillow', 'openai')
    'pdf-text' = @('pypdfium2')
    'pdf-vision' = @('pypdfium2', 'Pillow')
    'pdf-vision,dashscope' = @('pypdfium2', 'Pillow', 'openai')
    'audio' = $null
    'video' = $null
}

$phase = 'phase1'  # Set only to the currently authorized phase.
if (-not $profilesByPhase.ContainsKey($phase)) { throw "unknown phase: $phase" }
foreach ($profile in $profilesByPhase[$phase]) {
    $expected = $expectedDistributions[$profile]
    if ($null -eq $expected) {
        throw "record exact expected distributions before measuring: $profile"
    }
    $safeProfile = $profile.Replace(',', '-')
    $profileVenv = Join-Path $env:TEMP ("ocrllm-$safeProfile-venv-" + [guid]::NewGuid())
    & D:\Anaconda\envs\OCRLLM\python.exe -m venv $profileVenv
    if ($LASTEXITCODE -ne 0) { throw "profile venv failed: $profile" }
    $profilePython = Join-Path $profileVenv 'Scripts\python.exe'
    $sitePackages = & $profilePython -I -c "import site; print(site.getsitepackages()[0])"
    $baselineBytes = (Get-ChildItem -LiteralPath $sitePackages -Recurse -File | Measure-Object Length -Sum).Sum
    & $profilePython -m pip install "$($wheel.FullName)[$profile]"
    if ($LASTEXITCODE -ne 0) { throw "profile install failed: $profile" }
    $expectedCsv = $expected -join ','
    $profileProbe = "import importlib.metadata as m,sys; d=m.distribution('ocrllm'); declared=set(d.metadata.get_all('Provides-Extra') or []); requested=set(sys.argv[1].split(',')); missing_extras=requested-declared; assert not missing_extras, missing_extras; [(m.version(name) if name else None) for name in sys.argv[2].split(',')]; print(sorted(declared))"
    & $profilePython -I -c $profileProbe $profile $expectedCsv
    if ($LASTEXITCODE -ne 0) { throw "profile dependency declaration failed: $profile" }
    if ($profile -eq 'image,dashscope') {
        $dashscopeProbe = @'
import sys

from ocrllm import Config, DashScopeSettings

loaded = {name.split(".")[0] for name in sys.modules}
forbidden = {"PIL", "openai", "httpx"}
assert not loaded & forbidden, loaded & forbidden

settings = DashScopeSettings(
    region="ap-southeast-1",
    base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
)
config = Config(
    provider="dashscope",
    api_key="offline-package-probe",
    model="qwen3.7-plus-2026-05-26",
    dashscope=settings,
)
assert config.dashscope == settings
assert config.dashscope is not settings

from ocrllm.providers.dashscope.create_dashscope_openai_client import (
    create_dashscope_openai_client,
)
from ocrllm.providers.dashscope.load_openai import load_openai

openai_module = load_openai()
client = create_dashscope_openai_client(
    openai_module,
    api_key="offline-package-probe",
    settings=settings,
    timeout_seconds=3.0,
)
client.close()
print(openai_module.__version__)
'@
        $dashscopeProbe | & $profilePython -I -
        if ($LASTEXITCODE -ne 0) { throw "DashScope offline package probe failed" }
    }
    $afterBytes = (Get-ChildItem -LiteralPath $sitePackages -Recurse -File | Measure-Object Length -Sum).Sum
    $deltaBytes = $afterBytes - $baselineBytes
    if ($deltaBytes -gt $profileLimitBytes[$profile]) {
        throw "profile size failed: $profile delta=$deltaBytes limit=$($profileLimitBytes[$profile])"
    }
    "$profile installed delta: $deltaBytes bytes"
}
```

PDF phase verification must additionally print:

- pypdfium2 version and PDFium build version,
- rendered page count and ordered dimensions,
- extracted text per selected page,
- clean installed profile delta,
- copied license/notice file locations.

The guarded runner is committed at `fb23d1e`, but do not execute its paid live
CLI until the caller supplies the credential's exact approved region and
`base_url`; the shared endpoint used by offline tests is only a test value. Use
a new evidence path and the exact confirmation value 13. The live plan is fixed
at 13 paid calls with no retry: one clean-slide smoke, all six dispatches in run
A, then all six independently dispatched entries in run B. A provider failure
or truncation aborts without another call; never rerun only the failed fixture.
Simulated evidence cannot satisfy the live gate.

Real provider evidence must preserve raw Markdown plus the provider/model
identifier, configuration and Git/import/code/corpus/manifest/artifact hashes,
dependency versions, UTC and elapsed time, every scorer metric, nonempty result
status, and typed failure category without printing credentials, the full
endpoint, or other sensitive documents. After both full runs pass, rerun the
clean profiles and explicitly update this decision; runner success alone does
not change Phase 1 from NO-GO to GO.

## Change Rejection Checklist

Reject a proposed change when any answer is yes:

- Does it import `legacy_app` or uppercase `OCRLLM`?
- Does it add PyMuPDF or `fitz` to the active package?
- Does it add an optional dependency to base import time?
- Does it put more than one responsibility in a new file?
- Does a function live in a file whose name does not describe that function?
- Does it return success with empty content or missing required artifacts?
- Does it expose a legacy processor class as public API?
- Does it put provider retry policy inside media conversion code?
- Does it put output writing inside a provider adapter?
- Does it add GUI, server, downloader, HarmonyOS, Rust, WASM, Office, GPU, or
  offline-model work without a new explicit decision?
- Does it claim support based only on code existence, mocks, historical logs,
  or installed dependencies?
- Does it change an active boundary without updating `MIGRATION_STATUS.md`?

## Documentation Rule

When a phase changes from NO-GO to GO, update all of these in the same commit:

```text
MIGRATION_STATUS.md
README.md
src/ocrllm/README_ACTIVE_LIBRARY.md
docs/ocrllm_library_go_no_go.md
docs/ocrllm_module_target_design.md
```

Record exact commands and results. Do not replace failed or unavailable proof
with planned language.
