# OCRLLM Migration Status

This file is the project memory aid. Read it before changing the repo.

## One-Sentence Summary

The old OCRLLM app has been moved to `legacy_app/`; the active project is an
importable Python library in `src/ocrllm`, with contract honesty GO and Phase 1
real board/image plus one provider now current.

## First Files To Read

Use these files to avoid confusing new work, old app code, and suspended future
planning:

```text
START_HERE.md                         One-screen repo map.
README.md                             Short public overview.
src/ocrllm/README_ACTIVE_LIBRARY.md   Active package boundary.
src/ocrllm/AGENTS.md                  Active package editing rules.
docs/ocrllm_library_go_no_go.md       Authoritative execution decision, file
                                      responsibilities, and phase GO gates.
docs/library_migration_decision.md    Foundational library-making rationale.
legacy_app/README_LEGACY.md           Legacy app boundary.
legacy_app/AGENTS.md                  Legacy app editing rules.
docs/ocrllm_module_target_design.md   Target-state module design map.
docs/provider_cost_and_reliability_policy.md
                                      Account-specific provider policy.
docs/phase1_implementation_record.md  Phase 1 commits, agent work, atomic writer,
                                      verification, and resume point.
docs/legacy_bilibili_social_long_debug_record.md
                                      Legacy Bilibili course robustness record.
docs/legacy_youtube_playlist_social_long_workflow.md
                                      Legacy YouTube playlist course workflow.
docs/legacy_filetrans_codex_debug_record.md
                                      Legacy Filetrans/Codex runtime record.
Architecture.md                       Suspended future architecture reference.
```

## Why This Happened

The previous codebase had useful features, but it was not a clean dependency for
other projects:

- It imported as uppercase `OCRLLM`, while the desired package is lowercase
  `ocrllm`.
- It mixed GUI, CLI, FastAPI, social downloaders, processors, prompts, and core
  logic in one package surface.
- It had no root `pyproject.toml`.
- It defaulted output/temp paths into the package directory.
- It exposed implementation classes before there was a stable library facade.

The active decision is to make a small Python-first library and migrate proven
behavior one vertical slice at a time. Implementations are rewritten behind the
new contract; legacy classes and files are not ported. Exact rules are in
`docs/ocrllm_library_go_no_go.md`.

## What Is Current

Use this:

```text
src/ocrllm/
```

Do not build new integrations on this:

```text
legacy_app/OCRLLM/
```

The current public API is:

```python
from ocrllm import (
    Config,
    DashScopeSettings,
    RecognitionResult,
    recognize,
    recognize_batch,
    OCRLLMError,
    ConfigError,
    DependencyMissing,
    InvalidSource,
    NoSpeechDetected,
    OutputError,
    OutputExists,
    ProviderError,
    ProviderUnavailable,
    QuotaExhausted,
    RateLimited,
    UnsupportedFormat,
    Cancelled,
)
```

Phase 0 is GO. The active Phase 1 route validates PNG/JPEG sources and sends
request-scoped snapshots isolated from later caller-path changes to either one
synchronous injected vision provider or the exact built-in name `"dashscope"`:

```python
from ocrllm import Config, recognize


class Provider:
    def recognize_images(self, image_paths, *, prompt, config):
        return "# Board\n"


result = recognize("board.png", config=Config(provider=Provider()))
```

The built-in route requires explicit regional settings and never guesses an
endpoint from a credential:

```python
from ocrllm import Config, DashScopeSettings, recognize


result = recognize(
    "board.png",
    config=Config(
        provider="dashscope",
        dashscope=DashScopeSettings(
            region="ap-southeast-1",
            base_url=(
                "https://your-workspace-id.ap-southeast-1.maas.aliyuncs.com/"
                "compatible-mode/v1"
            ),
        ),
    ),
)
```

The provider receives ordered snapshot paths, not the caller's mutable paths.
It must read them and return before `recognize_images()` returns. The library
then removes the snapshots; a cleanup failure is typed and never silently
reported as success. The active path now provides:

```text
allowed inputs                     PNG, JPG, JPEG
canonical media/profile            image / board
missing/empty/invalid/oversized     fail before provider invocation
provider empty/control-only result  PROVIDER_RESPONSE_INVALID
metadata                            recursively copied and immutable
output_dir=None                     memory-only
existing output                     OUTPUT_EXISTS unless overwrite=True
provider/config secrets             absent from public repr/error/result data
built-in provider/model             dashscope / qwen3.7-plus or pinned snapshot
built-in provider metadata          region, thinking/high-resolution flags,
                                    model, provider, prompt version, image count
public Config boundary              exact Config only; freshly revalidated
```

The built-in DashScope adapter and offline boundary tests now exist. Offline
checkpoint `e328253` additionally commits the licensed five-class image corpus,
deterministic generators, scorers, and integrated manifest-authenticated
live-scoring gate. The pinned suite and byte-identity checks pass. On 2026-07-11
the user confirmed `cn-beijing` and the key-matching endpoint, and the committed
runner completed its fixed 13-call plan with zero runner retries. Both full runs
completed, but neither passed. No provider request or terminal runner failure
occurred. Phase 1 remains NO-GO. The immutable result is summarized in
`docs/phase1_live_quality_result_2026-07-11.md`. Google, Codex, local-OCR, PDF,
audio, and video adapters do not exist in the active library.

Current package metadata still has no base runtime requirements. It declares
exactly `dev`, `image`, and `dashscope`; `image` installs `Pillow>=10.4,<13`, and
`dashscope` installs `openai>=2.30,<3`. Plain `import ocrllm` must leave `PIL`,
`openai`, and transitive `httpx` absent from `sys.modules`.

Active PDF policy is decided now even though PDF implementation is not
authorized yet:

- Use PDFium through `pypdfium2`.
- Keep `pypdfium2` behind future `ocrllm[pdf-text]` and
  `ocrllm[pdf-vision]` extras and out of base import. Text-only installs do not
  install Pillow.
- Rewrite PDF rendering and text extraction; do not port PyMuPDF/`fitz` code.
- Start with `pypdfium2>=5.11.0,<5.12` and `Pillow>=10.4,<13`; lock the first CI
  proof to pypdfium2 5.11.0 and Pillow 12.2.0.
- Serialize PDFium calls behind one process-wide lock. Do not port the legacy
  threaded renderer because PDFium is not thread-safe.
- Do not mark PDF supported until the Phase 3 gate in
  `docs/ocrllm_library_go_no_go.md` passes.

Local PDFium feasibility evidence on Windows/Python 3.13:

```text
pypdfium2 5.11.0
PDFium 151.0.7920.0
2-page mixed PDF opened
text page extracted expected content
raster-only page extracted no text
both pages rendered at 1224 x 1584
malformed PDF raised PdfiumError error code 3
wheel size 3,778,234 bytes
installed size 8,306,352 bytes
```

This is a conditional feasibility GO, not active PDF support. Python 3.10,
Unicode, encrypted, hostile, large-document, recognition, cancellation, and
license-notice packaging gates remain.

Latest Phase 0 gate evidence on the recorded Windows reference host, from code
checkpoint `5018ad0` plus the final phase-transition documentation tree on
2026-07-10:

```text
root tests                         141 passed
                                  (138 active-library, 3 course-tool tests)
wheel size                         31,151 bytes
wheel SHA-256                      FD983CA90944F545A4B670F33A8ABF015712E1DDAC8F866BB4703E0A465C707D
isolated no-deps install          135,213 bytes
Python 3.10, 30 fresh processes   wall median/p95/max 58.642/108.161/114.861 ms
                                   CPU median/p95/max 46.875/78.125/78.125 ms
Python 3.13, 30 fresh processes   wall median/p95/max 22.865/30.880/31.043 ms
                                   CPU median/p95/max 23.438/31.250/31.250 ms
plain-import optional modules     PIL, pypdfium2, openai all absent
base runtime requirements         none
native binaries in base wheel     none
declared extras                    dev, image
clean image installed delta       15,814,896 bytes
clean image Pillow                12.3.0
clean generated-PNG recognition   complete, source_type=image, profile=board
```

The exact gate ran the authoritative test/build/isolated-target/timing commands.
For the image-extra proof it generated an 8-by-6 PNG inside the fresh image venv
after installing the wheel, then decoded and recognized that file; this replaces
the stale reference to a nonexistent committed `tests/fixtures/images/valid.png`.
All Phase 0 numeric and behavior gates passed at that historical checkpoint.
Phase 0 alone did not make recognition quality available. Current checkpoint
`e328253` supplies the licensed Phase 1 corpus and scorer separately. The first
live result now exists and is a recorded NO-GO: 13 calls completed, zero of two
full runs passed.

The historical Phase 0 verification entrypoints used were:

```powershell
& D:\Anaconda\envs\OCRLLM\python.exe -m pytest -q -p no:cacheprovider
& D:\Anaconda\python.exe -m build --wheel --outdir $wheelDir
& D:\Anaconda\envs\OCRLLM\python.exe -m pip install --no-deps --target $targetDir $wheel.FullName
& D:\Anaconda\envs\OCRLLM\python.exe -m venv $imageVenv
& $imagePython -m pip install "$($wheel.FullName)[image]"
```

The 30-process/two-warm-up timing loop, metadata/native guard, outside-repo
import, deterministic PNG generator, and image recognition assertions were run
exactly as recorded in `docs/ocrllm_library_go_no_go.md`.

A later Python 3.10 repeat measured 48.978 ms median with one 155.312 ms maximum
and failed the draft maximum-100-ms rule. A post-build run then measured 70.477
ms wall median/108.311 ms p95, while a separate unchanged-package probe measured
36.382/40.744 ms wall and 31.250/46.875 ms process CPU median/p95. The final gate
uses 30 fresh processes after two warm-ups: wall median <= 100 ms/p95 <= 200 ms
and process-CPU median <= 60 ms/p95 <= 100 ms; maxima remain diagnostic. This
change separates package CPU work from bounded scheduler/antivirus noise rather
than waiving a CPU or percentile failure.

HarmonyOS/ArkTS integration is deferred. It is not an active feature, phase, or
compatibility claim.

## Historical Legacy Social-Long Course Path

The Bilibili/social downloader still lives under `legacy_app/OCRLLM/`. It is a
read-only behavior reference for this migration, not a public `ocrllm` library
API or an active test surface.

Detailed incident history, implementation map, verification commands, and
operational rules are in:

```text
docs/legacy_bilibili_social_long_debug_record.md
```

The recorded multi-part Bilibili command was:

```powershell
$env:PYTHONPATH='legacy_app'
D:\Anaconda\envs\OCRLLM\python.exe -m OCRLLM.cli social_long `
  "https://www.bilibili.com/video/BV1nJ411z7fe?p=33" `
  --parts 1-33 --resume -o output\bilibili_cs231n_full
```

Expected per-part output is exactly two Markdown files:

```text
*_板书识别.md
*_录音识别.md
```

The Bilibili comments and per-part danmaku context is written separately to:

```text
bilibili_social_context.md
```

This legacy path has resume support for existing downloads, completed video
phases, and in-flight DashScope FileTrans task IDs. Keep new downstream
projects importing `ocrllm`; do not expose this legacy processor as a new public
library boundary.

For multi-part YouTube course playlists, the equivalent recorded legacy
workflow is documented here:

```text
docs/legacy_youtube_playlist_social_long_workflow.md
```

The recorded command used the same legacy CLI boundary:

```powershell
$env:PYTHONPATH='legacy_app'
D:\Anaconda\envs\OCRLLM\python.exe -m OCRLLM.cli social_long `
  "https://youtube.com/playlist?list=PLggLP4f-rq02vX0OQQ5vrCxbJrzamYDfx&si=6VZ5fem42kqyyasd" `
  --parts 1-97 --resume -o output\youtube_modern_robotics_full
```

The 2026-07-06 YouTube playlist run is still legacy compatibility work, not a
public `ocrllm` API. It fixed and documents these additional runtime rules:

- YouTube playlist probe results must expose flat entries and route to
  `social_long`, not `social_short`.
- Non-Bilibili yt-dlp downloads must allow playlists and map `--parts` to
  `playlist_items`.
- Codex social-long video recognition caps the effective video frame batch size
  at 1 to avoid incomplete multi-frame markers.
- Video debug temp directory names must be Windows-safe and stable for YouTube
  titles.
- Social-long part output directories must strip trailing spaces/dots after
  legacy truncation, and long per-part artifact stems must shorten before
  Windows path limits are reached.
- Resume skip checks must accept an existing clean board/audio markdown pair
  before changing artifact stems, otherwise completed parts can be duplicated.
- DashScope FileTrans sidecars must be shortened using the resolved absolute
  `.tmp` path length.

The 2026-07-06 Bilibili CS231n run exposed and fixed these legacy runtime
problems:

- Multi-part Bilibili pages must route to `social_long`, not short-video mode.
- Requested part failures must fail the whole selected run instead of returning
  a partial course.
- Bilibili MP4 downloads need reusable `.part` downloads and existing-file
  reuse.
- Shared comments must be fetched once from the course AID; danmaku must be
  fetched per part CID.
- The old XML danmaku endpoint can return Bilibili 412/risk-control HTML, so
  the fallback path uses the segmented protobuf danmaku API.
- Each part is complete only with exactly `*_板书识别.md` and
  `*_录音识别.md`.
- FileTrans task IDs must survive process interruption so resume can continue
  polling instead of resubmitting the same long audio.
- Video resume must trust valid phase artifacts when a checkpoint was not
  marked complete before process exit.
- Social media GUI input must accept free-form text and Markdown-style pasted
  links, not only lines beginning with `http`.

Historical completion evidence recorded for the supervised Bilibili course
run; this is not current active-library evidence:

```text
33 part directories
33 downloaded MP4 files
33 *_板书识别.md files
33 *_录音识别.md files
0 FileTrans task sidecars
bilibili_social_context.md contained github.com/Divsigma/Courses and per-part danmaku
Focused legacy tests: 40 passed
Root active-library tests: 5 passed
```

## Legacy Codex/Filetrans Robustness Status

As of 2026-07-06, Codex video recognition and DashScope Filetrans audio
recognition remain legacy compatibility work in `legacy_app/`, not public
`ocrllm` API.

The July 2026 robustness fixes changed the legacy runtime behavior in these
ways:

- Codex CLI image-recognition subprocesses are launched with Windows
  no-window subprocess flags and closed stdin.
- Codex CLI nonzero exits and empty results are retried once and summarized,
  instead of dumping prompts or CLI diagnostics into board Markdown.
- In Codex mode, Phase 4 batch/per-frame failures are hard failures; they no
  longer create placeholder Markdown that looks complete.
- Codex mode skips the Qwen text hotword extraction step that made a Codex run
  appear to route through Qwen after image recognition.
- Filetrans cost logging uses the cached duration probe instead of the removed
  `_get_duration` method.
- Board-only reruns with `--phases 2 3 4` preserve existing audio transcripts
  instead of invalidating Phase 5 artifacts.

Historical evidence recorded by the 2026-07-06 audit:

```text
40 target course folders scanned
40 folders had exactly the expected board/audio Markdown pair
0 folders had known dirty markers
53 focused legacy regression tests passed
0 active legacy video checkpoints remained
```

Use `docs/legacy_filetrans_codex_debug_record.md` as behavior evidence. Do not
change or rerun this path for an active-library phase gate.

## Active Execution Decision And Target Design

`docs/ocrllm_library_go_no_go.md` is the controlling implementation record. It
defines:

- the current GO and NO-GO boundaries,
- one responsibility for each target file,
- which legacy behaviors to preserve,
- which implementations must be rewritten,
- which legacy areas are rejected or deferred,
- exact phase gates and verification commands.

`docs/ocrllm_module_target_design.md` describes the intended completed Python
library. It is a supporting design map, not the execution queue.

The documents are useful for rebuilding context after memory loss. The
GO/NO-GO record defines allowed boundaries; tests and real downstream imports
provide the evidence for advancing a gate.

## Future Provider, Preference, Pool, And Local-OCR Decision

The 2026-07-10 implementation brief is accepted as product direction, but its
configuration and pooling sketch is not accepted literally:

- `board` is a recognition profile. A future local-OCR path is an execution
  engine/capability orthogonal to that profile, reached through the same public
  `recognize()` facade only after an engine, optional dependency, fixtures,
  quality threshold, and capability name are approved.
- A universal `category + api_key` requirement is invalid because Codex is a
  local authenticated CLI and has no per-call API key. Future provider config
  must be discriminated by adapter category and validate only applicable fields.
- Do not overload `api_key` as `str | tuple[str, ...]`. Immutable workflow config
  will compose provider/model choice, recognition preferences, execution policy
  (batch, in-flight limit, monotonic request-start interval), and retry policy.
  A credential pool is a separate stateful, concurrency-safe runtime scheduler.
- A future pool must account for fair rotation, cooldown/health, last use,
  provider quota domains, and error disposition. It must never persist or print
  raw keys. Multiple Google keys in one project must not be treated as extra
  project quota.
- Model input limits are provider/model capabilities. An impossible request such
  as 100 images for a 10-image model must fail before upload, not surface as an
  opaque provider error.
- Quality/cost/latency preference is task based. Do not hard-code an
  audio-specific "Pro" model rule into generic configuration.
- Durable resume remains versioned completed-unit/remote-task state for later
  long PDF/audio/video jobs. Phase 0 image snapshots are validation isolation,
  not resume state.

Provider pools, model queues, automatic retry/switching, and local OCR remain
NO-GO until the one-provider Phase 1 error and quality gates establish evidence.

## Phase 1 DashScope Decision (2026-07-10)

Phase 1 has one implemented provider baseline with offline boundary tests. This
is not a claim that the recognition-quality or live-provider gate has passed:

- `qwen-vl-max` is now a legacy model and is not the implementation baseline.
  The exact Phase 1 allowlist is `qwen3.7-plus` and
  `qwen3.7-plus-2026-05-26`; omitted `Config.model` selects the pinned snapshot.
  The floating alias is allowed for explicit use, but cannot produce the initial
  reproducibility evidence.
- `Config(provider="dashscope")` must compose an immutable
  `DashScopeSettings`. The settings require an explicit region and full
  OpenAI-compatible `base_url`; the preferred production value is that region's
  workspace-dedicated endpoint. API keys are region-specific, so the adapter
  validates the region/endpoint pairing and never guesses a region or endpoint.
  An existing shared DashScope-domain endpoint may be selected explicitly for a
  legacy integration, but it is never a silent default.
- The exact settings fields are `region`, `base_url`,
  `enable_thinking=False`, and `vl_high_resolution_images=True`. Workspace
  endpoints use
  `https://{workspace-id}.{region}.maas.aliyuncs.com/compatible-mode/v1` for
  `ap-northeast-1`, `ap-southeast-1`, `cn-beijing`, `cn-hongkong`, or
  `eu-central-1`. The only shared compatibility endpoints are the matching
  Beijing, Singapore, Hong Kong, and US hosts accepted by the validator.
- Every public call revalidates an exact `Config` before source/provider work.
  Injected providers keep the caller's original `Config` identity. A named
  built-in provider is snapshotted at the first line of image processing, before
  provider/model resolution, prompt construction, or cancellation inspection;
  its adapter revalidates that isolated copy again. Nested settings are
  reconstructed so callback or frozen-dataclass mutation cannot diverge request
  metadata or bypass endpoint allowlisting.
- Credential lookup remains one value only: explicit `Config.api_key`, then
  `DASHSCOPE_API_KEY`, then `ConfigError`. Coding Plan `sk-sp-` keys are rejected
  because they cannot authorize this adapter. The key is redacted everywhere.
- The OpenAI-compatible request reads each validated snapshot and sends a
  MIME-correct Base64 data URL. A local filesystem path is never put in the
  remote JSON. Each complete data URL is at most `10,000,000` UTF-8 bytes, and
  the fully serialized JSON request remains capped at 20 MiB (`20,971,520`
  bytes), both before dispatch.
- DashScope-specific preflight requires both dimensions to be greater than 10
  pixels, an aspect ratio no greater than 200:1, a longest side no greater than
  `7,680`, and the selected model's pixel/image-count constraints. For the
  pinned model with high-resolution image processing enabled, the initial
  per-image provider ceiling is `16,777,216` pixels; the library's 10-image
  group limit remains stricter than the model's published maximum. The adapter
  decodes and encodes the same bounded byte buffer and rechecks the final
  group's `64,000,000` aggregate-pixel cap from those bytes.
- The non-streaming request preserves image order, appends the board prompt last,
  fixes `temperature=0` and `max_completion_tokens=16,384`, and uses
  `chat.completions.with_raw_response.create`. A response succeeds only when the
  partial-response header is absent or `false`, the response model exactly
  matches the request, exactly one choice has index 0, role `assistant`, no
  refusal, `finish_reason="stop"`, and nonempty text after facade validation.
- Construct the synchronous OpenAI client with `max_retries=0`. Cancellation is
  checked before preflight, between image preflights, and immediately before
  dispatch, but a synchronous in-flight HTTP call is not interruptible. The
  first adapter adds no hidden retry, model switch, key rotation, or paid-provider
  fallback.
- Initial quality runs fix `enable_thinking=false` and
  `vl_high_resolution_images=true`. These values are evidence-dependent, not a
  permanent quality promise: changing either one invalidates the affected live
  evidence. Any output truncation signal, including `finish_reason="length"`, is
  `PROVIDER_RESPONSE_INVALID`; truncated Markdown is never successful output.
- Error classification distinguishes retryable throttle
  (`PROVIDER_RATE_LIMITED`), timeout (`PROVIDER_TIMEOUT`), network
  (`PROVIDER_NETWORK`), and service-unavailable (`PROVIDER_UNAVAILABLE`) failures
  from nonretryable authentication, quota/billing, invalid configuration/source,
  and malformed-response failures. Provider quota/billing codes are evaluated
  before a generic HTTP status so permanent account limits are not mislabeled as
  retryable throttling or authentication failures. Documented provider timeout
  codes take precedence over generic 5xx mapping. Unsupported model text is not
  echoed in errors. If request processing and client close both fail, the first
  typed error remains primary with only
  `provider_client_cleanup_failed=true` attached.
- Successful result metadata records `provider`, `model`,
  `prompt_version="board.v6"`, `profile`, `image_count`, `provider_region`,
  `review_passes`, `provider_call_count`, `enable_thinking`, and
  `vl_high_resolution_images`. It never records the API
  key or request body.
- The historical adapter-only implementation checkpoint is commit `a6a8b18`.
  Its final offline gate passed `283` tests, `compileall`, and
  `git diff --check`. A clean wheel was
  `50,970` bytes with SHA-256
  `5502B5ED58D9D049F3640F3AF9AF5C4A8732426C14EA630D01125BD2556245AE`,
  `53` entries, no native/bytecode payload, and no base runtime requirement. Its
  isolated no-deps target was `233,115` bytes. Fresh CPython 3.10.20 and 3.14.3
  imports both left `PIL`, `pypdfium2`, `openai`, and `httpx` unloaded.
- A fresh `ocrllm[image]` empty-target install was `15,907,554` bytes and passed
  a generated-PNG recognition call through the injected-provider path with
  Pillow 12.3.0. A separate fresh `ocrllm[image,dashscope]` empty-target install
  was `40,727,895` bytes, below the 64 MiB gate. Its offline adapter probe used
  Pillow 12.3.0, OpenAI 2.45.0, and HTTPX 0.28.1, constructed the real client
  with `max_retries=0`, and sent no HTTP request.
- The current offline quality checkpoint is commit `e328253`. It commits the
  licensed five-class corpus, deterministic generators, provenance records,
  exact per-language/token, critical-slot, formula, table, and ordered-anchor
  scorers, plus the integrated live-scoring gate. That entrypoint authenticates
  the supplied manifest against a freshly strict-loaded byte-frozen manifest
  before scoring and fails closed when a scoring channel is not applicable.
- The current versioned manifest is exactly `35,400` bytes with SHA-256
  `43c548fdfda1d114b6851def2ce05284cc213bd3478e1e0eea9faa6242a27966`.
  The committed corpus has 20 artifacts, including 5 images, totaling
  `17,914,515` bytes and leaving `8,299,885` bytes of headroom below the 25 MiB
  limit.
- Runner checkpoint `fb23d1e` is committed at full commit
  `fb23d1e40d4594ed1da8e244945ae7ccb9568efd`. Its offline fake/evidence tests
  pass; at that checkpoint the complete pinned suite passed `546` tests, the
  four generated images remained byte-identical, and `compileall` passed.
  Direct no-network
  preflight verified the strict manifest and artifacts, exact repository import
  origins, the closed public signature
  `(region, base_url, evidence_path, confirm_paid_calls, repository_root)`, and a
  clean Git identity covering 98 tracked relevant files at that exact commit.
  No provider/API call was made.
- The runner freezes exactly 13 zero-retry invocations: one clean-slide smoke,
  then six manifest dispatches in run A and the same six independently
  dispatched in run B. V6 explicitly performs two same-model provider calls per
  recognition, so its paid-call confirmation is 26 while the dispatch order
  remains 13. The live entrypoint closes over real dependencies and
  cannot accept test injections. The private simulated path records its injected
  dependencies and can pass only `simulated_plan_passed`, never
  `phase1_gate_passed`.
- At startup the runner establishes exact import origins, strict manifest and
  artifact validity, code/Git identity, and the environment credential. Before
  and after each call it rechecks the applicable manifest, input, code/Git, and
  credential invariants; final postflight repeats the full identity checks. It
  atomically checkpoints the active attempt before each call and the raw
  Markdown, hashes, metadata, elapsed time, and complete scorer metrics
  afterward. Both SDK and runner retry counts are zero; a provider or identity
  failure aborts without another call.
- Evidence writes flush and `fsync` the temporary file, publish the first
  checkpoint with an exclusive hard link, and update it with normal atomic
  `os.replace`. The writer does not explicitly `fsync` the containing directory,
  so it does not promise persistence across sudden power loss beyond normal
  filesystem link/replace guarantees.
- Boundary checkpoint `5aaa854` (full commit
  `5aaa8545a8b73277fa728861be5510cb0a073d84`) adds exact one-below, at, and
  one-above cases for the per-source byte, decoded-pixel, group-count,
  aggregate-source-byte, and aggregate-pixel caps. The rejecting
  per-source/pixel/count/aggregate integration cases all prove zero provider
  calls; aggregate-source rejection additionally precedes temporary-directory
  access. The complete pinned suite passes `568` tests, generated fixture
  bytes remain identical, and `compileall` passes without a provider/API call.
- Pushed packaging hotfix `3414f47` fixed a filename-ignore defect without
  weakening secret protection. The legitimate module/function formerly named
  `resolve_dashscope_api_key.py` / `resolve_dashscope_api_key` matched the
  existing `*_api_key*` secret-ignore pattern; the hotfix renamed them to
  `resolve_dashscope_credential.py` / `resolve_dashscope_credential` and updated
  imports, documentation, and tests. A clean Git-archive build from full commit
  `3414f47e5b44a6d5fe2023012ebf2cf361f96a61` produced a `50,094`-byte wheel.
  Its isolated no-deps install imported `Config` and the resolver and passed an
  explicit test-key round-trip. No provider network call was made.
- The clean package proof for `5aaa854` uses a Git archive, not the working
  directory. It produced a `51,281`-byte wheel with SHA-256
  `23e0068b4525a437052254d8929f0d7ab7706efd5ff48447d04572c796909d93`, 52
  entries, zero base runtime requirements, and no native or bytecode payload.
  Its isolated no-deps target has 103 files totaling `233,665` bytes. Plain
  import leaves Pillow, PDFium, OpenAI, and HTTPX unloaded, and the explicit
  test-key credential resolver passes. Thirty measured processes after two
  discarded warm-ups pass the import budgets: Python 3.10.20 wall
  median/p95/max `51.9831/75.8686/77.3612` ms and CPU
  `46.875/78.125/78.125` ms; Python 3.13.5 wall
  `50.79575/61.3618/62.4312` ms and CPU `46.875/62.5/62.5` ms.
- The separate clean optional profiles for `5aaa854` also pass. Image uses
  Pillow 12.3.0, adds `15,904,714` bytes, preserves lazy import, and completes
  a generated-PNG recognition call through the injected-provider path. Image +
  DashScope uses Pillow 12.3.0, OpenAI 2.45.0, and HTTPX 0.28.1, adds
  `40,677,554` bytes, preserves lazy base import, and constructs and closes the
  real zero-retry client without HTTP. Both remain below their 25 MiB and 64 MiB
  ceilings. No external provider/API HTTP request was made. Decision-only
  result-recording edits do not change wheel inputs; the decision-time profile
  rerun remains required after live evidence or any later
  packaged-input/dependency change.
- A secret-safe local configuration audit found that
  `HKCU:\Software\OCRLLM\QCR\ui` stores a full HTTPS `base_url` whose API key is
  an exact match for the current `DASHSCOPE_API_KEY` under an ordinal string
  comparison that never prints either secret. The endpoint uses host
  `dashscope.aliyuncs.com`, exact path `/compatible-mode/v1`, and no query. That
  registry key stores no region/location value, and no DashScope-related region
  variable was found in the checked Process/User/Machine scopes. This recovers
  the key's configured endpoint. On 2026-07-11 the user explicitly confirmed
  that Aliyun API workflows always use Beijing, authorizing canonical region
  `cn-beijing` with that stored endpoint for the fixed Phase 1 live gate.
- Account-specific billing/reliability guidance is recorded separately in
  `docs/provider_cost_and_reliability_policy.md`. Qwen image calls are billed
  independently; FileTrans ASR is covered by the user's token package for later
  large audio tests; Google is free but less stable; and Codex Mini 5.4 is
  inexpensive and stable but not free. None of those later workflows becomes
  active during Phase 1.
- `docs/phase1_implementation_record.md` records every pushed checkpoint, the
  parallel agent/audit contributions, the atomic evidence-writer guarantees and
  power-loss caveat, current verification, and the exact live resume point.
- The user-supplied screenshots currently present under `docs/` are local,
  supplemental, and non-redistributable. They may help manual development, but
  they remain untracked and cannot enter pass/fail evidence. They are not part
  of the committed licensed corpus.

The current offline checkpoint verification entrypoints are:

```powershell
uv run --no-project --isolated --with 'Pillow==12.3.0' `
  --with 'pytest>=8,<10' --with 'openai>=2.30,<3' `
  --python 'D:\Anaconda\envs\OCRLLM\python.exe' `
  python -m pytest -q -p no:cacheprovider
uv run --no-project --isolated --with 'Pillow==12.3.0' `
  --python 'D:\Anaconda\envs\OCRLLM\python.exe' `
  python -m tests.quality.generators.generate_phase1_fixtures --check
& 'D:\Anaconda\envs\OCRLLM\python.exe' -m compileall -q src tests
```

The exact clean archive/build/install/import sequence for `3414f47` is recorded
under `Verification Commands` in `docs/ocrllm_library_go_no_go.md`.

Primary references: [Model Studio visual understanding and model
status](https://www.alibabacloud.com/help/en/model-studio/vision-model), [image
input and Chat Completions request
fields](https://www.alibabacloud.com/help/en/model-studio/qwen-api-via-openai-chat-completions),
[region and workspace base
URLs](https://www.alibabacloud.com/help/en/model-studio/base-url), and the
[OpenAI Python retry
configuration](https://github.com/openai/openai-python#retries).

## What Is Suspended

`Architecture.md` contains a Rust/PyO3 v3 rewrite plan. That plan is currently
suspended. It is not the implementation path for the next work item.

Rust can come back later only after:

- The Python import contract works.
- At least one real downstream project imports `ocrllm`.
- The module boundary to rewrite is stable.
- Tests can compare behavior against the Python implementation.

HarmonyOS/ArkTS is also deferred. Do not add a native bridge, ArkTS client, or
compatibility claim without a new explicit decision after the active library
and its distribution contracts are stable.

## What Was Moved

The old app package moved from repo root to:

```text
legacy_app/OCRLLM/
```

The old root launcher aliases were removed to avoid confusing the migrated repo
layout with the pre-migration app layout:

```text
start.bat
ocrllmstart.bat
legacy_app/start.bat
```

The preserved historical GUI launcher is:

```text
legacy_app/launch_gui.bat
```

That launcher runs `python -m OCRLLM.main` from `legacy_app/`, not
`python main.py`, because `main.py` lives at `legacy_app/OCRLLM/main.py`.

The old tests/docs/scripts moved to:

```text
legacy_app/tests/
legacy_app/docs/
legacy_app/README.md
legacy_app/requirements.txt
legacy_app/environment.yml
```

## What To Do Next

Current phase: **Phase 1 -- real board/image and one provider**.

Finish only this bounded slice. The first live gate is complete and failed; do
not delete, overwrite, selectively retry, or reinterpret its evidence:

1. Preserve and audit
   `evidence/phase1/phase1-quality-2026-07-11-cn-beijing.json` and its SHA-256
   `cfb2ee423eafecbc87190f9e30d39439f0ea0a865d1a0348a140f67d8088fa23`.
2. Design a separately versioned prompt/scorer correction offline. Keep all
   v1 thresholds and this evidence frozen. Add deliberate-corruption tests
   before accepting any newly declared presentation equivalence.
3. Treat the repeated handwriting recall, precision, and critical-slot misses
   as product quality failures; a formatting-parser correction cannot erase
   them.
4. Require a new explicit user decision, a new evidence path, and a clean
   Git/import/manifest/artifact preflight before another billed call set.
5. Keep the clean-tree offline/package gate current after source, packaged
   README, dependency, or package-metadata changes.

The historical v2 correction explicitly
requires labeled standalone formulas, Unicode inline relations, and exact
handwritten spelling/capitalization. Its separate fail-closed normalizer accepts
only the observed content-preserving presentation forms and standalone
horizontal rules. The full suite passes `568` tests. Diagnostic scoring of the
preserved v1 raw outputs makes the smoke and every non-handwriting dispatch pass
while both handwriting dispatches retain the same seven failure codes. This is
not new live evidence and does not authorize another billed run.

Clean package proof for full commit
`9dc4e7a8d9f113c1ea001105335829494086d003` passes. The wheel is 52,602 bytes
with SHA-256
`8ce3a51f2367bdfa3255f8ca23f1b95fd46176e728edec3ef4369da1c626f385`;
its isolated no-deps target is 237,251 bytes with zero base requirements and no
native payload. Python 3.10 and 3.13 pass the 30-sample wall/CPU import budgets.
Image and Image + DashScope add 15,918,041 and 40,837,813 bytes respectively;
the generated-PNG recognition and offline Beijing client-construction probes
pass without provider HTTP. See `docs/phase1_implementation_record.md` for the
recorded disk-contention and wrong-origin measurement incidents.

A zero-network v2 preflight passed at full commit
`2d5a693e53ba3395aa08c530c4dbdea693295097`. It verified 99 clean relevant
files, 20 artifacts, the v2 manifest/prompt/evidence contracts, the fixed
13-call plan, credential presence, Beijing settings, and an absent new evidence
path. Repeat it from the exact future paid-run commit; this result neither makes
a provider call nor authorizes one.

The first fixed v2 live gate then completed at full commit
`94d5187ff8718f2683f67e4c5f75e95c3a9d9070`: 13 calls, zero retries, zero
provider failures, two complete runs, and zero passing runs. The evidence is
`evidence/phase1/phase1-quality-v2-2026-07-11-cn-beijing.json`, 78,235 bytes,
SHA-256
`03275cf5922a46dd59fc75e4ab6dc6499e3aeea973190f1d3a6f48b0c556df0b`.
Projected slide, formula board, and calibration table passed twice. Printed and
ordered requests exposed undeclared U+2A7E relation typography; handwriting
exposed undeclared line-leading U+2192 diagram connectors. Phase 1 remains
NO-GO. The next correction must be versioned and keep wrong content and inline
arrows fail-closed.

That correction is now implemented as `board.v3` /
`labeled-latex-restricted.v3`. It maps only U+2A7E/U+2A7D relation typography
and line-leading U+2192 diagram connectors. Inline arrows, wrong relations, and
wrong values remain failures. The full suite passes `574` tests, fixture bytes
are identical, and compilation passes. Diagnostic scoring makes all preserved
v2 non-handwriting dispatches pass while handwriting retains the same seven
quality failures. A clean v3 package proof and meaningful handwriting-quality
improvement are still required before another full gate.

Post-v2 exploratory work is recorded in
`docs/phase1_exploratory_robustness_2026-07-11.md`. Thirteen requests tested
v3 handwriting, deterministic crops, four private dense optimization
screenshots, thinking mode, Qwen3.5-OCR chat/Responses, and
`qwen-vl-ocr-latest`. The private screenshots all completed; no tested
handwriting path passed. Qwen-VL-OCR returned HTTP 403, and Qwen3.5-OCR's
document-parsing response exposed a temporary signed OSS URL, so neither enters
the allowlist. The handwriting manifest also omits a visible label and requires
a complete source-derived reannotation before another handwriting gate.

The temporary split recommendation is withdrawn. The user required one unified
`board` capability, and the subsequent source audit proved the apparent gap was
mostly fixture error: the source says `Enzymens`, includes
`R-DNA / Replasmid`, has case-ambiguous cursive labels, and contains real faint
micro-labels omitted from precision truth. Crop, legacy-prompt, and high-
resolution controls did not change the disputed readings. Thinking mode did
capture the one genuinely missed second `+`.

`board.v4` now keeps the unified capability, pins thinking mode for the live
contract, separates required recall truth from optional source precision truth,
and version-controls line-leading Unicode/LaTeX diagram connectors. The
37,492-byte manifest SHA-256 is
`b0a38e364ca7e8a2b799548304a219392b5570ab515187ec72d52cd785bfbbb0`.
The isolated full suite passes 583 tests, generated fixture bytes are identical,
and `compileall` passes. Read
`docs/phase1_unified_board_handwriting_debug_2026-07-11.md` for the evidence.
Phase 1 remains NO-GO only until two fresh complete v4 live runs pass.

V4 live attempt 1 is preserved at
`evidence/phase1/phase1-quality-v4-2026-07-11-cn-beijing.json`, 27,245 bytes,
SHA-256
`49e5a3981d13137c5a8ca543b96290bf3b30595ed5cd6d19ca58362c19134015`.
It made one smoke invocation, received retryable DashScope HTTP 500
`internal_server_error`, and aborted with `PROVIDER_UNAVAILABLE` before any full
run. This is transport-failure evidence, not a recognition-quality result. Do
not overwrite or resume it; a later attempt must use a new complete plan and
new evidence path. See
`docs/phase1_live_quality_result_v4_attempt1_2026-07-11.md`.

V4 attempt 2 is preserved separately at
`evidence/phase1/phase1-quality-v4-attempt2-2026-07-11-cn-beijing.json`, 57,929
bytes, SHA-256
`936edd25c72d3d58f0d70fed4621c603ced023eca572901a8cf773d62635cc6e`.
It invoked seven calls. Smoke plus all five single fixtures returned; printed,
projected, formula, and table passed. Handwriting had 29/30 required recall,
33/40 precision, 5/6 critical-token accuracy, and 10/10 critical slots. It
still missed the center `+`; two line-leading ASCII `->` connectors caused four
false unexpected critical tokens. The run-A ordered request then timed out and
the runner aborted before run B. Preserve this partial evidence. The next
offline correction may accept only line-leading ASCII connectors with corruption
tests, but must still solve the genuinely missing `+`. See
`docs/phase1_live_quality_result_v4_attempt2_2026-07-11.md`.

The post-attempt correction is `board.v5` /
`labeled-latex-restricted.v5` / evidence schema v5. It adds a generic internal
region-by-region verification pass that inventories repeated standalone marks,
not a handwriting-specific prompt. It accepts ASCII `->` only as a
line-leading diagram connector; inline `A -> B` and other content remain
visible. Source reinspection adds the second genuine `RG` occurrence and the
visible `OR` label to optional precision truth. The center `+` remains required.

Two targeted built-in-provider calls wrote Markdown through the library's
atomic writer. Both reached 30/30 recall, 6/6 critical tokens, 10/10 critical
slots, and zero unexpected critical tokens. One passed directly; the other was
below English precision only under incomplete v4 optional truth and passes
after the two verified source labels are included. Truncated or guessed sequence
labels remain unmatched. The 37,661-byte v5 manifest SHA-256 is
`d602d38cbaf6433338d371fbe0d42e8dd4fd3be55811ee428f2333127c0f276d`.
The isolated suite passes 588 tests, fixtures are byte-identical, `compileall`
passes, and changed Python files pass Ruff. Commit/push v5, repeat the clean
preflight, then run a new v5 evidence path; Phase 1 remains NO-GO meanwhile.

The complete v5 gate is preserved at
`evidence/phase1/phase1-quality-v5-2026-07-11-cn-beijing.json`, 95,483 bytes,
SHA-256
`0ceb74a7f05ed2ca5cbcac8eb3eb1c340dfac4bf43ceb84e6883cbe4c40e2343`.
All 13 calls returned, both full runs completed, and run B passed all six
dispatches. Run A failed only handwriting: 30/30 recall, 38/40 precision, 6/6
critical-token accuracy, and 10/10 slots, but one unexpected critical token.
The model hallucinated `111110` from six plasmid hatch strokes. Do not accept
those digits as optional truth. Add a generic hatch/fill/texture exclusion to
the prompt and test it without splitting `board` or weakening the gate. See
`docs/phase1_live_quality_result_v5_2026-07-11.md`.

Post-v5 diagnostics are recorded comprehensively in
`docs/phase1_v6_review_workflow_debug_2026-07-11.md`: 28 provider calls, 27
complete results, and one timeout. Single-pass hatch wording removed the
`111110` hallucination but still missed the center `+` stochastically. Broad and
focused crops were inconsistent; explicit glyph counting did not fix recall;
seeds 1234, 42, 3407, and 20260711 reproducibly missed the same `+`. Those paths
are rejected.

Three readable draft-to-review trials all passed, including one that repaired a
failing draft. JSON-string framing was too opaque and failed twice. The final
line-by-line quoted framing is both injection-resistant and readable; two actual
production `RecognitionPreferences(review_passes=1)` probes passed with 30/30
recall, 6/6 critical tokens, zero unexpected critical tokens, and metadata
reporting two provider calls.

`board.v6` implements that explicit one-model workflow. Review defaults off;
only an exact `RecognitionPreferences(review_passes=1)` enables one review. A
review failure fails the whole request, and only reviewed Markdown can be
returned or atomically written. The manifest is 37,685 bytes with SHA-256
`c058a68b4a17d1ed13c74bd31429269fc4287539afeb23e20c8dfb0be6f50a27`.
The gate remains 13 ordered recognition invocations but precommits 26 provider
calls and requires all 26 to be reported before GO. The isolated suite passes
599 tests; generated fixtures, compilation, Ruff, and diff checks pass. Commit
and push v6, then run a new clean 26-call evidence path.

The complete v6 gate is preserved at
`evidence/phase1/phase1-quality-v6-2026-07-11-cn-beijing.json`, 97,150 bytes,
SHA-256
`bc256bfbdc73f7d5f80806eb95767d4e68f17cb512f76c9e6daaba5278504707`.
All 13 recognition invocations and 26 provider calls returned, both full runs
completed, and run A passed. Handwriting passed in both runs: review fixed the
missing operator without hallucinating hatch digits. Run B failed only the
formula board because review changed source lowercase `s_4` to uppercase `S_4`.
The exact formula gate correctly rejected that one unexpected atom. Do not
accept uppercase as truth. Make v7 review conservative about changing exact
draft identifiers/case, then test handwriting repair and formula preservation.
See `docs/phase1_live_quality_result_v6_2026-07-11.md`.

That v7 wording experiment is rejected. Two handwriting trials still omitted
the center `+`, and two formula trials still changed `s_4` to `S_4`; all four
reviewed results failed after eight successful provider calls. The accepted
v8 design uses the same unified prompt and profile to produce two independent
drafts, then performs one pixel-grounded consensus review. The targeted
consensus result passed handwriting at 30/30 required recall and 10/10 slots,
and passed the formula board at 12/12 signatures and 133/133 atoms. One formula
consensus attempt timed out without publishing output; one bounded final-only
recovery reused the two complete drafts and passed.

`RecognitionPreferences(draft_candidates=2, review_passes=1)` explicitly opts
into the three-call workflow; defaults remain one candidate and no review. No
handwriting/formula branching exists. V8 evidence precommits 13 recognition
invocations and 39 provider calls. The 37,712-byte manifest SHA-256 is
`7200d16ea44b365301ce491bd3353433520d6c8ba2cc686debe6562173623e35`;
the isolated suite passes 608 tests. Complete offline preflight, commit/push,
then run a new clean v8 evidence path. See
`docs/phase1_v8_consensus_workflow_debug_2026-07-11.md`.

PDF, audio, video, worker/service, local OCR, provider pools, HarmonyOS, Rust,
Office, social, GPU, and offline-model work are not the next task.

## Do Not Do This

- Do not import `legacy_app.OCRLLM` from new downstream projects.
- Do not copy whole legacy files into `src/ocrllm`.
- Do not expose legacy processors as public API.
- Do not freeze a `1.0` API until real downstream usage proves it.
- Do not make the Rust plan active again without a measured reason.
- Do not add PyMuPDF or `fitz` to the active package; Phase 3 uses PDFium through
  `pypdfium2`.
- Do not start a later phase before the current GO gate passes.
- Do not begin or claim HarmonyOS/ArkTS compatibility.
- Do not claim support from code existence, mocks, installed dependencies, or
  historical logs alone.
- Do not make a paid provider call outside the versioned confirmed call plan, or
  before the intended Git/import/manifest/artifact preflight is clean and the
  new evidence path is proven absent.
- Do not pass fake callables or clocks into the public live runner or relabel
  simulated evidence as live. The public signature intentionally exposes no
  dependency-injection parameters.
- Do not retry one failed paid dispatch. Preserve the failed complete-run
  evidence and start a separately dispatched full run only under a new explicit
  decision.
- Do not claim the evidence checkpoint survives every sudden power loss. File
  data is flushed and `fsync`ed before atomic link/replace, but the containing
  directory is not explicitly `fsync`ed.

## Done Criteria For This Migration Step

- `START_HERE.md` gives an immediate visual split between active, legacy, and
  suspended areas.
- Root `README.md` explains the active path.
- `MIGRATION_STATUS.md` explains what changed and what to do next.
- `src/ocrllm/` is clearly marked as the active importable package.
- `Architecture.md` is clearly marked as suspended future planning.
- `legacy_app/` is clearly marked as old app/reference code.
- New tests prove the active import contract.
- `docs/ocrllm_library_go_no_go.md` is the single authoritative execution
  record and all navigation docs point to it.
- PDFium is the only active PDF decision; PyMuPDF is explicitly legacy-only.
- HarmonyOS/ArkTS is explicitly deferred.
