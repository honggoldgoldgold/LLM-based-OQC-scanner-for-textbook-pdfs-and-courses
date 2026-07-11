# Phase 1 V16 Arrow Exclusion And Formula Dialect Record

Date: 2026-07-11.

Status: offline gates pass; the complete live gate finished with one of two
full runs passing.

## Decision

V15 completed all 52 calls with zero scout abstentions and proved that the
thinking-enabled Qwen3.7 scout workflow can safely restore missing handwriting
content. Each full run then failed one different local policy boundary. V16
changes only those two boundaries and retains one unified board workflow.

## Auxiliary Arrow Exclusion

Run A handwriting already contained both genuine pluses and all text, but
scout quorum restored a diagrammatic `←` before `RG`. Directional arrows in
board images are inherently ambiguous between text and diagram geometry.

V16 narrows the auxiliary restorable set to arithmetic and relation signs:

```text
+ - = <= >= ≤ ≥
```

The primary model may still transcribe visible arrows as part of its complete
source-grounded output. Only auxiliary insertion is prohibited. The scout
prompt explicitly says never to report directional or diagram arrows, and the
extractor independently discards an arrow record even if the model violates
that instruction. An arrow-only response has no supported row and abstains.

## Formula Dialect V7

Run B formula used `\mathrm{P}`, `\mathrm{A}`, `\mathrm{B}`,
`\mathrm{M}`, and `\mathrm{E}`. Each group contained exactly one ASCII letter
and was source-equivalent, but formula dialect v6 rejected the `\mathrm`
command.

`normalize_recognized_markdown_v7.py` runs the complete v6 normalizer first,
then unwraps only exact `\mathrm{X}` where `X` is one ASCII letter inside an
exact labeled `F01`-to-`F99` formula with one complete dollar wrapper. It does
not alter prose or unlabeled content. Empty, numeric, multi-letter, spaced,
nested-command, malformed, or unwrapped `\mathrm` remains visible to the
strict parser and is rejected.

The preserved v15 `\mathrm` formula shape passes end-to-end scoring under
dialect v7. Existing one-letter `\text{X}` normalization remains active.

## Frozen V16 Contract

- Prompt: `board.v16` with arithmetic/relation-only scout allowlist.
- Primary: one `qwen3.7-plus-2026-05-26`, thinking enabled.
- Scouts: three independent `qwen3.7-plus-2026-05-26`, thinking enabled,
  two-of-three quorum, no auxiliary arrows.
- Formula scorer: `labeled-latex-restricted.v7`.
- Timeout: 180 seconds per provider call.
- Plan: 13 recognitions and exactly 52 Beijing calls; no retry.
- Evidence schema: `ocrllm.phase1-quality-evidence.v16`.
- Manifest: 37,864 bytes, SHA-256
  `12b5234850d885926ea01161c31643ae2050728bd377c86e44784377d00abde9`.
- Focused regression/workflow suite: 99 passed without warnings.
- Exact isolated repository suite: 706 passed.
- Generated fixtures are byte-identical; compileall, Ruff, diff, and conflict
  checks pass.

## Complete Live Result

The frozen v16 run completed all 13 recognitions and 52 calls in about 66
minutes 17 seconds. Run B passed all six dispatches. Run A failed only the
original handwriting omission at 29/30 recall and 5/6 critical signs; all three
scouts yielded supported evidence but no second-plus quorum, so zero signs were
restored. Both v15 policy failures are gone: no arrow is inserted and both
formula runs pass dialect v7. Preserve the 103,882-byte evidence SHA-256
`4395c84ed0efa8d3567bdf5f14a35a8dad8d3412a52fdb5a9e8359ca355ea139`.
See `phase1_live_quality_result_v16_2026-07-11.md`.

Phase 1 remains NO-GO pending a safe generic small-sign availability
improvement, a fresh complete passing gate, and clean package profiles.
