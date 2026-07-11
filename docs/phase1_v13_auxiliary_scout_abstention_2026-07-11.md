# Phase 1 V13 Auxiliary Scout Abstention Record

Date: 2026-07-11.

Status: targeted Beijing probes and the complete offline suite pass; complete
live gate pending.

## Boundary Decision

Handwriting, whiteboards, printed slides, formulas, and mixed ordered image
groups continue through one `board` profile. V13 does not inspect fixture class,
route handwriting separately, use scorer feedback in production, or weaken the
handwriting truth.

The Qwen3.7 primary transcript remains authoritative. Qwen-VL Max scouts are
bounded auxiliary evidence: they may add only parsed standalone signs that meet
two-of-three anchored quorum. They cannot contribute prose, labels, formulas,
or replacement text.

## V12 Failure Diagnosis

The frozen v12 run from commit `05adc64` aborted at the first bilingual
printed-slide smoke recognition. Its strict parser rejected the scout set
before scoring. The atomic evidence is 29,606 bytes with SHA-256
`ea16775eec1aea7af79681e1f90b76ca075864e9b8e9b1b00dc1c90d125282ea`.

Raw no-sign diagnostics showed the cause. The slide contains eight rounded
content panels but no standalone sign requiring restoration. Two Qwen-VL Max
responses emitted a header followed by many false `-` records corresponding to
separate text lines; the third used a malformed four-field table shape. The
parser correctly rejected all three. Requiring the entire recognition to fail
because optional auxiliary evidence abstained was the workflow defect.

## Rejected Contrastive Audit

A candidate-aware prompt was tested before implementation. One current Qwen3.7
smoke transcript and three Qwen-VL Max comparisons consistently reported
`>= | TARGET RECALL: | 95%`. Three comparisons against a preserved handwriting
draft known to miss `foreign gene + I:V` instead re-reported the already present
`Transformation + Validation` sign. The contrastive instruction therefore did
not ground omission location reliably and was rejected.

## Accepted Scout Protocol

The final targeted prompt adds exact `NONE` for a zero-event result and forbids
panel borders, box outlines, underlines, grids, line relationships, list
markers, decorative strokes, and identifier/date/number hyphens.

Three independent printed-slide scouts returned exact `NONE`. Three independent
handwriting scouts all returned both genuine plus occurrences, including
`+ | foreign gene | I:V`. Their final list-separator record disagreed: one
returned the visible minus and two returned plus. This revealed a second local
guard needed independently of prompt quality.

V13 therefore applies all of these deterministic rules:

1. Exact `NONE` parses as a valid empty ledger and is not an abstention.
2. Any malformed ledger abstains as a whole; none of its records enter quorum.
3. The result metadata records the number of scout abstentions.
4. A two-of-three sign quorum is still required across distinct valid scouts.
5. A candidate restoration is blocked when any supported standalone sign is
   already present between the same primary-transcript anchors. This prevents a
   disagreeing plus from replacing or supplementing an existing minus.
6. If no safe quorum insertion remains, the primary transcript stays
   byte-identical.

Malformed scout output is never accepted. Abstention is fail-closed for the
auxiliary channel while preserving a valid authoritative primary result.

## Diagnostic API Accounting

After the frozen v12 gate, 17 Beijing diagnostic requests were made:

- 1 raw v12 smoke scout succeeded, then local CP-1252 console printing failed;
- 3 UTF-8 raw v12 smoke scouts exposed the invalid panel/line ledgers;
- 7 contrastive probes covered one current primary, three smoke audits, and
  three handwriting audits;
- 6 final-protocol probes covered three smoke and three handwriting scouts.

The console encoding error occurred after its provider response and is counted.
None of these calls is relabeled as gate evidence.

## Frozen V13 Candidate

- Prompt: `board.v13`.
- Primary: one `qwen3.7-plus-2026-05-26`, thinking enabled.
- Scouts: three `qwen-vl-max`, thinking disabled, strict ledger, two-of-three
  quorum, malformed-ledger abstention.
- Formula scorer: `labeled-latex-restricted.v6`.
- Timeout: 180 seconds per call.
- Plan: 13 recognitions and 52 provider calls; no retry.
- Evidence schema: `ocrllm.phase1-quality-evidence.v13`.
- Manifest: 37,853 bytes, SHA-256
  `890f67941bc2783bc81f91ab42b1290fb4ad1df4c722cb2f458e762dd9ad1522`.
- Focused offline suite: 96 passed.
- Exact isolated repository suite: 667 passed.

Phase 1 remains NO-GO pending one fresh complete live gate with two passing full
runs and clean package profiles.
