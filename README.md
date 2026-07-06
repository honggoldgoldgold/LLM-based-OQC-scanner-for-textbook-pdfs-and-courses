# OCRLLM

Read this first if you are returning to the project after losing context:
`START_HERE.md`.

Then read `MIGRATION_STATUS.md` for the migration history and next steps.

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
START_HERE.md                         One-screen new/old/suspended repo map.
AGENTS.md                             Repo-level boundary instructions.
src/ocrllm/                           Active importable library package.
src/ocrllm/README_ACTIVE_LIBRARY.md   Local active-library boundary.
src/ocrllm/AGENTS.md                  Local active-library agent rules.
tests/                                Active library import-contract tests.
legacy_app/                           Old GUI/CLI/FastAPI application.
legacy_app/README_LEGACY.md           Local legacy-app boundary.
legacy_app/AGENTS.md                  Local legacy-app agent rules.
docs/                                 Active migration decisions.
Architecture.md                       Suspended future architecture reference.
output/, temp/, ocrllm_social_e2e/    Runtime artifacts, not source.
```

## Legacy Runtime Notes

The old GUI, Codex video mode, Filetrans audio mode, and Bilibili/social-long
workflow are legacy compatibility surfaces under `legacy_app/`. Current
runtime incident notes live in:

```text
docs/legacy_filetrans_codex_debug_record.md
```

As of the 2026-07-06 robustness audit, the supervised legacy course runs were
considered clean only when every target course folder had exactly these two
Markdown artifacts and no known dirty failure markers:

```text
*_æ¿ä¹¦è¯†åˆ«.md
*_å½•éŸ³è¯†åˆ«.md
```

Known dirty markers include Codex batch/frame placeholders, `Reading additional
input from stdin`, `[WinError 10061]`, embedded Codex diagnostic dumps, or a
missing board/audio Markdown after the job has completed. These checks belong
to the legacy workflow; they are not part of the public `ocrllm` library API.

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
