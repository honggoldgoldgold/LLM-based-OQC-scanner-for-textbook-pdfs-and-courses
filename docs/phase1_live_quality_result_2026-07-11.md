# Phase 1 Live Quality Result: 2026-07-11

Status: complete live evidence; Phase 1 NO-GO.

This record summarizes the first fixed Phase 1 live gate without changing its
frozen prompt, corpus, scorer, thresholds, or results. The complete machine
evidence, including raw provider Markdown and every metric, is
`evidence/phase1/phase1-quality-2026-07-11-cn-beijing.json`.

## Evidence Identity

| Field | Value |
|---|---|
| Evidence schema | `ocrllm.phase1-quality-evidence.v1` |
| Evidence state | `complete` |
| Execution mode | `live` |
| Source commit | `7df3514a81481d37547ea1a624deed224998bddd` |
| Region | `cn-beijing` |
| Provider | `dashscope` |
| Model | `qwen3.7-plus-2026-05-26` |
| Calls | 13 planned, 13 invoked, zero runner retries |
| Full runs | 2 completed, 0 passed |
| Started | `2026-07-11T09:03:32.553711Z` |
| Finished | `2026-07-11T09:05:47.685222Z` |
| Evidence bytes | 73,627 |
| Evidence SHA-256 | `cfb2ee423eafecbc87190f9e30d39439f0ea0a865d1a0348a140f67d8088fa23` |

Independent post-run validation strict-loaded the JSON, confirmed its clean
relevant-tree/source-commit binding, and found neither the current credential
nor the full endpoint in raw or JSON-escaped form. The evidence records only a
SHA-256 identity for the configured endpoint. All 13 provider requests returned
and `terminal_failure` is null.

## Gate Result

The clean-slide smoke was rejected by the scorer, so it did not establish the
required feasibility pass. Both complete six-dispatch runs failed. The result
is therefore Phase 1 NO-GO; no capability becomes `available`.

| Dispatch | Run A | Run B | Observed reason |
|---|---|---|---|
| Printed slide | Rejected | Rejected | Provider rendered the visible `>=` relation as inline LaTeX; v1 rejects the dollar delimiter outside its labeled-formula grammar. |
| Projected slide | Rejected | Rejected | Same inline-LaTeX presentation mismatch. |
| Handwriting | Gate failed | Gate failed | Real quality miss: text recall `20/25`, precision `20/30`, critical text `3/4`, and critical slots `7/9`. |
| Formula board | Rejected | Rejected | Provider omitted the colon required by the frozen `F01: $...$` v1 grammar. |
| Calibration table | Passed | Passed | Critical cells `25/25`, data cells `30/30`, and headers `6/6`. |
| Ordered slide + formula | Rejected | Rejected | Run A used the same missing-colon formula form; run B used a four-column paired formula table outside the frozen two-column grammar. |

The handwriting output missed the `handwriting-enzymes-slot` and
`handwriting-sticky-end-slot` critical matchers in both runs. Its English
channel produced recall `17/21` and precision `17/25`. This remains a product
quality failure even if a later scorer version accepts more Markdown/LaTeX
presentation forms.

## Contract Diagnosis

The frozen v1 evidence remains authoritative and failed. It must not be
retroactively rescored as a pass.

The public `board.v1` prompt asks for Markdown and LaTeX but does not state the
scorer's stricter labeled-formula serialization. Qwen consistently produced
reasonable Markdown variants that the v1 parser does not accept: inline math
delimiters, formula labels without a colon, and a paired four-column table. This
is a deterministic prompt/scorer contract mismatch, separate from the genuine
handwriting recall and precision failure.

Two correction paths were considered:

1. Widen v1 after seeing this evidence and reinterpret the run. Rejected because
   it would lower or move a frozen gate after observation.
2. Preserve v1 and introduce a separately versioned prompt/scoring contract
   with deliberate-corruption tests before any new paid run. Selected because
   it keeps the audit trail honest and permits narrow, predeclared presentation
   equivalences without hiding content errors.

## Next Authorized Work

Offline work may design and test a versioned correction. It must keep exact
critical values and thresholds, continue to reject malformed or unsupported
content, and preserve this evidence unchanged. A second billed image run is not
authorized by the completed 13-call confirmation; it requires a new explicit
decision, a new evidence path, and the same clean preflight discipline.

## Subsequent Offline Correction

The separately versioned `board.v2` / `labeled-latex-restricted.v2` correction
is now implemented without editing this evidence. Its prompt declares the
formula grammar and exact handwriting case/spelling. Its fail-closed normalizer
handles only the observed presentation equivalents plus standalone horizontal
rules. The full suite passes `568` tests.

As a diagnostic only, v2 makes the preserved smoke and all non-handwriting
dispatches pass. Both handwriting dispatches still fail the original seven
quality gates. This confirms that the format mismatch is isolated while the
product-quality failure remains visible; it does not turn this v1 run into GO
evidence.
