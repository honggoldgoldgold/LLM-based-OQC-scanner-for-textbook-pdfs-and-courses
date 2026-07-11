# Phase 1 V17 Conditioned Omission Scout Record

Date: 2026-07-11.

Status: targeted Beijing probe and all offline gates pass; complete live gate
pending.

## Decision

V16 completed all 52 calls, eliminated the v15 arrow and formula failures, and
produced one completely passing full run. Run A still missed one handwriting
plus even though all three independent scout responses were parse-usable. The
unconditioned scouts could agree on only one of two source plus occurrences.

Increasing the pool would raise the already 66-minute, 52-call gate to at least
78 calls without addressing task ambiguity. V17 keeps three scouts and instead
changes their task from full sign inventory to candidate-conditioned omission
detection.

## Targeted Probe

Three independent thinking-enabled Qwen3.7 calls received the exact preserved
v16 Run A handwriting primary as quoted inert data and the original image. Each
call returned exactly:

```text
+ | foreign gene | I:V
```

There was three-of-three agreement on the genuinely omitted plus and no report
for the already represented `Transformation + Validation` plus. The three calls
completed in 273.9 seconds. They are diagnostic evidence, not gate evidence.

## Conditioned Prompt Boundary

`build_board_sign_scout_prompt(candidate_markdown)` now quotes every primary
line with `>` and labels the block inert, fallible data. Scouts must report only
an arithmetic/relation sign visible at a location where the candidate entirely
omits it. Neighbor anchors must be copied from the candidate. Exact `NONE` is
required when no omission exists.

The prompt has version `board-sign-omission.v1`. The quality request contract
records the fixed template SHA-256 and byte count. Each recognition result
records the version, exact dynamic prompt SHA-256, and UTF-8 byte count derived
from its primary transcript. The live validator requires a lowercase 64-digit
hash and a positive exact byte count.

Candidate text remains untrusted. Quoting and instruction boundaries reduce
prompt-injection risk; extraction still retains only exact allowlisted records,
deduplicates per scout, requires two distinct scouts, and applies all v14-v16
structural guards.

## Omission Budget Semantics

Inventory scouts listed every occurrence, so the old merger subtracted the
number of signs already present anywhere in the primary. Omission scouts list
only missing occurrences. A different plus elsewhere must therefore not consume
the missing-plus budget.

V17 treats each arithmetic omission quorum event as one candidate insertion.
Same-location anchor and sign checks still prevent duplicates. Unicode/ASCII/
LaTeX greater-equal and less-equal signs retain the global equivalence budget
to conservatively block duplicate relation rendering. Table protection,
arrow exclusion, safe anchors, event bounds, and two-of-three quorum are
unchanged.

## Frozen V17 Contract

- Primary prompt: `board.v17`.
- Scout prompt: `board-sign-omission.v1`, dynamically bound to the primary.
- Primary: one `qwen3.7-plus-2026-05-26`, thinking enabled.
- Scouts: three independent `qwen3.7-plus-2026-05-26`, thinking enabled,
  conditioned omission ledgers, two-of-three quorum.
- Formula scorer: `labeled-latex-restricted.v7`.
- Timeout: 180 seconds per provider call.
- Plan: 13 recognitions and exactly 52 Beijing calls; no retry.
- Evidence schema: `ocrllm.phase1-quality-evidence.v17`.
- Manifest: 37,864 bytes, SHA-256
  `4ec1440f531e88492eb06795a29308256a5718c2748625ce2ad9b1230807e393`.
- Focused workflow suite: 89 passed.
- Exact isolated repository suite: 712 passed.
- Generated fixtures are byte-identical; compileall, Ruff, diff, and conflict
  checks pass.

No v17 gate call has been made. Phase 1 remains NO-GO pending a fresh complete
gate with two passing full runs and clean package profiles.
