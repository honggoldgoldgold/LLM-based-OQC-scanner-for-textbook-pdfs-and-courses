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
active library has an offline-tested built-in DashScope adapter. Offline
checkpoint `e328253` also commits the licensed five-class Phase 1 corpus,
deterministic generators, scorers, and integrated manifest-authenticated
live-scoring gate. Its byte-frozen manifest is `35,400` bytes with SHA-256
`f0df9e7cd1dab282bec73a75717af150ecf34b3cd04567a2bef300b38a39df42`;
the corpus has 20 artifacts, including 5 images, totaling `17,914,515` bytes
with `8,299,885` bytes of headroom under the 25 MiB gate. The pinned full suite
now passes `546` tests; the generator byte-identity check and `compileall` pass.
Committed runner checkpoint `fb23d1e` adds the guarded live evidence path. Its
offline fake/evidence tests and direct preflight passed without a provider/API
call.

The runner's live entrypoint is non-injectable; fake dependencies enter only a
separately labeled simulated path that cannot pass the live gate. Its immutable
plan is exactly 13 zero-retry calls: one clean-slide smoke, then all six
dispatches in run A and all six independently dispatched entries in run B.
Phase 1 nevertheless remains NO-GO solely pending the caller's exact region and
`base_url`, those 13 live calls and two passing full runs, and the final
clean-profile/GO-decision update. Local user screenshots under `docs/` remain
untracked, non-redistributable supplemental material and are not gate evidence.

Pushed packaging hotfix `3414f47` renamed the legitimate credential resolver so
the existing secret filename-ignore rules no longer exclude that source module;
the rules themselves remain intact. Its clean Git-archive build produced a
`50,094`-byte wheel and passed an isolated resolver round-trip without a
network call. The active library still has no local OCR path, API-key pool,
retry/model-fallback policy, resume support, PDF, audio, or video support. Read
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
