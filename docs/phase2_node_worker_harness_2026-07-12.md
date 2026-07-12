# Phase 2 Node Worker Harness Checkpoint

Date: 2026-07-12.

Status: deterministic Node protocol and cancellation gates pass; Phase 2 remains
active and not yet GO because the Beijing live worker smoke remains.

## Shell-Free Process Boundary

The Node harness uses only the Node standard library. It launches Python with
`child_process.spawn(executable, args, {shell: false})`; executable, entrypoint,
and paths are separate array elements. No command string is interpreted by a
shell. Windows helper checks use `spawnSync()` with argument arrays and
`shell: false`.

`WorkerJsonlHarness` owns:

- UTF-8 chunk buffering across arbitrary pipe boundaries;
- rejection of blank or incomplete stdout lines;
- JSON parsing and strict validation of every complete stdout line;
- asynchronous event waiting without blocking Node's event loop;
- stdin close plus bounded worker exit; and
- failure cleanup of the worker process tree.

The independent validator checks the exact fields and value types for all six
event shapes, nested capability reports, results, artifacts, and JSON-valued
details/metadata. It rejects unknown events, fields, protocol versions, and
invalid UUID envelopes. This duplicates the wire boundary intentionally; the
Node consumer does not trust Python merely because Python produced the line.

## Deterministic Scenarios

### Fixture result and path round trip

Node 25.6.1 launches `tests/worker_fixture_entrypoint.py` outside any shell,
sends invalid JSON, capabilities, and recognition, and validates all four
events:

```text
error -> capabilities -> accepted -> result
```

The recognition URI is constructed in Node from a path containing a long
folder name, Chinese, emoji, and spaces. The exact URI survives Node JSON,
stdin, Python DTO parsing, fixture result metadata, stdout, and Node validation.
The scenario completes in about 0.30 seconds on the recorded machine.

### Child-plus-grandchild cancellation

`tests/worker_cancellation_entrypoint.py` composes the real control loop and
isolated manager with the existing blocking fixture. The recognition child
spawns a real grandchild and writes its PID. Node waits until that PID is alive,
sends a matching cancel command, validates `accepted` and terminal `CANCELLED`,
and proves the grandchild PID disappears. The measured complete scenario is
about 3.32 seconds, including process startup and clean EOF exit; the measured
cancel interval itself is also asserted not to exceed five seconds.

Failure cleanup independently kills a surviving worker tree and grandchild so a
failed assertion cannot strand fixture processes.

## Timer-Leak Debug Record

The first focused tests passed their cancellation assertions but took about 33
seconds. Per-scenario timing exposed a 15-second delay after each worker had
already exited. `Promise.race()` had left its losing timeout scheduled, keeping
Node's event loop alive. `withTimeout()` now clears the timer on both resolve and
reject. The accepted rerun completes both focused tests in about 3.88 seconds.

A separate manual timing attempt used relative Python entrypoint paths while the
harness intentionally changed the child working directory; both children timed
out because those relative paths no longer resolved. The actual tests and
accepted timing rerun pass absolute entrypoint paths as required by the
shell-free launch contract.

## Files

```text
tests/node/validate_worker_event.mjs
tests/node/worker_jsonl_harness.mjs
tests/node/verify_worker_protocol.mjs
tests/worker_cancellation_entrypoint.py
tests/test_node_worker_harness.py
```

## Verification

- Focused Node integration tests: `2 passed` in about 3.88 seconds.
- Node syntax checks for all three `.mjs` files: passed.
- Full isolated repository suite: `826 passed`.
- Phase 1 generated fixtures: byte-identical.
- `compileall`: passed.
- Ruff across `src` and `tests`: passed.
- `git diff --check`: passed.

Clean distribution proof for full commit
`480d00aaf4ebe0d0c4b799e4d454191a895943e5` also passes. The two Node tests
rerun from the extracted Git archive, not the working tree, and pass in about
3.82 seconds. The archive builds a 106,058-byte wheel with SHA-256
`30f2258a4b52b49ddc526c9b231aa9eb3fd9de7809bb2b5ac8bdde6a433a9cfc`;
its isolated no-dependency target contains 485,285 bytes. Plain root import
loads no optional media, provider, PDF, HTTP, or socket modules. Python 3.10
root-import wall median/p95/max is 47.3868/52.2511/53.1599 ms and CPU
median/p95/max is 46.875/62.5/62.5 ms.

## Next Gate

Commit and clean-build-prove this checkpoint, then run one opt-in live smoke
through the production `python -m ocrllm.worker` process using the Beijing
DashScope configuration and authorized local screenshot test data. Validate
every stdout line with the same Node harness. Do not declare Phase 2 GO until
that real worker result and its provider-call evidence are recorded.
