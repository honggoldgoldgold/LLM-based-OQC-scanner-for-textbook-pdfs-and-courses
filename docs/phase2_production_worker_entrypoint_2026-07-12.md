# Phase 2 Production Worker Entrypoint Checkpoint

Date: 2026-07-12.

Status: `python -m ocrllm.worker` is implemented and verified offline; Phase 2
remains active and not yet GO.

## Composition Boundary

The module entrypoint is intentionally only a launcher. Responsibilities live in
files whose names state their behavior:

```text
src/ocrllm/worker/__main__.py
src/ocrllm/worker/run_production_worker.py
src/ocrllm/worker/report_worker_internal_error.py
```

`__main__.py` calls `multiprocessing.freeze_support()`, binds the standard
streams, and delegates. `run_production_worker()` composes exactly one
`IsolatedWorkerJobManager` with `run_image_recognition_job()` and the existing
control loop. The worker accepts JSONL on stdin, owns JSONL-only stdout, and
runs until EOF. It has no CLI credential argument and no GUI, server, Electron,
PDF, audio, video, local OCR, fallback, or handwriting-specific route.

The alternative of placing composition and diagnostics directly in
`__main__.py` was rejected. A small launcher plus named modules preserves the
repository's filename-as-documentation rule and permits direct testing of stream
composition.

## Diagnostic Boundary

Unexpected control-loop or manager failures are reported only to stderr and
only as the fully qualified exception type. Exception messages are never
written because they may contain provider or path secrets. Expected typed
failures remain terminal JSON error events on stdout.

Child-process diagnostics already obey the same exception-type-only rule.
Provider credentials remain environment-only and are never read while serving a
capabilities command.

## Offline Subprocess Proofs

The real module entrypoint is launched from a directory outside the repository
root with source import configured explicitly:

- A capabilities command succeeds with `DASHSCOPE_API_KEY` removed, emits one
  valid capabilities event with all 19 atomic capabilities, makes no provider
  call, and writes nothing to stderr.
- A recognition command containing Chinese, emoji, and spaces starts the real
  spawned child and unified image adapter. Its deliberately nonexistent source
  emits `accepted`, `recognition 0/1`, then terminal `SOURCE_NOT_FOUND`. Stdin is
  held open until the terminal event, proving the manager does not merely get
  torn down by EOF. No provider call or credential read occurs.
- A secret-bearing unexpected exception proves the diagnostic contains only
  `builtins.RuntimeError`, not its message.

## Verification

- Production module-entrypoint tests: `3 passed`.
- Entrypoint plus worker-manager/adapter/control tests: `29 passed`.
- Full isolated repository suite: `824 passed`.
- Phase 1 generated fixtures: byte-identical.
- `compileall`: passed.
- Ruff across `src` and `tests`: passed.
- `git diff --check`: passed.

The clean committed-wheel proof follows after this checkpoint has immutable
commit bytes.

## Next Slice

Add the shell-free Node integration harness. It must validate every stdout line,
prove Unicode/emoji/space path round trips through Node, and exercise
child-plus-descendant cancellation within five seconds. After that deterministic
gate, run the separately opt-in Beijing live production-worker smoke. Phase 2
remains development-only and not GO until both gates pass.
