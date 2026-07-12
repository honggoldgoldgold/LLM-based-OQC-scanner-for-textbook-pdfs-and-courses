# Active Library Package

This directory is the new `ocrllm` Python package. It is the only codebase in
this repo intended for direct import by other projects.

## Public Contract

```python
from ocrllm import (
    Cancelled,
    CapabilityReport,
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
    get_capabilities,
)
```

Phase 0 contract honesty and Phase 1 real board/image are GO. The current phase
is **Phase 2 -- versioned JSON contract and Electron JSONL worker**.

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

The built-in DashScope board/image capability is available under the bounded
Phase 1 contract. The v17 Beijing gate completed exactly 52 provider calls with
no retry; both independent full-corpus runs passed. Run B repaired exactly one
missing handwriting sign through generic two-of-three omission consensus; no
handwriting route or model split exists. The committed Git-archive wheel then
passed base, `image`, and `image,dashscope` clean profiles.
`get_capabilities()` reports every known atomic capability without a network
call or optional import. With an explicit config, it reports that exact
workflow's proven status rather than treating installed code as sufficient.
Phase 2 also has an experimental spawned one-job manager with bounded JSON event
bridging and verified five-second descendant cancellation. It is not exposed as
a production worker until the remaining gates pass. The production image job
adapter now reuses this same unified facade once per ordered group, fixes the
Beijing v17 configuration, and adds no handwriting route, fallback, or retry.
`python -m ocrllm.worker` now composes that adapter with the isolated manager;
it remains a development worker until the Node and live gates pass.
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
evidence baseline. There is still no local OCR backend, key pool, automatic
retry/model fallback, or image resume; PDF, audio, and video remain unavailable.
Local user screenshots are uncommitted
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
