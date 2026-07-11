# Active Library Package

This directory is the new `ocrllm` Python package. It is the only codebase in
this repo intended for direct import by other projects.

## Public Contract

```python
from ocrllm import (
    Cancelled,
    Config,
    ConfigError,
    DashScopeSettings,
    DependencyMissing,
    InvalidSource,
    NoSpeechDetected,
    OCRLLMError,
    OutputError,
    OutputExists,
    ProviderError,
    ProviderUnavailable,
    QuotaExhausted,
    RateLimited,
    RecognitionResult,
    UnsupportedFormat,
    recognize,
    recognize_batch,
)
```

Phase 0 contract honesty is GO. The current phase is **Phase 1 -- real
board/image**.

The current image facade:

- accepts `.png`, `.jpg`, and `.jpeg`;
- decodes and validates every input before provider dispatch;
- copies validated bytes into request-scoped snapshots isolated from later
  caller-path changes;
- passes those ordered snapshots to one synchronous injected provider;
- rejects invalid provider output and maps failures to typed/redacted errors;
- returns `source_type="image"` and `profile="board"`;
- keeps output in memory unless `output_dir` requests atomic Markdown output;
- loads Pillow lazily from the optional `ocrllm[image]` extra.
- resolves the exact built-in provider name `"dashscope"` only when immutable
  `DashScopeSettings` is present, while keeping `openai` and `httpx` lazy behind
  `ocrllm[dashscope]`.
- freshly revalidates an exact public `Config`; injected providers retain the
  caller's config identity, while the built-in adapter uses an isolated,
  revalidated copy.

This is not yet a completed recognition capability. The built-in DashScope
adapter, exact offline boundary tests, committed licensed five-class corpus,
deterministic scorers, and guarded evidence runner now exist. Required live
provider evidence does not: Phase 1 remains NO-GO and no image/provider
capability is `available` until the clean smoke, both independently dispatched
full-corpus runs, final clean profiles, and explicit GO-decision update pass.
The adapter requires an explicit matching region and endpoint, accepts
`qwen3.7-plus`, the default pinned `qwen3.7-plus-2026-05-26`, and explicit
configured scout work, disables OpenAI SDK retries, and builds Base64 data
URLs rather than sending local paths. The v17 evidence candidate uses one
thinking-enabled pinned Qwen3.7 transcript plus three independent
thinking-enabled omission ledgers from the same pinned model, each conditioned
on the quoted inert primary. Only exact allowlisted records can reach
two-of-three deterministic quorum; scout prose and unsupported punctuation
cannot enter the result. Directional-arrow insertion is forbidden while
complete primary transcription remains unchanged. Exact dynamic scout-prompt
hashes and byte counts are returned in metadata.
Qwen-VL Max remains an explicit supported scout option but is not the Phase 1
evidence baseline. There is still no local OCR
backend, key pool, automatic retry/model fallback, or image resume; PDF, audio,
and video remain unavailable. Local user screenshots are uncommitted
supplemental material and never replace the committed corpus in pass/fail
evidence.

Read `../../docs/ocrllm_library_go_no_go.md` before active-library work. It is
the authoritative source for file responsibilities, GO gates, and the
migrate/rewrite/reject boundary.

## Belongs Here

- Stable public API code.
- Provider interfaces and small provider adapters after they are tested.
- Dependency-light processing code that can be imported safely.
- Behavior ported from `legacy_app/` one tested vertical slice at a time.

## Does Not Belong Here

- PyQt GUI code.
- FastAPI server code.
- Social downloader integrations.
- Desktop launcher behavior.
- Package-relative runtime output defaults.
- Direct imports from `legacy_app` or uppercase `OCRLLM`.
- PyMuPDF or `fitz`; the future PDF slice uses PDFium through `pypdfium2`.
- HarmonyOS/ArkTS code or compatibility claims; that work is deferred.

## Tests

Use the root test suite for this package:

```powershell
uv run --no-project --isolated --with 'Pillow==12.3.0' `
  --with 'pytest>=8,<10' --with 'openai>=2.30,<3' `
  --python 'D:\Anaconda\envs\OCRLLM\python.exe' `
  python -m pytest -q -p no:cacheprovider
```

The import contract must stay true:

```powershell
& 'D:\Anaconda\envs\OCRLLM\python.exe' -c `
  "import sys; sys.path.insert(0, 'src'); import ocrllm; print(ocrllm.__version__)"
```
