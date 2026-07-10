# OCRLLM Migration Status

This file is the project memory aid. Read it before changing the repo.

## One-Sentence Summary

The old OCRLLM app has been moved to `legacy_app/`; the active project is now a
new importable Python library in `src/ocrllm`, currently at the contract-honesty
gate before real image support.

## First Files To Read

Use these files to avoid confusing new work, old app code, and suspended future
planning:

```text
START_HERE.md                         One-screen repo map.
README.md                             Short public overview.
src/ocrllm/README_ACTIVE_LIBRARY.md   Active package boundary.
src/ocrllm/AGENTS.md                  Active package editing rules.
docs/ocrllm_library_go_no_go.md       Authoritative execution decision, file
                                      responsibilities, and phase GO gates.
docs/library_migration_decision.md    Foundational library-making rationale.
legacy_app/README_LEGACY.md           Legacy app boundary.
legacy_app/AGENTS.md                  Legacy app editing rules.
docs/ocrllm_module_target_design.md   Target-state module design map.
docs/legacy_bilibili_social_long_debug_record.md
                                      Legacy Bilibili course robustness record.
docs/legacy_youtube_playlist_social_long_workflow.md
                                      Legacy YouTube playlist course workflow.
docs/legacy_filetrans_codex_debug_record.md
                                      Legacy Filetrans/Codex runtime record.
Architecture.md                       Suspended future architecture reference.
```

## Why This Happened

The previous codebase had useful features, but it was not a clean dependency for
other projects:

- It imported as uppercase `OCRLLM`, while the desired package is lowercase
  `ocrllm`.
- It mixed GUI, CLI, FastAPI, social downloaders, processors, prompts, and core
  logic in one package surface.
- It had no root `pyproject.toml`.
- It defaulted output/temp paths into the package directory.
- It exposed implementation classes before there was a stable library facade.

The active decision is to make a small Python-first library and migrate proven
behavior one vertical slice at a time. Implementations are rewritten behind the
new contract; legacy classes and files are not ported. Exact rules are in
`docs/ocrllm_library_go_no_go.md`.

## What Is Current

Use this:

```text
src/ocrllm/
```

Do not build new integrations on this:

```text
legacy_app/OCRLLM/
```

The current public API is:

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

The current Phase 0 facade route sends board/image paths to an injected
provider:

```python
from ocrllm import Config, recognize


class Provider:
    def recognize_images(self, image_paths, *, prompt, config):
        return "# Board\n"


result = recognize("board.png", config=Config(provider=Provider()))
```

No real DashScope, Google, PDF, audio, or video provider has been ported into
the active library yet.

The current injected-provider path is not yet GO because it does not prove
input existence, real image decoding, nonempty provider output, or typed
provider failures. An isolated `qwen-vl-max` trial successfully recognized a
real PNG, which proves that the provider path is approachable; it does not prove
the active adapter because that adapter does not exist yet.

A 2026-07-09 negative runtime probe confirmed both blockers rather than merely
inferring them from source:

```text
nonexistent .png returned success       true
provider called for nonexistent source  1 time
empty provider Markdown returned success true
provider called for empty-output case   1 time
```

Therefore Phase 0 remains NO-GO even though the existing eight root tests pass.

Active PDF policy is decided now even though PDF implementation is not
authorized yet:

- Use PDFium through `pypdfium2`.
- Keep `pypdfium2` behind future `ocrllm[pdf-text]` and
  `ocrllm[pdf-vision]` extras and out of base import. Text-only installs do not
  install Pillow.
- Rewrite PDF rendering and text extraction; do not port PyMuPDF/`fitz` code.
- Start with `pypdfium2>=5.11.0,<5.12` and `Pillow>=10.4,<13`; lock the first CI
  proof to pypdfium2 5.11.0 and Pillow 12.2.0.
- Serialize PDFium calls behind one process-wide lock. Do not port the legacy
  threaded renderer because PDFium is not thread-safe.
- Do not mark PDF supported until the Phase 3 gate in
  `docs/ocrllm_library_go_no_go.md` passes.

Local PDFium feasibility evidence on Windows/Python 3.13:

```text
pypdfium2 5.11.0
PDFium 151.0.7920.0
2-page mixed PDF opened
text page extracted expected content
raster-only page extracted no text
both pages rendered at 1224 x 1584
malformed PDF raised PdfiumError error code 3
wheel size 3,778,234 bytes
installed size 8,306,352 bytes
```

This is a conditional feasibility GO, not active PDF support. Python 3.10,
Unicode, encrypted, hostile, large-document, recognition, cancellation, and
license-notice packaging gates remain.

Local lightweight base-wheel evidence on the recorded Windows reference host:

```text
wheel size                         9,283 bytes
wheel SHA-256                      166ACEC563B88203A7C8D1F616AB5838192D40501DC8837A5AA99B78EF865D0C
isolated no-deps install          26,152 bytes
Python 3.10, 30 fresh processes   wall median/p95 39.768/45.556 ms
                                   CPU median/p95 31.250/46.875 ms
Python 3.13, 30 fresh processes   wall median/p95 26.265/37.334 ms
                                   CPU median/p95 31.250/31.250 ms
plain-import optional modules     PIL, pypdfium2, openai all absent
base runtime requirements         none
native binaries in base wheel     none
```

This passes the current base-profile size/import feasibility budget. It does not
make image recognition GO: no committed licensed quality corpus or scorer exists
yet, and the Phase 0 input/output honesty failures remain. Numeric profile
budgets and objective recognition thresholds are authoritative in
`docs/ocrllm_library_go_no_go.md`.

A later Python 3.10 repeat measured 48.978 ms median with one 155.312 ms maximum
and failed the draft maximum-100-ms rule. A post-build run then measured 70.477
ms wall median/108.311 ms p95, while a separate unchanged-package probe measured
36.382/40.744 ms wall and 31.250/46.875 ms process CPU median/p95. The final gate
uses 30 fresh processes after two warm-ups: wall median <= 100 ms/p95 <= 200 ms
and process-CPU median <= 60 ms/p95 <= 100 ms; maxima remain diagnostic. This
change separates package CPU work from bounded scheduler/antivirus noise rather
than waiving a CPU or percentile failure.

HarmonyOS/ArkTS integration is deferred. It is not an active feature, phase, or
compatibility claim.

## Historical Legacy Social-Long Course Path

The Bilibili/social downloader still lives under `legacy_app/OCRLLM/`. It is a
read-only behavior reference for this migration, not a public `ocrllm` library
API or an active test surface.

Detailed incident history, implementation map, verification commands, and
operational rules are in:

```text
docs/legacy_bilibili_social_long_debug_record.md
```

The recorded multi-part Bilibili command was:

```powershell
$env:PYTHONPATH='legacy_app'
D:\Anaconda\envs\OCRLLM\python.exe -m OCRLLM.cli social_long `
  "https://www.bilibili.com/video/BV1nJ411z7fe?p=33" `
  --parts 1-33 --resume -o output\bilibili_cs231n_full
```

Expected per-part output is exactly two Markdown files:

```text
*_板书识别.md
*_录音识别.md
```

The Bilibili comments and per-part danmaku context is written separately to:

```text
bilibili_social_context.md
```

This legacy path has resume support for existing downloads, completed video
phases, and in-flight DashScope FileTrans task IDs. Keep new downstream
projects importing `ocrllm`; do not expose this legacy processor as a new public
library boundary.

For multi-part YouTube course playlists, the equivalent recorded legacy
workflow is documented here:

```text
docs/legacy_youtube_playlist_social_long_workflow.md
```

The recorded command used the same legacy CLI boundary:

```powershell
$env:PYTHONPATH='legacy_app'
D:\Anaconda\envs\OCRLLM\python.exe -m OCRLLM.cli social_long `
  "https://youtube.com/playlist?list=PLggLP4f-rq02vX0OQQ5vrCxbJrzamYDfx&si=6VZ5fem42kqyyasd" `
  --parts 1-97 --resume -o output\youtube_modern_robotics_full
```

The 2026-07-06 YouTube playlist run is still legacy compatibility work, not a
public `ocrllm` API. It fixed and documents these additional runtime rules:

- YouTube playlist probe results must expose flat entries and route to
  `social_long`, not `social_short`.
- Non-Bilibili yt-dlp downloads must allow playlists and map `--parts` to
  `playlist_items`.
- Codex social-long video recognition caps the effective video frame batch size
  at 1 to avoid incomplete multi-frame markers.
- Video debug temp directory names must be Windows-safe and stable for YouTube
  titles.
- Social-long part output directories must strip trailing spaces/dots after
  legacy truncation, and long per-part artifact stems must shorten before
  Windows path limits are reached.
- Resume skip checks must accept an existing clean board/audio markdown pair
  before changing artifact stems, otherwise completed parts can be duplicated.
- DashScope FileTrans sidecars must be shortened using the resolved absolute
  `.tmp` path length.

The 2026-07-06 Bilibili CS231n run exposed and fixed these legacy runtime
problems:

- Multi-part Bilibili pages must route to `social_long`, not short-video mode.
- Requested part failures must fail the whole selected run instead of returning
  a partial course.
- Bilibili MP4 downloads need reusable `.part` downloads and existing-file
  reuse.
- Shared comments must be fetched once from the course AID; danmaku must be
  fetched per part CID.
- The old XML danmaku endpoint can return Bilibili 412/risk-control HTML, so
  the fallback path uses the segmented protobuf danmaku API.
- Each part is complete only with exactly `*_板书识别.md` and
  `*_录音识别.md`.
- FileTrans task IDs must survive process interruption so resume can continue
  polling instead of resubmitting the same long audio.
- Video resume must trust valid phase artifacts when a checkpoint was not
  marked complete before process exit.
- Social media GUI input must accept free-form text and Markdown-style pasted
  links, not only lines beginning with `http`.

Historical completion evidence recorded for the supervised Bilibili course
run; this is not current active-library evidence:

```text
33 part directories
33 downloaded MP4 files
33 *_板书识别.md files
33 *_录音识别.md files
0 FileTrans task sidecars
bilibili_social_context.md contained github.com/Divsigma/Courses and per-part danmaku
Focused legacy tests: 40 passed
Root active-library tests: 5 passed
```

## Legacy Codex/Filetrans Robustness Status

As of 2026-07-06, Codex video recognition and DashScope Filetrans audio
recognition remain legacy compatibility work in `legacy_app/`, not public
`ocrllm` API.

The July 2026 robustness fixes changed the legacy runtime behavior in these
ways:

- Codex CLI image-recognition subprocesses are launched with Windows
  no-window subprocess flags and closed stdin.
- Codex CLI nonzero exits and empty results are retried once and summarized,
  instead of dumping prompts or CLI diagnostics into board Markdown.
- In Codex mode, Phase 4 batch/per-frame failures are hard failures; they no
  longer create placeholder Markdown that looks complete.
- Codex mode skips the Qwen text hotword extraction step that made a Codex run
  appear to route through Qwen after image recognition.
- Filetrans cost logging uses the cached duration probe instead of the removed
  `_get_duration` method.
- Board-only reruns with `--phases 2 3 4` preserve existing audio transcripts
  instead of invalidating Phase 5 artifacts.

Historical evidence recorded by the 2026-07-06 audit:

```text
40 target course folders scanned
40 folders had exactly the expected board/audio Markdown pair
0 folders had known dirty markers
53 focused legacy regression tests passed
0 active legacy video checkpoints remained
```

Use `docs/legacy_filetrans_codex_debug_record.md` as behavior evidence. Do not
change or rerun this path for an active-library phase gate.

## Active Execution Decision And Target Design

`docs/ocrllm_library_go_no_go.md` is the controlling implementation record. It
defines:

- the current GO and NO-GO boundaries,
- one responsibility for each target file,
- which legacy behaviors to preserve,
- which implementations must be rewritten,
- which legacy areas are rejected or deferred,
- exact phase gates and verification commands.

`docs/ocrllm_module_target_design.md` describes the intended completed Python
library. It is a supporting design map, not the execution queue.

The documents are useful for rebuilding context after memory loss. The
GO/NO-GO record defines allowed boundaries; tests and real downstream imports
provide the evidence for advancing a gate.

## What Is Suspended

`Architecture.md` contains a Rust/PyO3 v3 rewrite plan. That plan is currently
suspended. It is not the implementation path for the next work item.

Rust can come back later only after:

- The Python import contract works.
- At least one real downstream project imports `ocrllm`.
- The module boundary to rewrite is stable.
- Tests can compare behavior against the Python implementation.

HarmonyOS/ArkTS is also deferred. Do not add a native bridge, ArkTS client, or
compatibility claim without a new explicit decision after the active library
and its distribution contracts are stable.

## What Was Moved

The old app package moved from repo root to:

```text
legacy_app/OCRLLM/
```

The old root launcher aliases were removed to avoid confusing the migrated repo
layout with the pre-migration app layout:

```text
start.bat
ocrllmstart.bat
legacy_app/start.bat
```

The preserved historical GUI launcher is:

```text
legacy_app/launch_gui.bat
```

That launcher runs `python -m OCRLLM.main` from `legacy_app/`, not
`python main.py`, because `main.py` lives at `legacy_app/OCRLLM/main.py`.

The old tests/docs/scripts moved to:

```text
legacy_app/tests/
legacy_app/docs/
legacy_app/README.md
legacy_app/requirements.txt
legacy_app/environment.yml
```

## What To Do Next

Current phase: **Phase 0 -- contract honesty**.

Implement only this bounded slice:

1. Add tests proving missing, unreadable, empty, oversized, unsupported, and
   invalid image inputs fail before provider invocation.

2. Reject empty provider output and translate provider failures into typed,
   secret-safe public errors.

3. Make result metadata JSON-safe and make output collision behavior explicit.

   Change the canonical result media type from `board` to `image`; preserve
   `board` only as an image recognition profile before the versioned contract
   freezes.

4. Populate `ocrllm[image]` with `Pillow>=10.4,<13` for lazy decode validation.
   Remove the empty PDF, audio, video, and all extras. Re-add each later feature
   extra only when its phase installs and enables it.

5. Split the public functions and routing according to
   `docs/ocrllm_library_go_no_go.md`; do not create later-phase scaffolding.

6. Run the exact test, temporary-wheel build, clean-target install, outside-repo
   import, and heavy-module guard commands in
   `docs/ocrllm_library_go_no_go.md`. Record the commands and results here.

Phase 1 may begin only after all Phase 0 GO conditions pass. PDF, audio, video,
service, HarmonyOS, Rust, Office, social, GPU, and offline-model work is not the
next task.

## Do Not Do This

- Do not import `legacy_app.OCRLLM` from new downstream projects.
- Do not copy whole legacy files into `src/ocrllm`.
- Do not expose legacy processors as public API.
- Do not freeze a `1.0` API until real downstream usage proves it.
- Do not make the Rust plan active again without a measured reason.
- Do not add PyMuPDF or `fitz` to the active package; Phase 3 uses PDFium through
  `pypdfium2`.
- Do not start a later phase before the current GO gate passes.
- Do not begin or claim HarmonyOS/ArkTS compatibility.
- Do not claim support from code existence, mocks, installed dependencies, or
  historical logs alone.

## Done Criteria For This Migration Step

- `START_HERE.md` gives an immediate visual split between active, legacy, and
  suspended areas.
- Root `README.md` explains the active path.
- `MIGRATION_STATUS.md` explains what changed and what to do next.
- `src/ocrllm/` is clearly marked as the active importable package.
- `Architecture.md` is clearly marked as suspended future planning.
- `legacy_app/` is clearly marked as old app/reference code.
- New tests prove the active import contract.
- `docs/ocrllm_library_go_no_go.md` is the single authoritative execution
  record and all navigation docs point to it.
- PDFium is the only active PDF decision; PyMuPDF is explicitly legacy-only.
- HarmonyOS/ArkTS is explicitly deferred.
