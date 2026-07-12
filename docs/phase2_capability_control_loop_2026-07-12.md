# Phase 2 Capability Registry And Control Loop Checkpoint

Date: 2026-07-12.

Status: atomic capability registry and injected-manager control loop implemented;
Phase 2 remains active and not yet GO.

## Public Capability Registry

`get_capabilities(config=None)` now returns all 19 authoritative atomic registry
names in fixed order. It performs no network call and imports no Pillow,
PDFium, OpenAI, HTTPX, or socket stack.

Status is evidence- and configuration-sensitive:

- With no config, the proven PNG/JPEG board gates are `available`; built-in
  DashScope vision is `unavailable` because region/endpoint settings cannot be
  inferred safely from an environment key.
- With an explicit exact pinned Beijing v17 configuration, the image formats
  and DashScope vision provider are `available`.
- A valid DashScope workflow that differs from v17 is `experimental` rather
  than being promoted by installed code alone.
- An injected provider is `experimental` for image recognition and does not
  claim the DashScope provider identity.
- An explicit providerless config is `unavailable`.
- `worker.jsonl.v1alpha1` is `experimental` while its process, cancellation,
  Node, and live gates remain.
- Phase 3/4/5 capabilities are `deferred`, with the responsible phase in each
  reason.

The query freshly snapshots and validates an exact `Config`. Mutated nested
DashScope settings and `Config` subclasses fail closed. API keys never enter
reports or reasons. `CapabilityReport` and `get_capabilities` are now public
root exports.

## Control Loop Boundary

`run_worker_control_loop.py` owns command framing and event serialization. A
`WorkerJobManager` protocol owns nonblocking recognition state:

```text
start(recognize, emit) -> return promptly or raise typed error
cancel(cancel, emit)   -> cancel matching job or raise typed error
close()                -> release/terminate active work at EOF
```

This boundary allows the main loop to keep reading `capabilities` and `cancel`
while a later process manager runs recognition.

The control loop:

- recovers after invalid records;
- answers `capabilities` from the zero-argument registry;
- delegates recognize/cancel commands without blocking by contract;
- attaches a canonical command request ID to manager-raised typed errors;
- serializes main-thread and asynchronous manager events under one output lock;
- maps unexpected manager failures to secret-safe `WORKER_INTERNAL` stdout
  events while forwarding the original exception only to an injected
  off-protocol reporter;
- always calls `close()` at EOF or failure;
- does not hide a `close()` failure.

`WORKER_INTERNAL` is now a stable non-retryable public error code. Raw internal
exception text never enters protocol stdout.

## Real Subprocess Fixture

`tests/worker_fixture_entrypoint.py` launches the same control loop with a
deterministic test-only manager. It is not a public provider or production
worker entrypoint.

The subprocess proof launches Python with an argument list and no shell. Over
real OS stdin/stdout pipes it verifies:

- recovery after invalid JSON;
- all 19 capability reports;
- accepted/result event order;
- JSON-only stdout and empty stderr;
- percent-encoded Chinese, emoji, spaces, and a long Windows-style path;
- v1alpha1 fallback error version and recoverable request ID for an unsupported
  protocol.

Concurrent in-memory proof uses deliberately partial three-byte writes while a
manager thread emits progress and the main loop emits capabilities. All 20
records remain independently valid JSON lines.

## Verification

- Capability/control/command/event/I/O/error focused tests: `100 passed`.
- Full isolated repository suite: `794 passed`.
- Phase 1 generated fixtures: byte-identical.
- `compileall`: passed.
- Ruff across `src` and `tests`: passed.
- `git diff --check`: passed.

The first clean-wheel proof of feature commit `b3dd0cd` passed build, install,
functionality, and heavy-module guards but failed the established import budget:
Python 3.10 median wall/CPU were about 105.22/101.56 ms. Root-exporting one
`CapabilityReport` had executed the eager `ocrllm.contracts` initializer and
loaded the entire command/event graph.

A lazy contracts barrel reduced import time but was rejected before commit:
Python automatically placed lowercase submodule objects such as
`parse_worker_command` on the package, overwriting same-named lazy function
exports. Twenty-six command tests failed with `module object is not callable`.

The accepted fix gives the public `CapabilityReport` its own lightweight root
file and makes `ocrllm.contracts.capability_report` re-export that exact class.
The explicitly imported contracts barrel remains eager and stable; plain root
import never initializes it. All 794 tests pass again. A 32-process source-tree
probe reports about 31.60 ms median wall, 31.25 ms median CPU, and zero loaded
contract submodules. A clean committed-wheel timing proof remains required
after this checkpoint is committed.

## Next Slice

Implement the real isolated recognition job manager. It must start one child
process, emit `accepted` before work, bridge only typed events, reject a second
job with `WORKER_BUSY`, cancel only the matching UUID, and terminate the child
plus descendants within five seconds on Windows and POSIX. Prove all of that
with a deterministic child fixture before adding the production
`python -m ocrllm.worker` entrypoint or a live DashScope smoke.
