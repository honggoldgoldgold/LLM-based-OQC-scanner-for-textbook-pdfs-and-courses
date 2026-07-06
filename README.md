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
docs/legacy_bilibili_social_long_debug_record.md
docs/legacy_filetrans_codex_debug_record.md
```

Use the Bilibili record first when touching multi-part Bilibili course
downloads, comment/danmaku capture, `social_long --parts`, social URL input, or
resume behavior for the legacy course workflow.

As of the 2026-07-06 robustness audit, the supervised Bilibili CS231n course
run was considered clean only when the output tree had all of the following:

```text
33 part directories
33 downloaded MP4 files
33 *_板书识别.md files
33 *_录音识别.md files
0 FileTrans task sidecars
bilibili_social_context.md with shared comments, resource links, and per-part danmaku
```

For any completed legacy course/video folder, the expected per-part recognition
artifacts are exactly these two Markdown files:

```text
*_板书识别.md
*_录音识别.md
```

Known dirty markers include Codex batch/frame placeholders, `Reading additional
input from stdin`, `[WinError 10061]`, embedded Codex diagnostic dumps, or a
missing board/audio Markdown after the job has completed. These checks belong
to the legacy workflow; they are not part of the public `ocrllm` library API.

The reusable Bilibili course command is documented in
`docs/legacy_bilibili_social_long_debug_record.md`; it intentionally runs
through the legacy CLI:

```powershell
$env:PYTHONPATH='legacy_app'
D:\Anaconda\envs\OCRLLM\python.exe -m OCRLLM.cli social_long <bilibili-url> `
  --parts 1-33 --resume -o output\bilibili_cs231n_full
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
