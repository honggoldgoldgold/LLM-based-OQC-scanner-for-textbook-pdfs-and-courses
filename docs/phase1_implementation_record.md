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

The post-v5 investigation is fully recorded in
`phase1_v6_review_workflow_debug_2026-07-11.md`. Twenty-eight targeted calls
tested hatch exclusion, broad/focused details, explicit glyph counting, four
seeds, and three review-framing variants. Crops were inconsistent and added
duplication risk. Every explicit seed reproducibly missed the center `+`.
Prompt-only single pass remained stochastic.

Three readable draft-to-review trials passed, including one repair of a failing
draft. JSON-string framing failed twice because it obscured line comparison.
Line-by-line blockquote framing kept hostile-looking draft lines as data and
passed both actual production probes. The resulting `board.v6` adds immutable
`RecognitionPreferences(review_passes=0|1)`, defaults review off, calls the same
provider/model once more only when explicitly enabled, returns/writes only the
review, and reports both review and provider-call counts. Review failure never
falls back to the draft.

V6 pins one review pass for evidence: 13 recognition invocations, 26 confirmed
provider calls, evidence schema v6. The 37,685-byte manifest SHA-256 is
`c058a68b4a17d1ed13c74bd31429269fc4287539afeb23e20c8dfb0be6f50a27`.
The isolated suite passes 599 tests; fixture generation, compilation, Ruff, and
diff checks pass. Fresh repeated live v6 evidence remains required.

The complete v6 gate ran from clean full commit
`ef63a432ed8c5af61eb164ed754a2d2c1f9dda66`. All 13 recognitions and 26
provider calls returned; both runs completed and run A passed. Handwriting
passed twice, proving the quoted review closes both the missing-plus and hatch-
digit failures. Run B failed only F04 after review changed lowercase `s_4` to
uppercase `S_4`; formula signature was 11/12, atom precision 132/133, and all
108 critical atoms were correct. The 97,150-byte evidence SHA-256 is
`bc256bfbdc73f7d5f80806eb95767d4e68f17cb512f76c9e6daaba5278504707`.
V7 must preserve exact draft identifiers/case unless pixels clearly contradict
them while retaining omission/hallucination repair.

V7 conservative single-draft review was tested and rejected: two handwriting
finals still missed the center `+`, while two formula finals still mutated
`s_4` to `S_4`. V8 instead produces two independent drafts under the identical
unified board prompt and asks one final call to preserve exact agreement and
resolve disagreements against source pixels. The targeted handwriting and
formula consensus finals both pass their complete hard gates. There is no
fixture-class branch.

The public preference now supports an explicit
`RecognitionPreferences(draft_candidates=2, review_passes=1)` robustness mode.
Default `(1, 0)` remains a single provider call. V8 success metadata records
the two preference values and exact call count; failure metadata distinguishes
draft 2 from consensus review. Only the final consensus can be returned or
atomically published. The v8 manifest is 37,712 bytes, SHA-256
`7200d16ea44b365301ce491bd3353433520d6c8ba2cc686debe6562173623e35`.
The full isolated suite passes 608 tests. See
`phase1_v8_consensus_workflow_debug_2026-07-11.md`; complete 39-call evidence is
still required.

V8 live attempt 1 ran from clean pushed commit `04a7c9f`. Smoke and five Run A
single fixtures completed; formula consensus passed 12/12 signatures and
133/133 atoms, but handwriting again omitted one standalone `+` at 29/30 recall
and 5/6 critical-token accuracy. Run A's ordered request then timed out on its
first draft after 120.954 seconds, so it was not scored and Run B never started.
The 59,675-byte evidence SHA-256 is
`fd34fb9f3ec7d37674ba7f779f3db743a36b76af81371a27090e8c1b7d75fe94`.
Preserve it; do not retry the failed dispatch. The next generic workflow must
adjudicate one-sided sign disagreements explicitly rather than rewriting whole
drafts without a difference checklist.

V9 difference-checklist review is rejected. It repaired one handwriting trial
but changed `s_4` to `S_4` even when both formula drafts were byte-identical and
perfect; a second handwriting trial omitted the plus in every Qwen3.7 draft.
Qwen3.7 Max repeated the omission. Two independent legacy-default
`qwen-vl-max` calls consistently captured both plus signs but remained weaker
on exact prose.

V10 therefore makes one Qwen3.7 symbol-audited transcript authoritative for
text and uses two explicit Qwen-VL Max outputs only as untrusted standalone-sign
scouts. A bounded deterministic anchor quorum restored zero signs in an
already-passing handwriting trial, exactly one in a failing trial, and zero in
the perfect formula draft; all three final outputs pass and the formula bytes
are unchanged. The 37,853-byte manifest SHA-256 is
`15a7018084cd1d53c82acbf260bb19095ccb29664cc357beaaaefd9044b8f971`.
The isolated suite passes 628 tests. Full v10 live evidence remains required.

V10 live evidence completed all 13 recognitions and 39 calls. Run B passed all
six dispatches. Run A handwriting still missed one plus because two scouts
produced no usable quorum; Run A formula was provider-complete but rejected by
the scorer for safe `\text{}` LaTeX. Post-run inspection found one ordered
restoration was merely a Markdown `---` separator. Preserve the 98,351-byte
evidence SHA-256
`8c86c7117efa6ad7e999bad3180e861981a27598788cfaaeb526472ae65b9c54`.
V11 needs thematic-break exclusion, a 2-of-3 scout quorum, and a narrow safe
`\text{single-symbol}` normalization.

V11 implements those exact changes. Three independent Qwen-VL Max scouts vote
with a two-of-three anchored quorum; repeated `---`/`===` thematic lines are
not sign events. Formula dialect v6 unwraps only one ASCII letter in
`\text{X}` inside exact labeled math wrappers, while malformed or broader forms
remain rejected. The preserved v10 formula now passes perfectly. The v11
manifest is 37,853 bytes with SHA-256
`3b5c5392b1e10ed40261ac08dc5fbf692f0b451c6c13c4c71a44b710f28ec86b`;
647 isolated tests pass. The live plan is 13 recognitions and 52 calls.

V11 live evidence returned all 52 calls. Formula v6 and every other
non-handwriting dispatch passed twice, but both handwriting runs failed. One
had 30/30 recall but appended invented diagram captions; the other also missed
one plus. Three full-transcript scouts restored zero signs in both. Preserve the
104,026-byte evidence SHA-256
`44b74fdb0ba57662a6c49193c6c203b147b88a723bed8698b983fb9f1a59465f`.
Next test a literal-caption exclusion and strict sign-only scout ledger before
another complete gate.

V12 targeted live proof passes that decision: two Qwen3.7 primaries pass
handwriting without invented captions, and all three Qwen-VL Max scouts return
the same strict ledger for the two plus and two minus occurrences. Production
now rejects any ledger line outside exact `SIGN | BEFORE | AFTER`, plus invalid
signs, thematic breaks, extra prose, fences, and unsafe neighbors. The scout
prompt hash/size enters evidence. The v12 manifest is 37,853 bytes with SHA-256
`e2813e006d4de8db3b4b2fe3ef99a1e658935d98290e2a1735d75d4e80a164f6`;
661 isolated tests pass. The complete v12 gate attempted the first smoke
recognition and four provider calls, then aborted before scoring because the
strict sign protocol had no valid empty-ledger response. No full run began and
no selective retry was made. Preserve the 29,606-byte evidence SHA-256
`ea16775eec1aea7af79681e1f90b76ca075864e9b8e9b1b00dc1c90d125282ea`.
The next version must represent a legitimate zero-event ledger explicitly;
this is not a reason to split handwriting from the board workflow.

V13 adds exact `NONE`, whole-ledger auxiliary abstention, an abstention count in
result metadata, and a conflicting-sign insertion guard. Targeted Beijing
probes pass both sides: three printed-slide scouts return exact `NONE`, while
three handwriting scouts recover `foreign gene + I:V`. A disagreeing later
list sign is blocked because the primary already contains a supported sign at
those anchors. The manifest remains 37,853 bytes with SHA-256
`890f67941bc2783bc81f91ab42b1290fb4ad1df4c722cb2f458e762dd9ad1522`.
The focused suite passes 96 tests and the exact isolated repository suite passes
667 tests.

The complete v13 gate then returned all 52 calls and both full runs, but neither
run passed. Handwriting was complete twice and gained one false plus twice; one
projected slide duplicated LaTeX `\ge` as Unicode `≥`; and both valid tables
were split by five inserted sign lines. Preserve the 98,101-byte evidence
SHA-256
`b10b88eeeba94f637165ddf32b95eb3ff3e3e02d4ccdd254ad9fbfe39bec67f1`.
These are merger-policy defects, not handwriting capability failures.

V14 fixes only those merger defects. Anchor-attached signs now block a
conflicting insertion, source-equivalent Unicode/ASCII/LaTeX relation forms are
counted before restoration, and no insertion may touch a protected outer-pipe
table row. The 37,853-byte manifest SHA-256 is
`dae74f4da207d01e311f5756a204e557ca6e6982073024d2e48b672315febb07`.
The structural suite passes 37 tests, the wider workflow suite passes 153, and
the exact isolated repository suite passes 685. Complete live evidence remains
pending.

The v14 live gate returned all 52 calls. Run B passed all six dispatches; Run A
failed only handwriting at 29/30 recall and 5/6 critical signs because two
scouts abstained and no quorum restoration occurred. Both tables now pass, and
the Unicode/LaTeX and anchor-conflict regressions do not recur. Preserve the
103,074-byte evidence SHA-256
`48c4fb2f78d0bff36aae6e022074d173e85fbf8cdfa792a81bc04bef01fe067a`.
The next experiment is bounded scout availability, not handwriting routing or
single-scout acceptance.

V15 rejects both a larger Qwen-VL pool and one-scout quorum. Twenty-three
targeted Beijing calls show thinking-enabled Qwen3.7 captures both genuine
pluses eight of eight times across the original and final allowlisted prompts;
non-thinking captures the delicate plus only once in five. The final workflow
uses the pinned Qwen3.7 model for one primary and three independent thinking
scouts. Line-level allowlist extraction discards unsupported punctuation before
deduplicating exact per-scout records and applying the unchanged two-of-three
quorum and v14 guards. The 37,864-byte manifest
SHA-256 is
`9c5fe09635142c457c464d52f2c4bba8e78964f61e3c06cb4b786d8bf6bf3c11`;
159 focused and 696 exact isolated tests pass.

The v15 live gate returned all 52 calls after about 67 minutes 27 seconds. All
scout abstention counts are zero, and Run B handwriting passes with one safe
restoration. Run A fails only a scout-restored diagram arrow; Run B fails only
source-equivalent one-letter `\mathrm{X}` outside formula dialect v6. Preserve
the 99,223-byte evidence SHA-256
`65dad6a47206562c526f643bab600d87e0f68987f443cc6757e7f07ec9fff95b`.
Next exclude arrows from the auxiliary channel and add restricted formula
dialect v7; no routing, call-count, retry, or truth change is justified.

V16 excludes all directional arrows from auxiliary insertion while leaving the
complete primary free to transcribe them. Formula dialect v7 narrowly unwraps
only one-letter `\mathrm{X}` inside exact labeled formulas and preserves every
v6 restriction. The preserved v15 formula passes end-to-end scoring; arrow-only
scout evidence abstains. The 37,864-byte manifest SHA-256 is
`12b5234850d885926ea01161c31643ae2050728bd377c86e44784377d00abde9`;
99 focused and 706 exact isolated tests pass. Complete live v16 evidence is
pending.
