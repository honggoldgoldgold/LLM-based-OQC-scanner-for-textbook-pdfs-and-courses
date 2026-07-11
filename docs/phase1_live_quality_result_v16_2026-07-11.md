# Phase 1 V16 Live Quality Result

Date: 2026-07-11.

Status: complete provider execution; one of two full runs passed.

## Bound Contract

- Commit: `73da9925521a6c72ab93c143cd48f504330d90ae`
- Region: `cn-beijing`
- Prompt: `board.v16`
- Primary: one `qwen3.7-plus-2026-05-26`, thinking enabled
- Scouts: three independent `qwen3.7-plus-2026-05-26`, thinking enabled
- Plan: 13 recognitions and exactly 52 provider calls; no retry
- Formula dialect: `labeled-latex-restricted.v7`
- Manifest: 37,864 bytes, SHA-256
  `12b5234850d885926ea01161c31643ae2050728bd377c86e44784377d00abde9`

The run started at `2026-07-11T22:07:28.804143Z` and finished at
`2026-07-11T23:13:46.344163Z`, about 66 minutes 17 seconds. All 13
recognitions and 52 calls completed with no terminal failure and no retry.

Preserve
`evidence/phase1/phase1-quality-v16-2026-07-11-cn-beijing.json`: 103,882
bytes, SHA-256
`4395c84ed0efa8d3567bdf5f14a35a8dad8d3412a52fdb5a9e8359ca355ea139`.
Both full runs completed; Run B passed and Run A did not.

## Run A

- Clean slide, projected slide, formula, table, and ordered slide-plus-formula
  all passed with zero restorations and zero abstentions.
- Handwriting failed only `text_critical_accuracy_below_one`: 29/30 recall,
  35/36 precision, 5/6 critical signs, and 10/10 critical slots. All three
  scout responses yielded supported records, but they did not form a quorum
  representing a second plus. Zero signs were restored.
- No directional arrow was inserted. Formula dialect v7 passed.

## Run B

All six dispatches passed with zero restorations and zero abstentions. The
handwriting primary preserved both pluses without auxiliary change. Formula
dialect v7 passed, as did both structural and ordered checks.

## What V16 Proved

Both v15 failures are fixed:

1. Directional-arrow exclusion prevents diagram geometry from entering the
   transcript through the auxiliary channel.
2. Restricted one-letter `\mathrm{X}` normalization passes live formulas while
   the broader LaTeX gate remains strict.

The remaining failure is the original stochastic small-plus omission. It is no
longer caused by parser abstention, false insertion, formula policy, table
structure, or handwriting-specific routing. Three supported scout responses
can still agree on only one of two source plus occurrences.

Before increasing the fixed pool and raising the 52-call cost, the next bounded
experiment should compare primary-conditioned Qwen3.7 omission ledgers against
a larger independent pool on the preserved missing-plus transcript. Any accepted
design must remain generic across image classes and keep at least two-scout
agreement.

Phase 1 remains NO-GO.
