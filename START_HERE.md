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
- `docs/provider_cost_and_reliability_policy.md`
- `docs/phase1_implementation_record.md`
- `docs/phase1_live_quality_result_v17_2026-07-11.md`
- `docs/phase2_worker_command_contract_2026-07-11.md`
- `docs/phase2_worker_event_contract_2026-07-11.md`
- `docs/phase2_worker_jsonl_io_2026-07-11.md`
- `docs/phase2_capability_control_loop_2026-07-12.md`
- `docs/phase2_isolated_job_manager_2026-07-12.md`
- `docs/phase2_production_image_job_2026-07-12.md`
- `docs/phase2_production_worker_entrypoint_2026-07-12.md`
- `docs/phase2_node_worker_harness_2026-07-12.md`
- `docs/phase2_live_worker_result_2026-07-12.md`

Public import shape:

```python
from ocrllm import Config, DashScopeSettings, recognize
```

Current phase: **Phase 2 -- versioned JSON contract and Electron JSONL
worker**. Phase 0 contract honesty and Phase 1 real board/image are GO.
The active facade now decodes valid PNG/JPEG inputs before provider dispatch,
passes request-scoped validated snapshots isolated from later caller-path
changes to one synchronous injected provider,
rejects empty or control-only provider output, returns typed/redacted public
errors, and reports
canonical `source_type="image"` with `profile="board"`. File output remains
optional and atomic; `output_dir=None` stays memory-only. Pillow is installed by
the `image` extra and remains lazy during plain `import ocrllm`.

Phase 1 uses one unified `board.v17` workflow for printed, projected,
handwritten, formula, table, and ordered-image inputs. The Beijing live gate
completed all 13 recognitions and exactly 52 provider calls with no retry or
terminal failure. Both independent six-dispatch runs passed. Run A required no
restoration; Run B restored exactly one missing handwriting sign through the
same generic two-of-three omission-scout path used for every image class.

Preserve
`evidence/phase1/phase1-quality-v17-2026-07-11-cn-beijing.json`: 107,246
bytes, SHA-256
`6f0454d634dbe76f68f29c07a4c0ced4a047c080e46bb75dda2cb84ffca3a96b`.
The clean Git-archive gate at `0278b66` passed 712 tests, fixture-byte identity,
compilation, a 67,266-byte wheel, base import and timing budgets, a generated
image recognition, and fresh `image` plus Beijing `image,dashscope` profiles.
The image/provider capabilities are available; this authorizes only Phase 2.

The active library still has no local OCR path, API-key pool,
retry/model-fallback policy, resume support, PDF, audio, or video support. Local
user PDFs/screenshots under `docs/` remain untracked supplemental test material,
not redistributable gate evidence. Read
`MIGRATION_STATUS.md` for current evidence and next steps, and
`docs/ocrllm_library_go_no_go.md` for exact gates, commands, target
responsibilities, and the migrate/rewrite/reject matrix.

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

The pinned offline checkpoint checks are:

```powershell
uv run --no-project --isolated --with 'Pillow==12.3.0' `
  --with 'pytest>=8,<10' --with 'openai>=2.30,<3' `
  --python 'D:\Anaconda\envs\OCRLLM\python.exe' `
  python -m pytest -q -p no:cacheprovider
uv run --no-project --isolated --with 'Pillow==12.3.0' `
  --python 'D:\Anaconda\envs\OCRLLM\python.exe' `
  python -m tests.quality.generators.generate_phase1_fixtures --check
& 'D:\Anaconda\envs\OCRLLM\python.exe' -m compileall -q src tests
```

Before reporting completion, run the clean Git-archive wheel build, isolated
install, and outside-repo heavy-module guard in
`docs/ocrllm_library_go_no_go.md`. Do not run the paid live gate until the
exact region/`base_url` is confirmed by the caller and the runner's Git/import,
manifest, artifact, and credential preflight passes.

Active-library migration tests must not modify or run the legacy suite as a
phase gate. Create fixtures and tests under root `tests/`. Legacy commands and
tests are historical reference unless a separate legacy-maintenance request
explicitly authorizes that work.
