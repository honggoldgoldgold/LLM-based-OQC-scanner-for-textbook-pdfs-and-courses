# Phase 1 V16 Arrow Exclusion And Formula Dialect Record

Date: 2026-07-11.

Status: offline gates pass; complete live gate pending.

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

No v16 provider call has been made. Phase 1 remains NO-GO pending a fresh
complete gate with two passing full runs and clean package profiles.
