# Phase 2 Isolated Job Manager Checkpoint

Date: 2026-07-12.

Status: one-job spawned process manager and process-tree cancellation
implemented; Phase 2 remains active and not yet GO.

## Process Boundary

`IsolatedWorkerJobManager` owns at most one spawned child. It implements the
nonblocking `WorkerJobManager` protocol used by the control loop:

- `start()` rejects a second job with `WORKER_BUSY`.
- A child establishes its process-group boundary and signals readiness before
  the parent emits `accepted` and releases it to work.
- A relay thread reconstructs and validates child events, enforces the request
  ID, forbids output after a terminal event, and clears completed state.
- `cancel()` accepts only the matching UUID, terminates the process tree within
  the five-second deadline, waits for relay shutdown, and emits one
  non-retryable `CANCELLED` event.
- A wrong or stale UUID raises `REQUEST_NOT_ACTIVE` without touching the active
  job.
- `close()` terminates active work without emitting after control-stream EOF.
- Unexpected child/relay failures become one secret-safe `WORKER_INTERNAL`
  terminal event. Child stderr reports only the exception type, never its
  message.

Windows uses `taskkill /PID ... /T /F` without a shell. POSIX children create a
new session, then cancellation sends TERM and bounded KILL to that process
group. The child-ready handshake prevents a POSIX cancel race before `setsid()`.

## JSON-Safe Spawn And Pipe Boundary

The first spawned-process test failed all eight cases before child work:
`ImageRecognitionRequest.options` is intentionally a `mappingproxy`, which is
not pickleable under Windows spawn. Event metadata/details have the same
property. Making DTOs mutable or pickle-specific was rejected.

The accepted boundary is canonical JSON-compatible data:

1. Parent serializes the immutable command to dict/list/scalars before spawn.
2. Child strictly reparses it into a fresh immutable command.
3. Child serializes each validated event to compact UTF-8 JSON bytes.
4. The pipe transports at most 64 MiB per event.
5. Parent decodes JSON, strictly reconstructs the event DTO, rechecks its type
   and request ID, then forwards it to the stdout-owning control loop.

`parse_worker_event.py` now round-trips all six frozen event shapes and rejects
unknown versions, fields, event literals, malformed results, artifacts, and
capability reports.

## Deterministic Child Proofs

Pickle-safe top-level fixtures cover:

- accepted, progress, and result from a different PID;
- a typed retryable provider timeout with recursive credential redaction;
- an unexpected exception whose secret-bearing message never reaches events;
- a child attempt to emit another request ID;
- a child returning without a terminal event;
- a blocking child that spawns a real grandchild process.

The cancellation test waits for the grandchild PID file, sends a matching
cancel, requires the manager call to return within five seconds, then proves the
grandchild is gone. A separate `close()` test proves EOF cleanup kills the same
tree without emitting a cancellation event. Test cleanup independently kills a
leftover PID if an assertion fails, so a failed test cannot strand the fixture.

## Files

```text
src/ocrllm/contracts/parse_worker_event.py
src/ocrllm/worker/worker_job_callable.py
src/ocrllm/worker/run_isolated_worker_job.py
src/ocrllm/worker/terminate_process_tree.py
src/ocrllm/worker/isolated_worker_job_manager.py
tests/worker_job_fixtures.py
tests/test_isolated_worker_job_manager.py
```

## Verification

- Event-parser plus isolated-manager tests: `31 passed`.
- Full isolated repository suite: `807 passed`.
- Phase 1 generated fixtures: byte-identical.
- `compileall`: passed.
- Ruff across `src` and `tests`: passed.
- `git diff --check`: passed.

Clean distribution proof for full commit
`41d94ac5ef0ad18f1c8a6380835b6ebc20b7a514` also passes. A Git archive built a
101,271-byte wheel; its isolated no-dependency target contains 466,544 bytes.
Outside the repository, the installed manager imports and an event
serialize/parse round trip passes. Plain root import loads no optional media,
provider, PDF, HTTP, or socket modules; Python 3.10 wall median/p95/max is
33.4714/35.1181/35.4495 ms and CPU median/p95/max is
31.25/46.875/46.875 ms.

## Next Slice

Implement the production image-job callable as a thin adapter from the frozen
worker request to the existing public `recognize()` facade. It must decode
absolute file URIs, construct the explicit Beijing v17 DashScope configuration,
source the key only from `DASHSCOPE_API_KEY`, map progress/result/errors, and
make no alternate provider or handwriting route. Then add
`python -m ocrllm.worker`, the Node harness, and an opt-in live smoke as separate
verified checkpoints.
