# OCRLLM Migration Status

This file is the project memory aid. Read it before changing the repo.

## One-Sentence Summary

The old OCRLLM app has been moved to `legacy_app/`; the active project is now a
new importable Python library in `src/ocrllm`.

## First Files To Read

Use these files to avoid confusing new work, old app code, and suspended future
planning:

```text
START_HERE.md                         One-screen repo map.
README.md                             Short public overview.
src/ocrllm/README_ACTIVE_LIBRARY.md   Active package boundary.
src/ocrllm/AGENTS.md                  Active package editing rules.
legacy_app/README_LEGACY.md           Legacy app boundary.
legacy_app/AGENTS.md                  Legacy app editing rules.
docs/library_migration_decision.md    Library-making decision and rationale.
docs/ocrllm_module_target_design.md   Target-state module design map.
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

The active decision is to make a small Python-first library and port behavior
from legacy code only after the public contract is clear.

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
    ConfigError,
    QuotaExhausted,
    UnsupportedFormat,
    Cancelled,
)
```

The first supported feature is board/image recognition with an injected
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

## Legacy Social-Long Course Path

The Bilibili/social downloader still lives under `legacy_app/OCRLLM/`. It is a
maintained compatibility workflow, not a public `ocrllm` library API.

For multi-part Bilibili courses, the reusable path is:

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

## Target Module Design

`docs/ocrllm_module_target_design.md` describes the intended completed Python
library as if it already exists. It is a design map, not a frozen contract.

The document is useful for rebuilding context after memory loss, but tests and
real downstream imports decide the actual implementation.

## What Is Suspended

`Architecture.md` contains a Rust/PyO3 v3 rewrite plan. That plan is currently
suspended. It is not the implementation path for the next work item.

Rust can come back later only after:

- The Python import contract works.
- At least one real downstream project imports `ocrllm`.
- The module boundary to rewrite is stable.
- Tests can compare behavior against the Python implementation.

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

The maintained GUI launcher is now:

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

1. Verify the new package:

   ```bash
   pip install -e .
   python -c "import ocrllm; print(ocrllm.__version__)"
   pytest
   ```

2. Add a real provider behind the existing injected-provider seam.

3. Port only the minimum board-image preprocessing needed for a tested real
   board flow.

4. Add optional dependency groups when real features need them:

   ```text
   ocrllm[image]
   ocrllm[pdf]
   ocrllm[audio]
   ocrllm[video]
   ocrllm[all]
   ```

5. Add PDF, audio, and video as separate vertical slices.

## Do Not Do This

- Do not import `legacy_app.OCRLLM` from new downstream projects.
- Do not copy whole legacy files into `src/ocrllm`.
- Do not expose legacy processors as public API.
- Do not freeze a `1.0` API until real downstream usage proves it.
- Do not make the Rust plan active again without a measured reason.

## Done Criteria For This Migration Step

- `START_HERE.md` gives an immediate visual split between active, legacy, and
  suspended areas.
- Root `README.md` explains the active path.
- `MIGRATION_STATUS.md` explains what changed and what to do next.
- `src/ocrllm/` is clearly marked as the active importable package.
- `Architecture.md` is clearly marked as suspended future planning.
- `legacy_app/` is clearly marked as old app/reference code.
- New tests prove the active import contract.
