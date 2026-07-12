# Phase 2 Worker JSONL I/O Checkpoint

Date: 2026-07-11.

Status: bounded stdin and protocol-only stdout helpers implemented; Phase 2
remains active and not yet GO.

## Reader Contract

`src/ocrllm/worker/read_jsonl_command.py` owns one binary stdin record.

- Clean EOF returns `None`.
- Every non-EOF record must end in `\n` and contain at most 1,048,576 bytes,
  including that newline.
- UTF-8 decoding is strict.
- A record at the exact byte ceiling passes when its JSON payload is valid.
- An oversized or incomplete record fails `COMMAND_INVALID`.
- When an oversized record spans multiple bounded reads, the reader drains only
  that rejected record through its newline. The next command remains readable.
- JSON syntax, duplicate-key, non-finite-number, and command validation remain
  delegated to the previously frozen pure parser.

The worker will pass `sys.stdin.buffer`; text-mode locale decoding is not part
of the protocol boundary.

## Writer Contract

`src/ocrllm/worker/write_jsonl_event.py` owns one binary stdout event.

- It accepts one exact worker event DTO.
- It emits compact UTF-8 JSON with `ensure_ascii=False` and `allow_nan=False`.
- Embedded Markdown newlines are JSON escapes; the only physical newline is the
  record terminator.
- Partial binary writes are completed in a loop.
- A zero/invalid write result fails instead of truncating a record.
- The writer flushes exactly after the complete record has been written.
- It prints no diagnostics. Later control-loop diagnostics belong on stderr.

The worker will pass `sys.stdout.buffer`. Only this writer may own protocol
stdout.

## Error Identity

The command parser now validates and stores a recoverable canonical request UUID
inside typed error details. Unsupported protocol, exact-field, and recognition
configuration failures therefore produce an error event with the request ID.
Malformed/noncanonical IDs yield `request_id=null`.

`build_worker_error_event.py` removes the internal duplicate request-ID detail,
preserves stable code/message/retryability, and preserves recursive sensitive
detail redaction.

The first focused run found that the builder accepted any string detail as a
request ID. A `not-a-uuid` value then failed during event construction. The
builder now performs canonical UUID validation before recovery; all focused
tests pass.

## Verification

- Command, event, and JSONL I/O tests: `66 passed`.
- Full isolated repository suite: `778 passed`.
- Phase 1 generated fixtures: byte-identical.
- `compileall`: passed.
- Ruff across `src` and `tests`: passed.
- `git diff --check`: passed.

## Explicit Non-Goals And Next Slice

No process is spawned yet. There is no `python -m ocrllm.worker`, control loop,
job runner, capability registry response, cancellation, or Node harness.

The next slice should add the deterministic capability registry and a
single-threaded no-job control loop that answers `capabilities`, converts parse
errors to error events, and stops cleanly at EOF. Recognition child-process
isolation and concurrent cancel handling should be added only after that
protocol-only loop passes subprocess tests.
