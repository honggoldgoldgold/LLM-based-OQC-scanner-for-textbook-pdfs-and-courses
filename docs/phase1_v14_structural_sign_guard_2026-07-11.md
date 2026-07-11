# Phase 1 V14 Structural Sign Guard Record

Date: 2026-07-11.

Status: offline gates pass; complete live gate pending.

## Decision

V13 completed all 52 provider calls and proved that Qwen3.7 can produce complete
handwriting content in both full runs. The remaining failures were caused by
local sign insertion after the primary response, not separate model capability.
V14 changes only deterministic merger policy and keeps one `board` workflow for
all image classes.

No provider, model, prompt text, call count, fixture truth, scorer threshold,
or public routing decision changes. `board.v14` identifies the new local result
contract.

## Exact V13 Regressions

The 98,101-byte v13 evidence SHA-256
`b10b88eeeba94f637165ddf32b95eb3ff3e3e02d4ccdd254ad9fbfe39bec67f1`
showed three repeatable defects:

1. Both handwriting results contained `- Selection` and `- Screening`, but the
   conflict window excluded the anchor lines. A disagreeing scout plus was
   inserted between them in both runs.
2. One projected-slide primary contained source `≥` as LaTeX `\ge`; the merger
   counted only exact Unicode tokens and inserted a duplicate Unicode `≥`.
3. Both calibration primaries were valid GFM pipe tables. Five scout signs were
   inserted between data rows, breaking the table before scoring.

## V14 Guards

`count_standalone_sign_representations.py` counts source-equivalent relation
forms before calculating how many restorations remain. Unicode `≥`/`≤`, ASCII
`>=`/`<=`, and LaTeX `\ge`, `\geq`, `\geqslant`, `\le`, `\leq`, and
`\leqslant` are equivalent for this conservative count. Embedded table values
such as `+0.18` do not count as standalone plus signs.

`is_gfm_pipe_table_row.py` identifies conservative outer-pipe row boundaries.
The merger refuses an insertion immediately before or after such a row, so it
cannot split a valid table block.

The sign-conflict window now includes both anchor lines. A sign attached to an
anchor, such as the minus in `- Selection`, blocks any additional supported
sign at that anchored location. Missing `foreign gene + I:V` remains eligible
because neither anchor line contains a sign.

All rules prefer the primary when uncertain. They do not inspect handwriting,
fixture IDs, scorer output, or image class.

## Frozen V14 Contract

- Prompt identity: `board.v14`; scout prompt text remains the v13 strict
  `NONE`/ledger protocol.
- Primary: one `qwen3.7-plus-2026-05-26`, thinking enabled.
- Scouts: three `qwen-vl-max`, thinking disabled, two-of-three valid quorum.
- Formula scorer: `labeled-latex-restricted.v6`.
- Timeout: 180 seconds per call.
- Plan: 13 recognitions and exactly 52 Beijing provider calls; no retry.
- Evidence schema: `ocrllm.phase1-quality-evidence.v14`.
- Manifest: 37,853 bytes, SHA-256
  `dae74f4da207d01e311f5756a204e557ca6e6982073024d2e48b672315febb07`.
- Direct structural regression suite: 37 passed.
- Wider workflow/quality suite: 153 passed.
- Exact isolated repository suite: 685 passed.
- Generated fixtures are byte-identical; compileall, Ruff, diff, and conflict
  checks pass.

No v14 provider call has been made yet. Phase 1 remains NO-GO pending a fresh
complete live gate with two passing full runs and clean package profiles.
