# START HERE: OCRLLM Repo Map

This repo currently contains two codebases. Treat the directory boundary as a
hard signal before editing or importing anything.

## Active New Library

Path: `src/ocrllm/`

Use for:

- New importable package: `ocrllm`
- Stable public API work
- New downstream project dependencies
- Root test suite under `tests/`

Read next:

- `src/ocrllm/README_ACTIVE_LIBRARY.md`
- `src/ocrllm/AGENTS.md`
- `docs/ocrllm_module_target_design.md`

Public import shape:

```python
from ocrllm import Config, recognize
```

## Legacy Application

Path: `legacy_app/`

Use for:

- Old GUI, CLI, FastAPI, processors, and launchers
- GUI launcher fixes for `legacy_app/launch_gui.bat`
- Behavior reference while porting one tested vertical slice at a time
- Legacy test suite under `legacy_app/tests/`

Read next:

- `legacy_app/README_LEGACY.md`
- `legacy_app/AGENTS.md`
- `docs/legacy_bilibili_social_long_debug_record.md` for multi-part Bilibili
  course download/recognition recovery.
- `docs/legacy_youtube_playlist_social_long_workflow.md` for YouTube playlist
  course download/recognition recovery.
- `docs/legacy_filetrans_codex_debug_record.md` for Codex/FileTrans recovery.

Do not use as a new dependency boundary:

```python
import legacy_app.OCRLLM
```

## Suspended Future Plan

Path: `Architecture.md`

Status: future plan, currently suspended.

Do not make the Rust/PyO3 rewrite active again until the Python import contract
has real downstream usage and stable module boundaries.

## Runtime Artifacts

These paths are not source-of-truth code:

- `output/`
- `temp/`
- `ocrllm_social_e2e/`
- `.pytest_cache/`
- `__pycache__/`

Do not infer architecture from generated output or temporary files.

## Choose The Edit Location

```text
Need to change the public library API      -> src/ocrllm/ and tests/
Need to add a downstream import feature    -> src/ocrllm/ and tests/
Need to fix GUI launcher/Codex/Google UI   -> legacy_app/
Need to compare old product behavior       -> legacy_app/
Need to record migration state             -> MIGRATION_STATUS.md
Need to debug Bilibili social-long courses -> docs/legacy_bilibili_social_long_debug_record.md
Need to debug YouTube playlist courses    -> docs/legacy_youtube_playlist_social_long_workflow.md
Need to design the completed module shape  -> docs/ocrllm_module_target_design.md
Need to revisit future Rust/PyO3 design    -> Architecture.md
```

## Do Not Cross These Boundaries

- Do not import `legacy_app.OCRLLM` from new downstream projects.
- Do not copy a whole legacy module into `src/ocrllm`.
- Do not let `import ocrllm` pull GUI, FastAPI, social downloader, or heavy
  media dependencies.
- Do not treat `Architecture.md` as the active implementation plan.
- Do not put runtime output defaults inside package directories.

## Verification Commands

Root library contract:

```bash
pip install -e .
python -c "import ocrllm; print(ocrllm.__version__)"
pytest
```

Legacy app checks must be run from the legacy context and may include external
service tests. Prefer targeted tests when changing launchers, GUI settings, or
provider mode routing.
