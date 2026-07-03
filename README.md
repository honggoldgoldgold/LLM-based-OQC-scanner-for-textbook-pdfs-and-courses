# OCRLLM

Read this first if you are returning to the project after losing context:
`MIGRATION_STATUS.md`.

OCRLLM is now being extracted into a Python library that other projects can
import as `ocrllm`. The previous application code was moved into
`legacy_app/` and should be treated as a reference implementation, not as the
dependency surface for new projects.

## Active Direction

The active package is `src/ocrllm`.

The active goal is small and concrete:

- Make `pip install -e .` work.
- Make `import ocrllm` work from any current working directory.
- Expose a stable facade: `Config`, `RecognitionResult`, `recognize`,
  `recognize_batch`, and public errors.
- Support the first vertical slice: board/image recognition through an injected
  provider.
- Keep file output optional. `output_dir=None` means in-memory results only.

The old Rust/PyO3 rewrite plan in `Architecture.md` is suspended and kept only
as a future reference.

## Current Public API

```python
from ocrllm import Config, recognize


class Provider:
    def recognize_images(self, image_paths, *, prompt, config):
        return "# Recognized board\n"


result = recognize("board.jpg", config=Config(provider=Provider()))
print(result.markdown)
```

## Repository Map

```text
src/ocrllm/          Active importable library package.
tests/               Active library import-contract tests.
legacy_app/          Old GUI/CLI/FastAPI application and old tests/docs.
docs/                Active migration decisions for the new library.
Architecture.md      Suspended future architecture reference.
```

## Rules For New Work

- New projects should import only from `ocrllm`, never from `legacy_app`.
- Do not port a legacy module wholesale. Extract one tested vertical slice at a
  time.
- Do not make GUI, FastAPI, social download, or heavyweight media dependencies
  import on `import ocrllm`.
- Do not make package-relative output directories the default.
- Keep the public API boring and stable before revisiting Rust internals.

## Verification

```bash
pip install -e .
python -c "import ocrllm; print(ocrllm.__version__)"
pytest
```
