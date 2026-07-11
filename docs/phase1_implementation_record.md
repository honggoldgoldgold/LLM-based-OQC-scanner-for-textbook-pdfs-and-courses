# Phase 1 Implementation Record

Status: recovery ledger for the active board/image slice.

Last updated: 2026-07-11.

This file explains what was built, what parallel review work contributed, how
the evidence writer behaves, and how to resume without reconstructing history
from chat transcripts. The authoritative GO/NO-GO boundary remains
`ocrllm_library_go_no_go.md`.

## Scope Preserved

Phase 1 implements one lightweight Python board/image path and one built-in
DashScope provider. It does not implement local OCR, provider pools, automatic
model switching, durable image resume, PDF, audio, video, GUI, or services.
Those requests remain recorded for later phases rather than being hidden inside
the image adapter.

## Pushed Checkpoints

| Commit | Durable result |
|---|---|
| `5018ad0` | Phase 0 contract-honesty transition. |
| `a6a8b18` | Explicit zero-retry DashScope vision adapter and offline boundaries. |
| `db63918` | Adapter verification and migration evidence. |
| `3414f47` | Credential resolver renamed so secret filename ignores no longer omit legitimate wheel source. |
| `e328253` | Licensed five-class corpus, deterministic generators, exact scorers, and manifest-authenticated gate. |
| `fb23d1e` | Atomic, interruption-aware, fixed 13-call live evidence runner. |
| `72667e5` | Recovery documents reconciled with the evidence-runner checkpoint. |
| `51d3f27` | Clean package proof recorded. |
| `5aaa854` | Missing exact below/at/above input-limit coverage completed. |
| `8fe4847` | Boundary, package, profile, and endpoint-search evidence recorded. |

Use `git show <commit>` for exact patches. New changes must be committed and
pushed in similarly bounded checkpoints.

## Parallel Review And Agent Work

Agent work is evidence only after the main branch tests or records it.

- The corpus/generator workstream assembled the licensed five-class fixture
  set, deterministic image generators, provenance, frozen manifest, and exact
  scorer channels. Independent audits checked hashes, inventory, licensing,
  thresholds, and byte reproduction before commit `e328253`.
- The evidence-runner workstream implemented the fixed smoke + run A + run B
  plan, repository/import identity binding, secret scanning, raw result capture,
  scorer serialization, and failure/interruption tests. A separate contract
  review found no remaining high-severity runner defect before `fb23d1e`.
- The documentation workstream reconciled `START_HERE.md`, `README.md`,
  `MIGRATION_STATUS.md`, and the authoritative decision with the corpus and
  runner checkpoints. A separate read-only audit checked hashes, counts,
  commands, balanced Markdown fences, and NO-GO wording.
- The completion-audit workstream compared the original pasted brief with the
  actual tree. It found missing exact three-point tests for several image caps
  and a stale active-library README. Those findings produced `5aaa854`; the
  pinned suite increased from 546 to 554 passing tests.
- The endpoint-search workstream performed a secret-safe local configuration
  audit. It proved that the current environment key exactly matched the key in
  `HKCU:\Software\OCRLLM\QCR\ui` and recovered the configured Beijing endpoint,
  while correctly refusing to infer a region before user confirmation. The user
  confirmed on 2026-07-11 that Aliyun API workflows always use Beijing.

No agent result authorizes crossing a deferred phase. Git commits, tests,
artifacts, and this record are the recovery authority.

## Atomic Evidence Writer

`tests/quality/write_quality_evidence_atomically.py` owns evidence persistence.
The live runner uses it before and after every paid call.

- Evidence is strict, sorted, indented UTF-8 JSON with a final newline.
- The current credential and full endpoint are scanned recursively before JSON
  serialization and again in JSON-escaped form. A detected secret aborts the
  write instead of producing a partially redacted success claim.
- Each update is written to a temporary file in the evidence directory, then
  flushed and file-`fsync`ed.
- Initial publication uses an exclusive hard link so an existing evidence path
  cannot be overwritten. Later checkpoints use atomic `os.replace`.
- The runner checkpoints the active attempt and incremented invocation count
  before dispatch. After return it records raw Markdown, hashes, metadata,
  elapsed time, and every scorer metric.
- `KeyboardInterrupt` is checkpointed and re-raised. Provider, identity,
  credential, or internal scorer failures abort without another paid call.
- A scored threshold failure remains in the evidence and the immutable plan
  continues; the runner never retries one fixture or chooses the better run.
- The writer file-`fsync`s data but does not explicitly `fsync` the containing
  directory. It promises normal atomic link/replace behavior, not persistence
  through every sudden power-loss scenario.

## Current Verified Offline State

- Pinned suite: `554 passed`.
- Generated fixture check: byte-identical.
- Compile check: passed.
- Frozen manifest: 35,400 bytes; SHA-256
  `f0df9e7cd1dab282bec73a75717af150ecf34b3cd04567a2bef300b38a39df42`.
- Corpus: 20 artifacts, including 5 images, totaling 17,914,515 bytes.
- Clean wheel from `5aaa854`: 51,281 bytes; SHA-256
  `23e0068b4525a437052254d8929f0d7ab7706efd5ff48447d04572c796909d93`.
- Base, Image, and Image + DashScope profiles pass their size and lazy-import
  budgets. The real client construction proof sends no HTTP request.

## Live Gate Resume Point

The user confirmed the following paid-run configuration on 2026-07-11:

```text
region=cn-beijing
base_url=https://dashscope.aliyuncs.com/compatible-mode/v1
```

The next evidence run must use a new path, `--confirm-paid-calls 13`, the pinned
model, zero retries, and a clean relevant Git/import/manifest/artifact preflight.
If it fails, preserve and commit the failed evidence and update the decision as
NO-GO. If both full runs pass, rerun the final package profiles and update all
GO documents together.
