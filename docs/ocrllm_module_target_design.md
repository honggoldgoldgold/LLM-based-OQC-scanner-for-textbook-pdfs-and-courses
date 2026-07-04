# OCRLLM Module Target Design

Status: target-state design map.

This document describes the intended completed `ocrllm` Python module as if the
library already exists. It is not a promise that every name below is frozen.
Implementation may change when tests, downstream usage, or dependency reality
prove a better shape.

The active implementation remains the Python-first package in `src/ocrllm`.
The Rust/PyO3 plan in `Architecture.md` is suspended future planning.

## One-Sentence Goal

`ocrllm` is an importable Python library that turns boards, screenshots, PDFs,
audio, video, and selected office documents into structured Markdown through a
small public API, explicit providers, optional dependencies, and tested vertical
slices.

## Architectural Judgment

The library must not be a renamed copy of the old application. The old app is a
behavior reference, not a module boundary.

The old codebase contains valuable product knowledge, but its shape is hostile
to library reuse:

- GUI, CLI, FastAPI, downloader, provider, and processor concerns were mixed.
- Runtime output defaults lived too close to package code.
- Large files carried multiple responsibilities.
- Broad exception handling made failure modes hard to trust.
- Internal classes leaked before there was a stable facade.

The correct move is a library extraction, not a heroic rewrite. Build a small
facade first, port one vertical slice at a time, and let downstream imports
prove the boundary before optimizing internals.

## Non-Negotiable Boundaries

- `import ocrllm` must stay lightweight.
- No GUI import at module import time.
- No FastAPI import at module import time.
- No social downloader import at module import time.
- No browser automation import at module import time.
- No `legacy_app` or uppercase `OCRLLM` imports from `src/ocrllm`.
- No output files unless the caller explicitly requests output.
- No package-relative runtime output or temp defaults.
- No public API that exposes legacy processor classes directly.
- No silent catch-all error handling.
- No Rust/PyO3 dependency until the Python module boundary is proven.

## Completed User Experience

The completed package should feel boring to import and predictable to call:

```python
from ocrllm import Config, recognize

result = recognize(
    "lecture_board.png",
    config=Config(
        provider="dashscope",
        api_key="sk-...",
        model="qwen-vl-max",
    ),
)

print(result.markdown)
```

For batch use:

```python
from ocrllm import Config, recognize_batch

results = recognize_batch(
    ["board.png", "slides.pdf", "lecture.mp4"],
    config=Config(provider="dashscope", output_dir="out"),
)
```

For downstream projects that already own provider clients:

```python
from ocrllm import Config, recognize


class ExistingVisionClient:
    def recognize_images(self, image_paths, *, prompt, config):
        return "# Recognized content\n"


result = recognize(
    "board.jpg",
    config=Config(provider=ExistingVisionClient()),
)
```

The dependency surface should support both modes:

- Built-in provider adapters for normal users.
- Injected provider objects for host applications that already manage clients,
  billing, logging, retries, secrets, and network policy.

## Public API

The public API should be small. Everything else is internal unless explicitly
documented.

```python
from ocrllm import (
    Config,
    RecognitionResult,
    recognize,
    recognize_batch,
    OCRLLMError,
    ConfigError,
    ProviderError,
    QuotaExhausted,
    UnsupportedFormat,
    Cancelled,
)
```

### `recognize`

```python
def recognize(
    source: str | Path | Sequence[str | Path],
    *,
    config: Config | None = None,
) -> RecognitionResult:
    ...
```

Purpose:

- Recognize one source.
- Recognize a same-type group, such as multiple board screenshots that share
  context.
- Route by file type.
- Return exactly one `RecognitionResult`.

Rules:

- A mixed-type list belongs in `recognize_batch`, not `recognize`.
- Missing files should fail before provider calls.
- Unsupported extensions should raise `UnsupportedFormat`.
- Provider configuration problems should raise `ConfigError`.
- Provider runtime failures should raise a provider-specific public error.
- Partial output is allowed only when represented explicitly in the result.

### `recognize_batch`

```python
def recognize_batch(
    sources: Iterable[str | Path | Sequence[str | Path]],
    *,
    config: Config | None = None,
) -> list[RecognitionResult]:
    ...
```

Purpose:

- Recognize independent sources.
- Return one result per input item.
- Preserve input order.
- Allow safe per-item failure policy later without changing the single-file API.

Default behavior should be fail-fast. A later `BatchPolicy` can add
`continue_on_error` without changing `recognize`.

### `Config`

`Config` is immutable and safe to pass across calls.

Target fields:

```python
@dataclass(frozen=True, slots=True)
class Config:
    provider: str | object | None = None
    api_key: str | None = None
    model: str | None = None
    model_queue: tuple[str, ...] = ()
    output_dir: str | Path | None = None
    temp_dir: str | Path | None = None
    cache_dir: str | Path | None = None
    parallel_requests: int = 8
    timeout_seconds: float = 120.0
    resume: bool = True
    overwrite: bool = False
    progress: object | None = None
    cancellation: object | None = None
    extra: Mapping[str, Any] = field(default_factory=dict)
```

Design rules:

- `output_dir=None` means memory-only result.
- `temp_dir=None` means a safe OS temp location, not a package directory.
- `cache_dir=None` means a platform cache location, not a package directory.
- API keys come from explicit config or environment variables.
- Config loading from files can exist, but it must not happen implicitly on
  `import ocrllm`.
- Provider-specific options belong in provider adapters or `extra`, not as an
  exploding list of top-level fields.

### `RecognitionResult`

`RecognitionResult` is the only normal successful return type.

Target fields:

```python
@dataclass(frozen=True, slots=True)
class RecognitionResult:
    markdown: str
    source_type: str
    output_path: Path | None = None
    assets: tuple[Path, ...] = ()
    hotwords: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)
```

Design rules:

- `markdown` is always the primary result.
- `output_path` is `None` unless the caller requested file output.
- `assets` contains generated side files, not internal temp files.
- `hotwords` is non-empty only when a processor extracts useful terms.
- `warnings` contains degraded-but-successful conditions.
- `metadata` is structured, stable enough for debugging, and not required for
  normal user workflows.

### Public Errors

Every error type should communicate the failure category without requiring
string matching.

```text
OCRLLMError          Base public exception.
ConfigError         Invalid or missing caller configuration.
ProviderError       Provider call failed for a non-quota reason.
QuotaExhausted      All configured model or key options were exhausted.
UnsupportedFormat   The source cannot be routed to a supported processor.
Cancelled           Caller cancellation was honored.
```

Rules:

- No bare `except Exception` in processor or provider paths unless immediately
  wrapped into a public error with useful context.
- Provider HTTP status, model name, and request category should be preserved in
  error metadata where practical.
- Secret values must never appear in exception messages.

## Package Layout

Target layout:

```text
src/ocrllm/
  __init__.py                 Public facade only.
  api.py                      recognize and recognize_batch.
  config.py                   Immutable Config and config normalization.
  result.py                   RecognitionResult.
  errors.py                   Public exception hierarchy.
  protocols.py                Runtime-checkable provider/progress protocols.
  routing.py                  Source type detection and processor routing.

  processors/
    __init__.py               Internal processor package marker.
    board.py                  Board and screenshot recognition.
    pdf.py                    PDF recognition.
    audio.py                  Audio transcription and Markdown assembly.
    video.py                  Video extraction, board recognition, ASR merge.
    office.py                 DOCX/PPTX text extraction where supported.

  providers/
    __init__.py               Provider adapter exports.
    base.py                   Provider protocols and capability checks.
    dashscope.py              DashScope adapter.
    google.py                 Google adapter.
    openai_compatible.py      OpenAI-compatible vision/audio adapter.
    retry.py                  Retry, backoff, model fallback.
    key_pool.py               Optional multi-key rotation.

  imaging/
    __init__.py
    load_image.py             Image loading and format normalization.
    resize_image.py           Size limits for provider requests.
    preprocess_board.py       Crop, contrast, and board cleanup.

  pdf/
    __init__.py
    render_pages.py           PDF page rendering behind optional dependency.
    extract_text.py           Text-layer extraction when useful.
    split_pages.py            Page selection and batching.

  media/
    __init__.py
    find_ffmpeg.py            ffmpeg and ffprobe discovery.
    extract_audio.py          Video to audio extraction.
    split_audio.py            Long audio chunking.
    extract_frames.py         Video frame sampling.
    detect_slide_changes.py   Frame deduplication and slide changes.

  output/
    __init__.py
    write_markdown.py         Optional Markdown file output.
    resume_markdown.py        Resume state stored in output where applicable.
    naming.py                 Stable output filenames.

  testing/
    __init__.py
    fake_provider.py          Test helper for downstream projects.
```

This layout is a target, not a mandate. The rule that matters is one file, one
responsibility. If a file needs more than a short phrase to describe its job,
split it.

## Layering

Allowed dependency direction:

```text
errors/result/config
        |
protocols/routing
        |
providers   imaging/pdf/media/output
        \       |       |       /
             processors
                 |
                api
                 |
             __init__.py
```

Rules:

- `__init__.py` re-exports only public names.
- `api.py` orchestrates; it does not perform OCR, PDF rendering, ASR, or ffmpeg
  work directly.
- Processors call helpers and providers.
- Helpers do not call processors.
- Providers do not know about output files.
- Output writers do not know about providers.
- Tests may use public APIs first and internals only for narrow unit coverage.

## Processor Contracts

Each processor should be a vertical slice with the same basic shape:

```python
def recognize_<type>(
    paths: Sequence[Path],
    *,
    config: Config,
    provider: object,
) -> RecognitionResult:
    ...
```

The exact function signature can change, but the responsibility must not.

### Board Processor

Input:

- `.jpg`
- `.jpeg`
- `.png`
- `.bmp`
- `.webp`
- `.heic`
- `.heif`
- `.tif`
- `.tiff`

Responsibilities:

- Validate files.
- Normalize images only when needed.
- Preserve multi-image order.
- Build the board prompt.
- Call a vision-capable provider.
- Return Markdown.
- Optionally write Markdown output.

Must not:

- Import GUI code.
- Decide provider billing policy.
- Hide provider failures as empty Markdown.

### PDF Processor

Input:

- `.pdf`

Responsibilities:

- Decide text-layer path versus page-image path.
- Render pages through an optional PDF dependency.
- Batch pages predictably.
- Preserve page markers in Markdown.
- Support resume when output is long-running.

Must not:

- Make PDF dependencies required for board-only installs.
- Write temporary pages into the package directory.
- Treat every PDF as image-only without checking whether text extraction is
  better.

### Audio Processor

Input:

- `.wav`
- `.mp3`
- `.m4a`
- `.aac`
- `.flac`
- `.ogg`
- `.opus`
- `.wma`

Responsibilities:

- Probe duration.
- Choose direct transcription or chunked transcription.
- Preserve timestamps when available.
- Merge transcript chunks into coherent Markdown.
- Extract hotwords when useful.

Must not:

- Swallow failed chunks silently.
- Require video dependencies for audio-only use.
- Mix provider retry policy into audio splitting code.

### Video Processor

Input:

- `.mp4`
- `.avi`
- `.mkv`
- `.mov`
- `.flv`
- `.wmv`

Responsibilities:

- Extract audio.
- Sample frames.
- Deduplicate near-identical frames.
- Recognize visual board/slide content.
- Transcribe audio.
- Merge visual and transcript streams into one Markdown document.

Must not:

- Own the generic audio processor.
- Own generic ffmpeg discovery.
- Make social downloader behavior part of core video recognition.

### Office Processor

Input:

- `.docx`
- `.pptx`

Responsibilities:

- Extract text and embedded media when dependencies allow.
- Preserve headings, slide/page boundaries, and images where useful.
- Return Markdown.

Must not:

- Support old binary `.doc` or `.ppt` as a first target.
- Pull office dependencies into `import ocrllm`.

## Provider Contracts

Provider adapters are replaceable. Processors should care about capabilities,
not vendor classes.

Minimum target capabilities:

```python
class VisionProvider(Protocol):
    def recognize_images(
        self,
        image_paths: Sequence[Path],
        *,
        prompt: str,
        config: Config,
    ) -> str:
        ...


class AudioProvider(Protocol):
    def transcribe_audio(
        self,
        audio_path: Path,
        *,
        prompt: str | None,
        config: Config,
    ) -> str:
        ...
```

Provider resolution:

```text
Config.provider is an object       -> use it directly after capability checks.
Config.provider is a string        -> load the matching built-in adapter.
Config.provider is None            -> use a documented default only if safe.
```

Critical rule: provider adapters own HTTP details, authentication, request
format, and response parsing. Processors own media-specific workflow.

## Optional Dependencies

The base install should support importing the package and running fake-provider
board tests.

Target extras:

```text
ocrllm[image]    Image loading, conversion, preprocessing.
ocrllm[pdf]      PDF rendering and text extraction.
ocrllm[audio]    Audio probing and transcription helpers.
ocrllm[video]    ffmpeg-based video/audio helpers.
ocrllm[providers] Built-in network provider adapters.
ocrllm[all]      All supported optional features.
ocrllm[dev]      Test and development tools.
```

Rules:

- Missing optional dependencies should raise `ConfigError` or a dedicated
  dependency error with the required extra name.
- Optional dependency imports should live inside the function or module that
  needs them.
- Importing `ocrllm` must not require ffmpeg, PyQt, FastAPI, browser tools, or
  provider SDKs.

## Output And Resume

The default result is in memory.

When `output_dir` is set:

- Create the directory if needed.
- Use deterministic output names.
- Return the Markdown path in `RecognitionResult.output_path`.
- Store only user-meaningful assets in `RecognitionResult.assets`.

Resume support should be added only for long-running processors where it is
worth the complexity:

- PDF.
- Audio.
- Video.

Resume state should live with output files or in an explicit caller-provided
state path. It must not depend on hidden package directories.

## Configuration And Secrets

Secret lookup order:

```text
Explicit Config.api_key
Provider-specific environment variable
OCRLLM_API_KEY
ConfigError
```

Provider-specific examples:

```text
DASHSCOPE_API_KEY
GOOGLE_API_KEY
OPENAI_API_KEY
```

Rules:

- Never persist API keys.
- Never print API keys.
- Never include API keys in exceptions, warnings, result metadata, or logs.
- Do not silently fall back to a different paid provider.

## Testing Strategy

Tests define the real contract. Documentation does not.

Required test groups:

```text
tests/test_import_contract.py        Public imports and fake-provider board path.
tests/test_routing.py                Extension routing and mixed input rules.
tests/test_config.py                 Config normalization and secret lookup.
tests/test_errors.py                 Public error categories.
tests/test_output.py                 In-memory versus file output.
tests/test_provider_contracts.py     Fake provider capability checks.
tests/test_board_processor.py        Board vertical slice.
tests/test_pdf_processor.py          PDF vertical slice with local fixtures.
tests/test_audio_processor.py        Audio vertical slice with local fixtures.
tests/test_video_processor.py        Video vertical slice with local fixtures.
```

Network provider tests should be opt-in and skipped by default unless required
environment variables are present.

Golden tests should exist for behavior preservation, but they must be small and
reviewable. They should prove output structure, not exact provider wording.

## Completion Criteria

The module can be considered library-complete only when these are true:

- `pip install -e .` works.
- `pip install .` builds a wheel.
- `import ocrllm` works from outside the repo.
- `import ocrllm` has no heavyweight side effects.
- The public facade is documented and tested.
- Board recognition works with fake and real providers.
- PDF, audio, and video are separate tested vertical slices.
- Optional dependencies are isolated behind extras.
- Output defaults are safe for installed-package use.
- Errors are typed and do not require string matching.
- At least one downstream project imports the package without using
  `legacy_app`.

## Implementation Phases

### Phase 0: Keep The Import Contract Honest

Current active phase.

- Preserve the small public facade.
- Keep fake-provider board recognition passing.
- Keep `import ocrllm` lightweight.
- Add tests before widening the API.

### Phase 1: Real Board Slice

- Add image validation.
- Add optional image preprocessing.
- Add one real provider adapter.
- Keep provider injection working.
- Add representative board fixtures.

### Phase 2: Routing And Output Hardening

- Move source detection into `routing.py`.
- Add deterministic output naming.
- Add explicit missing-file behavior.
- Add output tests.

### Phase 3: PDF Slice

- Add optional PDF extra.
- Add page rendering and/or text extraction.
- Add page-batched provider calls.
- Add resume only if needed.

### Phase 4: Audio Slice

- Add optional audio extra.
- Add duration probing.
- Add short and long audio paths.
- Add provider transcription capability.

### Phase 5: Video Slice

- Add optional video extra.
- Add ffmpeg discovery.
- Add frame extraction and deduplication.
- Reuse audio and board logic instead of duplicating them.

### Phase 6: Packaging And Downstream Proof

- Build wheels.
- Test installation from another project.
- Document extras.
- Keep the old app isolated under `legacy_app`.

### Phase 7: Revisit Rust Only With Evidence

Rust can be reconsidered only when:

- A Python module boundary is stable.
- A specific module has measured performance or reliability pressure.
- Golden tests can compare behavior before and after replacement.
- The Rust build does not make basic Python installation fragile.

## Rejection Rules

Reject changes that do any of the following:

- Add a dependency that imports on `import ocrllm` without being needed by the
  facade.
- Copy a whole legacy file into the active package.
- Make downstream callers import internal processors for normal use.
- Add global mutable settings as the primary configuration mechanism.
- Add hidden output paths under `src/ocrllm`.
- Add broad exception swallowing around provider or processor logic.
- Put GUI, server, or social downloader behavior into the core library.

## Reader Reset

When returning after losing context, use this order:

1. `START_HERE.md`
2. `MIGRATION_STATUS.md`
3. `docs/library_migration_decision.md`
4. `docs/ocrllm_module_target_design.md`
5. `src/ocrllm/README_ACTIVE_LIBRARY.md`
6. `tests/test_import_contract.py`

The current implementation is smaller than this document. That is intentional.
This file is a map for the completed module, not evidence that the module is
already complete.
