# Phase 1 V14 Live Quality Result

Date: 2026-07-11.

Status: complete provider execution; one of two full runs passed.

## Bound Contract

- Commit: `ff25461b5fec1a53671bc0314788d98d30380d02`
- Region: `cn-beijing`
- Prompt: `board.v14`
- Primary: one `qwen3.7-plus-2026-05-26`, thinking enabled
- Scouts: three `qwen-vl-max`, thinking disabled
- Plan: 13 recognitions and exactly 52 provider calls; no retry
- Manifest: 37,853 bytes, SHA-256
  `dae74f4da207d01e311f5756a204e557ca6e6982073024d2e48b672315febb07`

All 13 recognitions and 52 calls completed with no terminal provider or runner
failure. Preserve
`evidence/phase1/phase1-quality-v14-2026-07-11-cn-beijing.json`: 103,074
bytes, SHA-256
`48c4fb2f78d0bff36aae6e022074d173e85fbf8cdfa792a81bc04bef01fe067a`.
The summary records two completed full runs and one passing full run, so the
Phase 1 gate remains failed.

## Run A

- Clean slide passed: zero restorations, zero abstentions.
- Projected slide passed: zero restorations, two abstentions.
- Handwriting failed only `text_critical_accuracy_below_one`: 29/30 recall,
  35/37 precision, 5/6 critical signs, and 10/10 slots. Two scouts abstained,
  the remaining scout could not form quorum, and zero signs were restored.
- Formula passed: zero restorations, three abstentions.
- Table passed: zero restorations, zero abstentions.
- Ordered slide plus formula passed: zero restorations, three abstentions.

## Run B

All six dispatches passed.

- Clean slide: zero restorations, one abstention.
- Projected slide: zero restorations, two abstentions. No duplicate Unicode
  relation was inserted for the primary LaTeX representation.
- Handwriting: zero restorations, one abstention. The primary already contained
  all required content.
- Formula: zero restorations, three abstentions.
- Table: zero restorations, zero abstentions. No GFM row was split.
- Ordered slide plus formula: zero restorations, three abstentions.

## What V14 Proved

All three v13 structural defects are fixed live:

1. No extra plus was inserted between signed handwriting anchor lines.
2. No LaTeX-equivalent relation was duplicated on projected content.
3. Both calibration tables remained valid and passed.

The remaining failure is bounded auxiliary availability. In Run A handwriting,
the primary omitted one genuine plus and only one of three strict ledgers was
usable. Lowering quorum to one would accept a single uncorroborated scout and
reintroduce false-positive risk. The next targeted experiment should instead
measure a larger fixed independent scout pool under the same strict parser and
v14 structural guards.

Handwriting and all other images remain one board workflow. Phase 1 remains
NO-GO.
