# Phase 1 V15 Live Quality Result

Date: 2026-07-11.

Status: complete provider execution; both full runs failed one distinct local
policy check.

## Bound Contract

- Commit: `248c627b8e42ea12349ca9a344da13895b5ee130`
- Region: `cn-beijing`
- Prompt: `board.v15`
- Primary: one `qwen3.7-plus-2026-05-26`, thinking enabled
- Scouts: three independent `qwen3.7-plus-2026-05-26`, thinking enabled
- Plan: 13 recognitions and exactly 52 provider calls; no retry
- Manifest: 37,864 bytes, SHA-256
  `9c5fe09635142c457c464d52f2c4bba8e78964f61e3c06cb4b786d8bf6bf3c11`

The run started at `2026-07-11T20:46:15.978740Z` and finished at
`2026-07-11T21:53:43.360241Z`, about 67 minutes 27 seconds. The outer shell
watchdog detached after one hour while 48 calls were reported; the child runner
continued normally, sealed all 13 recognitions and 52 calls, and exited. There
was no terminal provider or runner failure and no selective retry.

Preserve
`evidence/phase1/phase1-quality-v15-2026-07-11-cn-beijing.json`: 99,223 bytes,
SHA-256
`65dad6a47206562c526f643bab600d87e0f68987f443cc6757e7f07ec9fff95b`.
Both full runs completed; neither passed.

## Run A

- Clean slide, projected slide, formula, table, and ordered slide-plus-formula
  all passed with zero restorations and zero abstentions.
- Handwriting had zero abstentions and one restoration. The primary transcript
  already contained both genuine pluses and all visible text, but the scout
  quorum inserted a diagrammatic `←` before `RG`. The scorer rejected
  unsupported visible character U+2190.

## Run B

- Clean slide, projected slide, handwriting, table, and ordered
  slide-plus-formula all passed with zero abstentions.
- Handwriting passed with one safe restoration, proving the thinking-scout
  workflow can repair missing content without an availability failure.
- Formula had zero restorations and zero abstentions but the primary used
  `\mathrm{P}`, `\mathrm{A}`, `\mathrm{B}`, `\mathrm{M}`, and `\mathrm{E}`.
  The scorer rejected unsupported LaTeX command `\mathrm`. Every use wrapped
  exactly one ASCII letter and was source-equivalent to the fixture.

## Diagnosis

V15 solves the v14 scout-availability problem: all 39 scout responses across
the 13 recognitions yielded supported evidence, and every recorded abstention
count is zero. The remaining failures are independent and local:

1. Directional arrows are ambiguous between diagram geometry and textual
   operators. Auxiliary scouts must not restore them. The complete primary may
   still transcribe visible arrows normally.
2. Formula dialect v6 safely unwraps one-letter `\text{X}` but not the equally
   narrow one-letter `\mathrm{X}` form observed live. Dialect v7 should unwrap
   only one ASCII letter inside exact labeled formulas; multi-letter or malformed
   `\mathrm` must remain rejected.

V16 should make only those changes. It must not split handwriting routing,
weaken content truth, accept broad LaTeX, change provider count, or add retry.

Phase 1 remains NO-GO.
