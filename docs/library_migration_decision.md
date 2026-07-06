# OCRLLM Library Migration Decision

Status: active migration decision.

## What I Found

The existing OCRLLM codebase has useful product behavior, but it is shaped like
an application, not a library:

- The importable package was uppercase `OCRLLM`, while the desired dependency
  surface is lowercase `ocrllm`.
- The old root had no `pyproject.toml`, so downstream projects could not depend
  on it as a normal Python package.
- GUI, FastAPI, social download, CLI, processors, prompts, and core logic shared
  the same package surface.
- Default output and temporary paths were package-relative, which is hostile to
  installed library usage.
- The old architecture plan correctly identified structural rot, but its
  Rust/PyO3 rewrite path was too early for the immediate goal of reuse by other
  projects.

## Decision

Create a new Python-first library package at `src/ocrllm` and move the old app
code under `legacy_app/`.

The new library starts with a narrow, stable facade:

- `ocrllm.Config`
- `ocrllm.RecognitionResult`
- `ocrllm.recognize`
- `ocrllm.recognize_batch`
- public exception types

The first supported vertical slice is board/image recognition through an
injected provider. PDF, audio, video, provider HTTP clients, and Rust internals
are future additions, not part of the first import contract.

## Why This Path

This path creates something another project can safely import now without
inheriting the whole legacy application.

It avoids three failure modes:

- A full rewrite that takes too long before becoming usable.
- Direct downstream imports from legacy internals that freeze bad boundaries.
- Premature Rust/PyO3 packaging complexity before the Python API proves itself.

The old code remains available as a reference implementation and behavior oracle
under `legacy_app/`, but new projects should depend only on `src/ocrllm`.

## Current Repo Shape

```text
START_HERE.md                         One-screen active/legacy/suspended map.
AGENTS.md                             Repo-level boundary instructions.
src/ocrllm/                           New importable library package.
src/ocrllm/README_ACTIVE_LIBRARY.md   Local active-library boundary.
src/ocrllm/AGENTS.md                  Local active-library agent rules.
tests/                                New import-contract tests.
legacy_app/                           Old application code and old tests/docs.
legacy_app/README_LEGACY.md           Local legacy-app boundary.
legacy_app/AGENTS.md                  Local legacy-app agent rules.
docs/legacy_bilibili_social_long_debug_record.md
                                      Legacy Bilibili course runtime record.
Architecture.md                       Suspended future Rust/PyO3 reference.
```

## Done Means

The migration is only useful when these are true:

- `pip install -e .` succeeds.
- `import ocrllm` works from outside the repo root.
- The public API can be tested with fake providers.
- No import of `ocrllm` pulls GUI, FastAPI, social download, or heavyweight
  media dependencies.
- File output is optional; `output_dir=None` keeps results in memory.

## Future Work

1. Add real provider implementations behind the provider interface.
2. Port board preprocessing only after its contract is tested.
3. Add optional dependency groups for image, PDF, audio, and video.
4. Port PDF, audio, and video one vertical slice at a time.
5. Revisit Rust only for measured bottlenecks or modules whose boundaries are
   already stable.
