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

- `MIGRATION_STATUS.md`
- `docs/ocrllm_library_go_no_go.md`
- `src/ocrllm/README_ACTIVE_LIBRARY.md`
- `src/ocrllm/AGENTS.md`
- `docs/ocrllm_module_target_design.md`

Public import shape:

```python
from ocrllm import Config, DashScopeSettings, recognize
```

Current phase: **Phase 1 -- real board/image**. Phase 0 contract honesty is GO.
The active facade now decodes valid PNG/JPEG inputs before provider dispatch,
passes request-scoped validated snapshots isolated from later caller-path
changes to one synchronous injected provider,
rejects empty or control-only provider output, returns typed/redacted public
errors, and reports
canonical `source_type="image"` with `profile="board"`. File output remains
optional and atomic; `output_dir=None` stays memory-only. Pillow is installed by
the `image` extra and remains lazy during plain `import ocrllm`.

Phase 0 GO is a contract result, not a real recognition-capability claim. The
active library now has an offline-tested built-in DashScope adapter, but no
committed quality corpus/scorer, local OCR path, API-key pool,
retry/model-fallback policy, or resume support. PDF, audio, and video are also
unavailable. Phase 1 remains NO-GO pending reproducible image-quality and live
provider evidence. The adapter requires immutable `DashScopeSettings` with an
explicit region and OpenAI-compatible endpoint, accepts only `qwen3.7-plus` or
the default pinned `qwen3.7-plus-2026-05-26`, disables SDK retries, and sends
Base64 data URLs rather than local paths. Local user screenshots remain
uncommitted supplemental evidence; the GO gate still needs the committed
licensed five-class corpus, live smoke, and two complete live corpus runs. Read
`MIGRATION_STATUS.md` for current evidence and next steps, and
`docs/ocrllm_library_go_no_go.md` for exact gates, target responsibilities, and
the migrate/rewrite/reject matrix.

## Legacy Application

Path: `legacy_app/`

Use for:

- Read-only behavior reference for old GUI, CLI, FastAPI, processors, and
  launchers
- Historical outputs and incident records used to define active-library
  fixtures

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
Need to compare old product behavior       -> legacy_app/
Need to fix or maintain the old app        -> stop; require a separately scoped
                                               legacy-maintenance request
Need to record migration state             -> MIGRATION_STATUS.md
Need to decide GO/NO-GO or port behavior   -> docs/ocrllm_library_go_no_go.md
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
- Do not add PyMuPDF or `fitz` to the active library. Active PDF work uses
  PDFium through `pypdfium2` only after the PDF phase is authorized.
- Do not begin or claim HarmonyOS/ArkTS compatibility. It is deferred by the
  active GO/NO-GO decision.

## Verification Commands

The short local check is:

```bash
pip install -e .
python -c "import ocrllm; print(ocrllm.__version__)"
pytest
```

Before reporting completion, run the temporary-wheel install and outside-repo
heavy-module guard in `docs/ocrllm_library_go_no_go.md`.

Active-library migration tests must not modify or run the legacy suite as a
phase gate. Create fixtures and tests under root `tests/`. Legacy commands and
tests are historical reference unless a separate legacy-maintenance request
explicitly authorizes that work.
