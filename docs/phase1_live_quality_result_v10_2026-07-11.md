# Phase 1 V10 Live Quality Result

Date: 2026-07-11.

Decision: NO-GO. Preserve this complete evidence unchanged.

## Bound Contract

- Commit: `79a90d30a46394ecff764ebf47a2471ad1127893`
- Primary: `qwen3.7-plus-2026-05-26`, thinking enabled
- Scouts: two independent `qwen-vl-max`, thinking disabled
- Region: `cn-beijing`
- Prompt: `board.v10`
- Timeout: 180 seconds per call
- Plan: 13 recognitions, 39 provider calls, no retry
- Manifest: 37,853 bytes, SHA-256
  `15a7018084cd1d53c82acbf260bb19095ccb29664cc357beaaaefd9044b8f971`
- Evidence: `evidence/phase1/phase1-quality-v10-2026-07-11-cn-beijing.json`

## Result

All 13 recognitions and 39 provider calls returned. Both full runs completed;
Run B passed all six dispatches, while Run A did not pass. There was no terminal
provider failure. The evidence is 98,351 bytes with SHA-256
`8c86c7117efa6ad7e999bad3180e861981a27598788cfaaeb526472ae65b9c54`.

Run A:

- Clean slide, projected slide, table, and ordered slide+formula passed.
- Handwriting missed one genuine standalone plus: 29/30 recall, 31/32
  precision, 5/6 critical-token accuracy, 10/10 slots, no unexpected critical
  token, and zero restored signs. The two scouts produced no usable anchored
  quorum in this run.
- Formula provider output and result contract succeeded with zero restoration,
  but the scorer rejected source-equivalent `\text{...}` LaTeX with
  `SCORER_REJECTED`. This is a dialect gap, not a measured recognition miss.

Run B:

- All six dispatches passed.
- Handwriting passed at 30/30 recall, 38/39 precision, 6/6 critical tokens, and
  10/10 slots. Its primary already contained both plus signs, so restoration
  remained zero.
- Formula passed without scorer rejection.
- The ordered request passed and reported one restoration.

## Post-Run Safety Finding

The ordered restoration was not source content. It was a Markdown thematic
separator line `---` shared by both scouts and absent from the primary. The
sign parser treated repeated hyphens as a standalone sign. The scorer ignored
the separator, so the gate did not expose the semantic error. V11 must reject
Markdown thematic breaks before they enter quorum processing and add an exact
regression test.

## Next Contract

Two scouts are safe only when they agree, but their recall is insufficient for
the difficult mark. V11 should use three independent scouts and accept a sign
event only when at least two agree at a matching neighbor anchor. This raises
the fixed plan to 52 calls but improves the probability of a usable quorum
without weakening truth or copying scout prose.

V11 should also introduce a narrowly bounded formula normalizer for simple
source-equivalent `\text{single-symbol}` forms. It must reject prose-bearing,
nested, empty, or otherwise unsupported `\text{}` commands and retain the exact
formula corruption gates.
