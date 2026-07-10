# Active Library Package

This directory is the new `ocrllm` Python package. It is the only codebase in
this repo intended for direct import by other projects.

## Public Contract

```python
from ocrllm import (
    Config,
    RecognitionResult,
    recognize,
    recognize_batch,
    OCRLLMError,
    ConfigError,
    QuotaExhausted,
    UnsupportedFormat,
    Cancelled,
)
```

The current implementation is a Phase 0 facade, not a completed recognition
feature. It routes board/image paths to an injected provider, but input
validation and a built-in real provider have not been ported yet. PDF, audio,
and video are unsupported.

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
