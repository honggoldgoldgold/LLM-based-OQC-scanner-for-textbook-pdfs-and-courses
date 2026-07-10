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

As of the decision date:

- The base wheel builds and imports without runtime dependencies.
- The active package routes image extensions to an injected Python provider.
- The active package does not validate that an image exists or decodes.
- The active package can accept empty provider output as success.
- A 2026-07-09 runtime probe confirmed that a nonexistent `.png` still invoked
  the provider and returned success, and an empty provider string also returned
  success. This is direct Phase 0 NO-GO evidence.
- The active package currently returns `source_type="board"`. Before the JSON
  contract freezes, change the canonical media type to `image` and represent
  board recognition as `profile="board"`.
- A real `qwen-vl-max` image call succeeded in an isolated trial, but no real
  provider adapter exists in `src/ocrllm/`.
- PDF, audio, and video are unsupported by the active package.
- `pyproject.toml` currently advertises empty image, PDF, audio, video, and all
  extras. In Phase 0, populate `image` with the lazy decoder dependency and
  remove the other empty feature extras. Add each later extra back only in the
  phase that installs and enables its tested feature.
- A Windows/Python 3.13 PDFium trial passed with pypdfium2 5.11.0 and PDFium
  151.0.7920.0: text extraction distinguished a text page from a raster-only
  page, both pages rendered at 1224 by 1584, and malformed input raised
  `PdfiumError` with error code 3. Python 3.10 installation remains a Phase 3
  gate.
- The tested Windows amd64 pypdfium2 wheel was 3,778,234 bytes compressed and
  8,306,352 bytes installed. Twenty warm-cache fresh-process imports had a
  98.442 ms median; the first cold-cache observation was 279.718 ms. This is an
  optional feature cost, not part of the base import budget.
- The final isolated base verification built a 9,283-byte wheel with SHA-256
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

Therefore the current active phase is contract honesty. Real-image hardening is
the next phase. The current phase is not PDF migration, audio migration, video
migration, service work, or native work.

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
installation/gate state and evaluates the built-in DashScope/default-model
configuration only from dependency discovery plus `DASHSCOPE_API_KEY` presence.
With a named provider/model config, it evaluates that exact pair. An injected
provider object proves protocol shape offline but is `experimental` at most
unless it exposes a stable capability identity matching recorded live evidence.
The worker `capabilities` command uses the zero-argument, environment-scoped
semantics and never returns secret values.

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
    Define immutable caller configuration. No implicit file loading or network
    access.

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
PROVIDER_QUOTA_EXHAUSTED
PROVIDER_TIMEOUT
PROVIDER_NETWORK
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

The current `api.py` is a Phase 0 facade stub. Split it into `recognize.py` and
`recognize_batch.py`; remove routing logic from the facade when Phase 1 lands.

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
    Decode and validate an image through the optional image dependency.

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
64,000,000 aggregate decoded pixels. The fully serialized provider JSON request,
including base64 expansion and prompt, is at most 20 MiB. Validate every group
member and the final serialized size before the first provider call. Decode,
normalize, and close images sequentially; never retain the whole group's decoded
pixel buffers. These are fixed version-1 caps, not caller overrides.

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

tests/quality/load_fixture_manifest.py
    Parse and validate license, hash, language, content-unit, and timestamp data.

tests/quality/normalize_content_units.py
    Apply only the fixed NFKC, newline, whitespace, and declared-equivalence
    normalization rules.

tests/quality/calculate_token_metrics.py
    Calculate required-token recall and content-unit precision.

tests/quality/score_formula_signatures.py
    Compare formula identifiers, values, operators, relations, exponents, and
    subscripts.

tests/quality/score_table_cells.py
    Compare normalized cells by row and column coordinate.

tests/quality/calculate_wer.py
    Calculate Latin-script word error rate.

tests/quality/calculate_cer.py
    Calculate CJK character error rate.

tests/quality/calculate_timestamp_errors.py
    Calculate median and maximum absolute timestamp error.

tests/quality/assert_quality_thresholds.py
    Apply only the predeclared per-phase thresholds in this file.
```

These files stay outside `src/ocrllm` and do not add runtime dependencies.

### Provider layer

```text
src/ocrllm/providers/vision_provider.py
    Define the vision capability protocol.

src/ocrllm/providers/short_audio_provider.py
    Define the synchronous short-audio capability protocol in Phase 4.

src/ocrllm/providers/long_audio_provider.py
    Define the submit, poll, and result-fetch lifecycle for resumable long audio
    in Phase 4.

src/ocrllm/providers/resolve_provider.py
    Resolve an injected object or a documented built-in provider name. Never
    silently switch to a different paid provider.

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
    Map authentication, quota, timeout, cancellation, malformed response, and
    network failures to public errors.
```

Provider model queues and key pools are NO-GO until one-provider error handling
is complete and tests prove why the extra policy is needed.

Phase 1 provider policy is concrete:

- The first vision adapter uses DashScope's OpenAI-compatible Chat Completions
  endpoint through lazy `openai>=2.30,<3`, matching the successful real trial.
  Do not add the DashScope SDK to the image path.
- For image recognition, `Config.provider` accepts an injected vision-capable
  object or the exact built-in name `"dashscope"`. `None` raises `ConfigError`;
  the library never initiates an implicit paid request. PDF `text` mode is local
  and requires no provider or API key.
- Credential order is explicit `Config.api_key`, then `DASHSCOPE_API_KEY`, then
  `ConfigError`.
- The built-in DashScope adapter uses `Config.model` when set and otherwise uses
  the trialed `qwen-vl-max` model.
- Default request timeout is 120 seconds.
- Perform no automatic model switch, key rotation, paid-provider fallback, or
  hidden retry in the first adapter.
- A quota response maps to `PROVIDER_QUOTA_EXHAUSTED`; it is never retried as a
  network failure.
- Add retry/backoff only in a later decision with retry-classification tests and
  cancellation-aware delays.
- Direct-Python cancellation is checked before dispatch. The synchronous
  adapter does not claim it can interrupt an in-flight HTTP call. Phase 2 adds
  hard cancellation by terminating the isolated worker job process.

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

There is currently no committed recognition corpus or scorer. Therefore the
real image call and PDFium backend spike prove feasibility only; they do not
make image, PDF, audio, or video recognition `available`.

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

Commit five fixtures: a synthetic English/Simplified-Chinese slide with at
least 50 scored text units and 8 critical slots; a deterministic perspective,
glare, and JPEG derivative; a CC0 or repo-owned handwritten board with at least
25 units and 5 critical slots; a synthetic board with at least 10 formulas; and
a synthetic table with at least 20 data cells, full headers, and 5 critical
numeric cells. Also score one ordered two-image request with unique first/last
anchors.

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

### Phase 0: Contract honesty -- current

GO when all are true:

- `ocrllm[image]` installs `Pillow>=10.4,<13`; Pillow is imported lazily only
  when validating/decoding an image.
- Missing, unreadable, empty, oversized, unsupported, and invalid image inputs
  fail before provider invocation.
- Empty provider output fails.
- Provider exceptions are typed and secret-safe.
- Config repr/error/event/result tests use unique sentinels for provider object,
  API key, PDF password, and provider `extra`; no sentinel appears in output.
- `RecognitionResult` metadata is JSON-safe and immutable to callers. Tests
  mutate the caller's original nested dict/list and attempt mutation through the
  result; neither can change stored state.
- Result/source tests use canonical media type `image`; `board` appears only as
  a recognition profile.
- Output collision policy is explicit and tested.
- Empty PDF, audio, video, and all extras are removed from package metadata.
- The isolated base wheel/target and fresh-process import probes pass every Base
  numeric budget in `Dependency Profiles` on both recorded Python versions.

NO-GO while the current suffix-only success path remains.

### Phase 1: Real board/image

GO when all are true:

- Offline tests use valid PNG/JPEG files, not arbitrary bytes.
- Tests hit one-below/at/one-above every per-image, aggregate-source,
  aggregate-pixel, group-count, and serialized-request cap and prove rejection
  occurs before provider invocation.
- Handwriting, projected slide, and mixed text/formula fixtures exist.
- One lazy real provider adapter passes authentication, quota, timeout,
  malformed response, pre-dispatch cancellation, and redaction tests. Its
  synchronous in-flight call is documented as non-interruptible.
- One live feasibility smoke returns nonempty structured Markdown for the clean
  slide; this permits `experimental` at most.
- The committed Phase 1 scorer rejects its deliberate corruptions, and two
  independently dispatched full-corpus runs pass every image threshold in
  `Recognition Quality Evidence` without per-fixture retries.
- Plain `import ocrllm` does not import Pillow or the provider SDK/client.
- Clean Image and Image + DashScope installs pass the 25 MiB and 64 MiB profile
  budgets.

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

The base target uses fresh-process imports after two discarded warm-ups, not an
unmeasured cold-cache claim. The actual hard budgets are:

| Profile | Installed-size budget | Import/bundle rule |
|---|---:|---|
| Base | Wheel <= 256 KiB; no-deps target <= 1 MiB | Zero base runtime requirements, zero native binaries, no PIL/pypdfium2/openai imports; 30 measured fresh processes after two warm-ups. Wall median <= 100 ms and p95 <= 200 ms; process-CPU median <= 60 ms and p95 <= 100 ms. Record maxima diagnostically. |
| Image | Clean installed delta <= 25 MiB | Pillow remains lazy. |
| Image + DashScope | Clean installed delta <= 64 MiB | Pillow and openai remain lazy on base import. |
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

Run after every active-library change from the repository root:

```powershell
$wheelDir = Join-Path $env:TEMP ("ocrllm-wheel-" + [guid]::NewGuid())
$targetDir = Join-Path $env:TEMP ("ocrllm-target-" + [guid]::NewGuid())
New-Item -ItemType Directory -Path $wheelDir, $targetDir | Out-Null

& D:\Anaconda\envs\OCRLLM\python.exe -m pytest -q -p no:cacheprovider
if ($LASTEXITCODE -ne 0) { throw "pytest failed" }
& D:\Anaconda\python.exe -m build --wheel --outdir $wheelDir
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
    & D:\Anaconda\envs\OCRLLM\python.exe -I -c "import os,sys; sys.path.insert(0,os.environ['OCRLLM_WHEEL_TARGET']); import ocrllm; loaded={n.split('.')[0] for n in sys.modules}; forbidden={'PIL','pypdfium2','openai'}; assert not loaded & forbidden, loaded & forbidden; print(ocrllm.__version__)"
    if ($LASTEXITCODE -ne 0) { throw "outside-repo import failed" }

    $metadataProbe = "import importlib.metadata as m,sys; d=next(x for x in m.distributions(path=[sys.argv[1]]) if x.metadata['Name']=='ocrllm'); reqs=d.requires or []; base=[r for r in reqs if 'extra ==' not in r]; native=[str(p) for p in (d.files or []) if str(p).lower().endswith(('.pyd','.dll','.so','.dylib','.exe'))]; assert not base, base; assert not native, native"
    & D:\Anaconda\envs\OCRLLM\python.exe -I -c $metadataProbe $targetDir
    if ($LASTEXITCODE -ne 0) { throw "base metadata budget failed" }

    $timingProbe = "import json,sys,time; sys.path.insert(0,sys.argv[1]); c=time.process_time_ns(); w=time.perf_counter_ns(); import ocrllm; wall=(time.perf_counter_ns()-w)/1e6; cpu=(time.process_time_ns()-c)/1e6; loaded={n.split('.')[0] for n in sys.modules}; forbidden={'PIL','pypdfium2','openai'}; assert not loaded & forbidden, loaded & forbidden; print(json.dumps({'wall':wall,'cpu':cpu}))"
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

Before changing Phase 0 from NO-GO to GO, also run this clean image-extra proof;
it is expected to fail while the current `image=[]` metadata remains:

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
& $imagePython -I -c "import importlib.metadata as m,sys; v=m.version('Pillow'); parts=tuple(map(int,v.split('.')[:2])); assert parts >= (10,4) and parts < (13,0), v; from PIL import Image; p=sys.argv[1]; im=Image.open(p); im.verify(); im.close(); print(v)" (Resolve-Path 'tests\fixtures\images\valid.png')
if ($LASTEXITCODE -ne 0) { throw "image extra decode proof failed" }
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

$phase = 'phase0'  # Set only to the currently authorized phase.
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

Real provider tests are opt-in and must print the provider/model identifier,
elapsed time, nonempty result status, and typed failure category without
printing credentials or full sensitive documents.

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
