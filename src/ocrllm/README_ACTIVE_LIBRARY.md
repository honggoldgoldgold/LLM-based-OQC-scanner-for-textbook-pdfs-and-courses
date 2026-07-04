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
    ConfigError,
    QuotaExhausted,
    UnsupportedFormat,
    Cancelled,
)
```

The first supported vertical slice is board/image recognition through an
injected provider. Real DashScope, Google, PDF, audio, and video providers have
not been ported into this package yet.

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

## Tests

Use the root test suite for this package:

```bash
pytest
```

The import contract must stay true:

```bash
python -c "import ocrllm; print(ocrllm.__version__)"
```
