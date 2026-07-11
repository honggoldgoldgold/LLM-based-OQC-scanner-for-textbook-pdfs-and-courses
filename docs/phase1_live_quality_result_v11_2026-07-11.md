# Phase 1 V11 Live Quality Result

Date: 2026-07-11.

Decision: NO-GO. Preserve this complete evidence unchanged.

## Result

V11 ran from commit `60eeb677538df50e3b4c2a2c3e5c61cc8ff9bd35` with
the 37,853-byte manifest SHA-256
`3b5c5392b1e10ed40261ac08dc5fbf692f0b451c6c13c4c71a44b710f28ec86b`.
All 13 recognitions and 52 provider calls returned; both full runs completed and
neither passed. There was no terminal provider failure. The 104,026-byte
evidence SHA-256 is
`44b74fdb0ba57662a6c49193c6c203b147b88a723bed8698b983fb9f1a59465f`.

Every non-handwriting dispatch passed in both runs. Formula dialect v6 accepted
safe source-equivalent `\text{P}`/`\text{E}` forms without weakening the formula
atom gate. Ordered requests completed under the 180-second timeout. The thematic
break regression did not recur.

## Handwriting Run A

- 30/30 recall, 38/58 precision, 6/6 critical tokens, 10/10 critical slots.
- Failures: content precision, unexpected critical units, and English content
  precision.
- Restored signs: zero.
- Both genuine plus signs were present.
- Qwen3.7 appended invented structural prose: `Diagram Labels`, numbered circle
  captions, positional words, and a curved-segment caption around otherwise
  plausible faint labels. Those captions are not source text.

## Handwriting Run B

- 29/30 recall, 36/55 precision, 5/6 critical tokens, 10/10 critical slots.
- Failures additionally include a missing plus and duplicate critical slots.
- Restored signs: zero.
- Qwen3.7 appended Markdown diagram-description sections such as `MCS Diagram`,
  `Plasmid Vector Diagram`, and `Foreign Gene Diagram`. It also omitted one
  standalone plus.

## Decision

Increasing full-transcript scouts from two to three did not create usable sign
quorum in either handwriting run. Do not add more scouts of the same shape.
The next targeted experiment should instead:

1. forbid model-created region captions, diagram descriptions, numbering, and
   positional prose unless literally visible in the source; and
2. make scouts return only a strict standalone-sign ledger with immediate
   neighboring visible text, rather than another full transcript.

Run targeted probes before another full paid gate. Keep one unified board
profile and the unchanged fixture truth.
