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
| `7df3514` | Beijing provider policy and the pre-live implementation ledger recorded. |
| `cf4be8b` | Failed Beijing live evidence and the immutable NO-GO audit recorded. |
| `9dc4e7a` | Versioned `board.v2` prompt and fail-closed presentation normalizer implemented. |
| `2d5a693` | Exact v2 package, import, and optional-profile proof recorded. |

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

- Pinned suite: `574 passed` after the offline `board.v3` correction.
- Generated fixture check: byte-identical.
- Compile check: passed.
- Current versioned manifest: 35,400 bytes; SHA-256
  `43c548fdfda1d114b6851def2ce05284cc213bd3478e1e0eea9faa6242a27966`.
- Corpus: 20 artifacts, including 5 images, totaling 17,914,515 bytes.
- Clean wheel from `9dc4e7a`: 52,602 bytes; SHA-256
  `8ce3a51f2367bdfa3255f8ca23f1b95fd46176e728edec3ef4369da1c626f385`.
- Its isolated no-deps target is 237,251 bytes, has zero base runtime
  requirements and no native payload, and leaves Pillow, PDFium, OpenAI, and
  HTTPX unloaded.
- Python 3.10 fresh-import wall median/p95/max is
  `40.1895/68.8959/105.353` ms and CPU is `31.25/62.5/93.75` ms. Python 3.13
  wall is `34.7108/40.7423/44.7913` ms and CPU is
  `31.25/46.875/46.875` ms. Both pass the Base budgets.
- Image adds 15,918,041 bytes and passes a generated-PNG recognition call.
  Image + DashScope adds 40,837,813 bytes, uses OpenAI 2.45.0, and constructs
  and closes the real client with Beijing settings without HTTP. Both profiles
  pass their size and lazy-import budgets.

### Package Verification Incidents

The user's large backup/move was actively loading `D:` during the proof. Two
bounded combined orchestration attempts timed out after isolated build work;
their workspace-scoped temporary directories were verified and removed. A
later split run found the complete wheel already atomically published and
verified that exact file instead of rebuilding it.

The first valid 30-sample Python 3.10 timing set read directly from the busy
`D:` target and failed (`200.7165/436.1208` ms wall median/p95 and
`171.875/296.875` ms CPU). A first attempt to copy the target to `C:` used
literal-path wildcard semantics, so it did not prove the intended origin and
was discarded. The corrected probe copied the 237,251-byte target, asserted
that `ocrllm.__file__` was inside that GUID-scoped target on every process, and
produced the passing measurements above. No failed or wrong-origin measurement
is used as package-pass evidence.

## First Live Gate Result

The user confirmed the following paid-run configuration on 2026-07-11:

```text
region=cn-beijing
base_url=https://dashscope.aliyuncs.com/compatible-mode/v1
```

The guarded runner completed the fixed plan once from source commit `7df3514`:
13 calls were invoked with zero runner retries, both full runs completed, and
neither full run passed. No provider request failed and no terminal runner
failure occurred. The 73,627-byte evidence file has SHA-256
`cfb2ee423eafecbc87190f9e30d39439f0ea0a865d1a0348a140f67d8088fa23`.

The durable result and diagnosis are in
`phase1_live_quality_result_2026-07-11.md`. The evidence remains immutable and
Phase 1 remains NO-GO. Do not rerun a dispatch or begin another billed set under
the exhausted 13-call confirmation. Offline work may prepare a versioned
prompt/scorer correction; another live plan requires a new explicit decision
and a new evidence path.

## Offline V2 Correction

The post-evidence correction is versioned as `board.v2` and
`labeled-latex-restricted.v2`. The runtime prompt now states the labeled formula
serialization, uses Unicode inline relations, forbids formula tables and
invented labels, and requires exact handwritten spelling and capitalization.

`tests/quality/normalize_recognized_markdown_v2.py` has one responsibility: it
canonicalizes only the observed content-preserving presentation forms before
the existing exact scoring views run. It accepts inline relation math,
missing-colon labeled formulas, strict paired formula tables, common slanted
relation commands, and standalone horizontal rules. Ambiguous wrappers,
arbitrary inline LaTeX, malformed pairs, duplicate labels, and wrong formula
content remain rejected or fail exact scoring.

The pinned full suite passes `568` tests. A diagnostic test applies v2 to the
preserved v1 raw Markdown: the smoke and every non-handwriting dispatch pass,
while both handwriting dispatches retain the original seven failure codes. No
provider call occurred, the v1 evidence was not rewritten, and this does not
authorize another billed run.

The no-network v2 preflight passed at full commit
`2d5a693e53ba3395aa08c530c4dbdea693295097`: 99 relevant files were clean, all
20 artifacts authenticated, the manifest hash and `board.v2`/evidence-v2
contracts matched, the plan contained exactly 13 calls, credential presence was
accepted without printing it, and the proposed evidence path was absent. The
preflight made zero network calls. Because recording this result creates a
later documentation commit, the same preflight must run again from the exact
commit used by any future paid attempt.

## V2 Live Gate Result

The user authorized unrestricted API use and private local testing with the
four screenshots and PDF under `docs/`. The assets remain untracked and are not
treated as redistribution permission.

After a repeated clean preflight at `94d5187`, the fixed v2 gate invoked all 13
calls with zero retries. All provider calls succeeded, both full runs completed,
and neither passed. The 78,235-byte evidence file has SHA-256
`03275cf5922a46dd59fc75e4ab6dc6499e3aeea973190f1d3a6f48b0c556df0b`.
Projected slide, formula board, and calibration table passed in both runs.
Printed and ordered dispatches were rejected only for U+2A7E `⩾`; handwriting
was rejected for line-leading U+2192 diagram arrows. The durable audit is
`phase1_live_quality_result_v2_2026-07-11.md`.

The PowerShell stdin pipeline reported exit code 1 after the runner printed the
evidence hash, although the JSON is complete with no terminal failure. The file
was audited instead of rerunning any call.

## Offline V3 Correction

The v2 evidence remains immutable. `board.v3` and
`labeled-latex-restricted.v3` add only two presentation equivalences: U+2A7E /
U+2A7D relation typography maps to U+2265 / U+2264, and a U+2192 connector is
structural only at the beginning of a line before whitespace. Inline arrows,
wrong relations, and wrong values remain visible failures.

The complete suite passes `574` tests; fixture generation is byte-identical and
`compileall` passes. Diagnostic scoring of the v2 raw output makes the smoke and
every non-handwriting dispatch pass. Both handwriting dispatches retain the
same seven content-quality failures, so v3 does not convert the failed v2 gate
into GO evidence.

## Exploratory Robustness And Provider Audit

`phase1_exploratory_robustness_2026-07-11.md` records 13 post-gate exploratory
network requests, four private screenshot diagnostics, the rejected crop and
thinking variants, both OCR model candidates, the incomplete handwriting
annotation, and the Qwen3.5-OCR signed-URL security incident. No raw private
response or temporary provider credential was committed.

The split recommendation above is superseded by
`phase1_unified_board_handwriting_debug_2026-07-11.md`. High-resolution source
inspection proved the annotation corrected `Enzymens`, omitted
`R-DNA / Replasmid`, over-constrained ambiguous cursive case, and penalized real
faint labels. Crop, legacy-prompt, and 4160-pixel controls did not improve the
core reading; thinking mode captured the one genuinely missing second `+`.

The unified `board.v4` contract pins thinking mode, adds optional source truth
for precision without relaxing required recall, and accepts only line-leading
Unicode/LaTeX diagram connectors as layout. The 37,492-byte manifest SHA-256 is
`b0a38e364ca7e8a2b799548304a219392b5570ab515187ec72d52cd785bfbbb0`.
The isolated offline suite passes 583 tests, fixture generation is
byte-identical, and `compileall` passes. Fresh repeated live v4 evidence is
still required; Phase 1 remains NO-GO.

V4 live attempt 1 started from clean full commit
`a4fc4181e2aa37207224df4de5a2e9c30863d2a8`. Its no-network preflight bound
103 relevant files, 20 artifacts, and the fixed 13-call plan. The first smoke
call returned DashScope HTTP 500 `internal_server_error`; the runner recorded
retryable `PROVIDER_UNAVAILABLE` and aborted with one invocation and zero full
runs. The 27,245-byte atomic evidence SHA-256 is
`49e5a3981d13137c5a8ca543b96290bf3b30595ed5cd6d19ca58362c19134015`.
It is preserved and must not be overwritten or resumed. A new complete attempt
requires a new clean commit and evidence path.

V4 attempt 2 started from clean full commit
`78892445f300128e8a9b252d9483c5608cbaf796`. Seven calls were invoked. Smoke and
all five single fixtures returned; every non-handwriting single passed.
Handwriting reached all 10 critical text slots but scored 29/30 recall, 33/40
precision, and 5/6 critical tokens. It missed the center `+`, while two
line-leading ASCII `->` connectors created four false unexpected critical
tokens. The run-A ordered request timed out and aborted the plan before run B.
The 57,929-byte evidence SHA-256 is
`936edd25c72d3d58f0d70fed4621c603ced023eca572901a8cf773d62635cc6e`.
Preserve it; fix only verified presentation equivalence and continue debugging
the missing operator before another full gate.

The next correction is `board.v5`. It adds the generic region-by-region
verification instruction tested in two targeted built-in-provider calls; it
does not add handwriting routing or fixture-specific prompt text. Both calls
captured the two standalone plus signs and wrote their Markdown through the
library atomic writer under ignored `temp/` paths. V5 also accepts only
line-leading ASCII `->` as layout and adds the source's second `RG` plus `OR` to
optional precision truth. Partial guessed sequences remain unmatched.

Both targeted outputs score 30/30 required recall, 6/6 critical tokens, 10/10
critical slots, and zero unexpected critical tokens under v5. The 37,661-byte
manifest SHA-256 is
`d602d38cbaf6433338d371fbe0d42e8dd4fd3be55811ee428f2333127c0f276d`.
The isolated suite passes 588 tests; fixtures are byte-identical, `compileall`
passes, and changed Python files pass Ruff. Fresh repeated v5 evidence remains
required.

The complete v5 live gate ran from clean full commit
`081dd2d8bb3d9f47f3fa3998476481294c1fa111`. All 13 calls returned and both
full runs completed. Run B passed all six dispatches. Run A passed every
non-handwriting dispatch; handwriting reached 30/30 recall, 38/40 precision,
6/6 critical tokens, and 10/10 slots but hallucinated `111110` from six plasmid
hatch strokes. The hard unexpected-critical gate correctly rejected it. The
95,483-byte evidence SHA-256 is
`0ceb74a7f05ed2ca5cbcac8eb3eb1c340dfac4bf43ceb84e6883cbe4c40e2343`.
Do not add the digits to truth. Test a generic diagram-texture exclusion next.
