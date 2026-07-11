# Phase 1 V13 Live Quality Result

Date: 2026-07-11.

Status: complete provider execution; quality gate failed.

## Bound Contract

- Commit: `74d155efbe786f27016df8529d290e18ca1d9ce6`
- Region: `cn-beijing`
- Prompt: `board.v13`
- Primary: one `qwen3.7-plus-2026-05-26`, thinking enabled
- Scouts: three `qwen-vl-max`, thinking disabled
- Plan: 13 recognitions and exactly 52 provider calls; no retry
- Manifest: 37,853 bytes, SHA-256
  `890f67941bc2783bc81f91ab42b1290fb4ad1df4c722cb2f458e762dd9ad1522`

The run completed all 13 recognitions and reported all 52 calls. Both full runs
completed, neither passed, and there was no terminal provider or runner
failure. Preserve
`evidence/phase1/phase1-quality-v13-2026-07-11-cn-beijing.json`: 98,101 bytes,
SHA-256
`b10b88eeeba94f637165ddf32b95eb3ff3e3e02d4ccdd254ad9fbfe39bec67f1`.

## Run A

- Clean slide passed: zero restorations, zero abstentions.
- Projected slide passed: zero restorations, one abstention.
- Handwriting had 30/30 recall, 38/40 precision, 6/6 critical signs, and 10/10
  slots. One sign was restored with zero abstentions, but an extra `+` was
  inserted between source lines `- Selection` and `- Screening`, causing
  `text_unexpected_critical_units`.
- Formula passed: zero restorations, three abstentions.
- Table scoring was rejected. Five signs were inserted between valid GFM pipe
  rows, leaving pipe syntax outside a table. There were zero abstentions.
- Ordered slide plus formula passed: zero restorations, three abstentions.

## Run B

- Clean slide passed: zero restorations, zero abstentions.
- Projected slide had 312/312 recall, 312/313 precision, and 31/31 critical
  accuracy. The primary already represented source `≥` as `\ge` in LaTeX, but
  one scout `≥` was inserted again after the output section. One scout
  abstained; the duplicate caused `text_unexpected_critical_units`.
- Handwriting had 30/30 recall, 35/36 precision, 6/6 critical signs, and 10/10
  slots. One sign was restored and one scout abstained, but the same extra `+`
  appeared between `- Selection` and `- Screening`.
- Formula passed: zero restorations, three abstentions.
- Table repeated Run A exactly: five row-interleaved restorations, zero
  abstentions, and scorer rejection for broken table structure.
- Ordered slide plus formula passed: zero restorations, three abstentions.

## Diagnosis

V13 solved the v12 protocol abort and recovered complete handwriting content.
The remaining failures are deterministic merger-policy defects:

1. Conflict detection excludes the anchor lines themselves. A source minus
   written on the `Selection` anchor line therefore does not block a disagreeing
   plus proposed between `Selection` and `Screening`.
2. Global representation counting treats Unicode `≥` and LaTeX `\ge` as
   different signs, so an already represented source sign can be duplicated.
3. The merger has no protected-structure rule for a GFM table and can insert
   standalone lines between its rows.

V14 should fix those three local rules without changing provider count, prompt
model, fixture truth, profile routing, or scorer thresholds. Handwriting and all
other images remain one board workflow.

Phase 1 remains NO-GO.
