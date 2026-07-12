# Phase 2 Worker Event Contract Checkpoint

Date: 2026-07-11.

Status: all six v1alpha1 event shapes frozen; Phase 2 remains active and not
yet GO.

## Architecture Correction

The prior target prose gave both `ResultEvent` and its nested recognition result
their own `protocol_version` and `request_id`. Repeating the same identity in
two places creates a divergence state with no useful semantics. This checkpoint
keeps version and request identity only in the event envelope.

The nested `WorkerRecognitionResult` contains only result data. It is distinct
from the proven direct-Python `ocrllm.RecognitionResult`; an explicit adapter
connects them. This avoids silently changing Phase 1 caller fields while the
worker is still experimental.

## Frozen Events

`tests/fixtures/worker/v1alpha1_events.jsonl` contains exactly one record for
each allowed event:

```text
capabilities
accepted
progress
warning
result
error
```

Each event is an immutable, slotted dataclass. All use the exact
`ocrllm.v1alpha1` envelope. Non-null request IDs are canonical lowercase UUIDs.
Serialization accepts exact DTO types and returns fresh JSON dict/list values.

## Result Boundary

`WorkerRecognitionResult` owns Markdown, canonical source type, profile,
complete/partial status, nullable output file URI, typed artifacts, hotwords,
warnings, and recursively frozen metadata.

`build_worker_recognition_result()` adapts only the exact direct-Python result:

- Markdown, media/profile/status, hotwords, warnings, and metadata are
  preserved.
- A requested output path must exist and becomes an absolute `file:` URI.
- Direct-Python `assets` are rejected when nonempty because they do not carry
  the artifact kind and MIME type required by the wire contract. The adapter
  does not invent that metadata.

`Artifact` requires a nonempty kind, absolute local file URI, and MIME-shaped
media type. Later processors must supply actual typed artifacts and prove they
exist before result construction.

## Other Event Invariants

- Progress counters are nonnegative integers; booleans are rejected; a known
  total cannot be below completed work.
- Capability status uses exactly `available`, `experimental`, `unavailable`, or
  `deferred`.
- Warning codes are stable uppercase identifiers.
- Error codes reuse the library's stable error-code registry and retryability
  validation.
- Warning and error detail mappings reuse the existing recursive sensitive-key
  redaction. Nested API-key/authorization sentinels serialize only as
  `[REDACTED]`.
- Result and detail metadata are copied and recursively frozen; later caller
  mutation cannot change emitted state.

## Files

```text
src/ocrllm/contracts/artifact.py
src/ocrllm/contracts/worker_recognition_result.py
src/ocrllm/contracts/build_worker_recognition_result.py
src/ocrllm/contracts/capability_report.py
src/ocrllm/contracts/capabilities_event.py
src/ocrllm/contracts/accepted_event.py
src/ocrllm/contracts/progress_event.py
src/ocrllm/contracts/warning_event.py
src/ocrllm/contracts/result_event.py
src/ocrllm/contracts/error_event.py
src/ocrllm/contracts/worker_event.py
src/ocrllm/contracts/serialize_worker_event.py
src/ocrllm/contracts/validate_nonempty_text.py
tests/fixtures/worker/v1alpha1_events.jsonl
tests/test_worker_event_contract.py
```

## Verification

- Command plus event contract tests: `51 passed`.
- Full isolated repository suite: `763 passed`.
- Phase 1 generated fixtures: byte-identical.
- `compileall`: passed.
- Ruff across `src` and `tests`: passed.
- `git diff --check`: passed.

## Next Slice

Implement `write_jsonl_event.py` as the sole stdout protocol writer and
`read_jsonl_command.py` as a bounded stdin-line reader over the already pure
parser. Tests must prove UTF-8, newline escaping, one record per line, flush
behavior, stdout isolation, invalid-command error construction, and size/EOF
handling before the child process/control loop is added.
