# Active Library Package

This directory is the new `ocrllm` Python package. It is the only codebase in
this repo intended for direct import by other projects.

## Public Contract

```python
from ocrllm import (
    Cancelled,
    Config,
    ConfigError,
    DependencyMissing,
    InvalidSource,
    NoSpeechDetected,
    OCRLLMError,
    OutputError,
    OutputExists,
    ProviderError,
    QuotaExhausted,
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

This is not yet a completed recognition capability. There is no built-in real
provider, committed quality corpus/scorer, local OCR backend, key pool,
automatic retry/model fallback, or image resume. PDF, audio, and video are also
unavailable. Phase 1 is specifically one lazy DashScope vision adapter plus
reproducible quality and live-provider evidence.

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

```bash
pytest
```

The import contract must stay true:

```bash
python -c "import ocrllm; print(ocrllm.__version__)"
```
