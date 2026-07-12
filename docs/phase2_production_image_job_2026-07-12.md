# Phase 2 Production Image Job Checkpoint

Date: 2026-07-12.

Status: the production image-command adapter is implemented; Phase 2 remains
active and not yet GO.

## Unified Recognition Boundary

`run_image_recognition_job()` is deliberately a thin adapter around the proven
public `recognize()` facade. It:

1. converts each validated absolute `file:` URI to a platform path while
   preserving source order;
2. constructs the exact credential-free Beijing DashScope configuration;
3. emits coarse start progress;
4. invokes `recognize()` exactly once for the complete ordered image group;
5. converts the direct result with the frozen worker-result adapter; and
6. emits completion progress followed by one result event.

There is no handwriting detector, handwriting-specific prompt, alternate model,
fallback, or retry. Printed pages, projected boards, handwritten boards,
formulae, tables, and ordered image groups continue through the same
`profile="board"` workflow established by the Phase 1 v17 gate. A quality gap
must be debugged in prompts, workflow, or test material; it does not authorize a
separate handwriting capability.

## Exact Provider Configuration

The adapter accepts the command model and fixes the remaining provider settings:

```text
provider                 dashscope
region                   cn-beijing
base URL                 https://dashscope.aliyuncs.com/compatible-mode/v1
profile                  board
thinking                 enabled
high-resolution images   enabled
sign scout model         qwen3.7-plus-2026-05-26
```

The constructed `Config` contains no API key and configuration construction
does not read `DASHSCOPE_API_KEY`. The existing DashScope provider resolves that
environment variable only inside the isolated recognition child immediately
before a provider call. Secrets therefore do not cross the JSON command,
spawn-argument, or event boundaries.

## File URI Boundary

`file_uri_to_path()` performs no filesystem access. It accepts absolute local
file URIs and Windows UNC file URIs, decodes spaces and Unicode, and rejects:

- non-`file` schemes;
- query strings, fragments, credentials, and ports;
- encoded path separators;
- decoded NUL or backslash ambiguity; and
- relative paths or remote authorities on POSIX.

Existence, image type, decoding, and output collision checks remain owned by the
public facade. The worker adapter does not duplicate those rules.

## Event And Error Behavior

The adapter emits `recognition 0/N` immediately before the facade call and
`recognition N/N` only after it succeeds. It then emits the single frozen result
event. Typed facade errors propagate unchanged to the isolated-child wrapper,
which already owns redaction and conversion to terminal error events. The
adapter does not catch and reinterpret them.

## Files

```text
src/ocrllm/worker/file_uri_to_path.py
src/ocrllm/worker/build_worker_image_config.py
src/ocrllm/worker/run_image_recognition_job.py
tests/test_worker_image_job.py
```

## Verification

- Production image-job tests: `14 passed`.
- Full isolated repository suite: `821 passed`.
- Phase 1 generated fixtures: byte-identical.
- `compileall`: passed.
- Ruff across `src` and `tests`: passed.
- `git diff --check`: passed.

The clean committed-wheel proof is recorded after this checkpoint is committed,
because a Git-archive proof must identify immutable source bytes.

## Next Slice

Add the production `python -m ocrllm.worker` entrypoint around the existing
control loop, isolated manager, and this image job. Then add a shell-free Node
harness, prove every stdout line validates, repeat descendant cancellation
through Node, and run the opt-in Beijing live worker smoke. Until those gates
pass, Phase 2 remains development-only and not GO.
