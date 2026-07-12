# Phase 2 Worker Command Contract Checkpoint

Date: 2026-07-11.

Status: first Phase 2 vertical slice implemented; Phase 2 remains active and
not yet GO.

## Scope

This checkpoint freezes the complete `ocrllm.v1alpha1` input-command boundary:

- `capabilities`
- `recognize`
- `cancel`

It does not implement event DTOs, stdin/stdout ownership, the worker control
loop, child-process isolation, cancellation, the Node harness, or a live worker
smoke. Those remain later Phase 2 slices.

The existing direct-Python `RecognitionResult` is deliberately unchanged. The
target wire result has different fields, so merging them while building command
parsing would create a systemic compatibility risk for the proven Phase 1 API.

## New Responsibilities

```text
src/ocrllm/contracts/worker_protocol_version.py
    Own the current and planned protocol version names.

src/ocrllm/contracts/source_descriptor.py
    Own one immutable canonical-media local file URI.

src/ocrllm/contracts/image_recognition_request.py
    Own the immutable v1alpha1 recognize command.

src/ocrllm/contracts/capabilities_command.py
src/ocrllm/contracts/cancel_command.py
    Own the two exact control commands.

src/ocrllm/contracts/parse_jsonl_command.py
    Decode one JSON record; reject duplicate keys and non-finite numbers.

src/ocrllm/contracts/parse_worker_command.py
    Validate the command envelope and construct one exact DTO.

src/ocrllm/contracts/serialize_worker_command.py
    Produce a fresh canonical JSON object from one exact DTO.

src/ocrllm/contracts/freeze_image_recognition_options.py
    Apply the three exact option defaults and freeze the result.

src/ocrllm/contracts/validate_absolute_file_uri.py
src/ocrllm/contracts/validate_language_tag.py
src/ocrllm/contracts/validate_worker_request_id.py
    Own file-URI, BCP-47, and canonical-UUID validation respectively.

src/ocrllm/thaw_json_value.py
    Convert recursively frozen JSON values to fresh serialization values.
```

`ocrllm.contracts` is importable explicitly, but root `import ocrllm` does not
import it. This preserves the lightweight Phase 1 facade while the Phase 2
protocol remains incomplete.

## Frozen Behavior

- Every command uses `ocrllm.v1alpha1` and a lowercase canonical UUID.
- `recognize` requires a nonempty ordered list of image `file:` URIs, exact
  provider `dashscope`, exact profile `board`, nullable nonempty model text, and
  BCP-47 language tags.
- Raw spaces, ASCII controls, backslashes, malformed percent escapes, query
  strings, fragments, and malformed authorities are rejected in file URIs.
  Percent-encoded Chinese, emoji, spaces, long-drive paths, and UNC paths are
  accepted without decoding or reordering them.
- The only option keys are `output_directory_uri`, `overwrite`, and
  `timeout_seconds`. Their defaults are `null`, `false`, and `120`.
- Unknown envelope fields fail `COMMAND_INVALID`; an unsupported version fails
  `PROTOCOL_UNSUPPORTED`; invalid recognition configuration fails
  `CONFIG_INVALID`.
- Duplicate JSON keys, multiple records, top-level arrays, empty input, and
  `NaN` fail `COMMAND_INVALID`.
- Public error messages never echo the rejected protocol, path, option value,
  or credential-shaped sentinel.
- DTOs are frozen. Sources and languages become tuples; options become a
  recursively frozen mapping. Serialization returns fresh dict/list values.

The frozen fixture is
`tests/fixtures/worker/v1alpha1_commands.jsonl`. It contains all three commands
and a recognize path with percent-encoded Chinese, emoji, and spaces.

## Verification

Focused command-contract tests: `33 passed`.

Full isolated repository suite after the new slice: `745 passed`. The Phase 1
fixture generator remained byte-identical and `compileall` passed.

Repository-wide Ruff initially exposed three pre-existing import-ownership
issues: `decode_image.py` re-exported `MAX_IMAGE_PIXELS` only for tests,
`test_validate_source.py` imported an unused group validator, and
`test_import_contract.py` imported an unused `Path`. Tests now import image
limits and DTOs from the files that own them, and the dead imports are removed.
Ruff passes across `src` and `tests`.

## Next Slice

Add the six immutable event DTOs and frozen event JSONL fixtures. Resolve the
wire-result/direct-result difference with an explicit serializer or adapter;
do not mutate the direct Phase 1 return contract implicitly. Only after event
serialization is frozen should `read_jsonl_command.py`,
`write_jsonl_event.py`, and the one-job control loop be implemented.
