# Phase 1 Unified Board Handwriting Debug: 2026-07-11

Status: offline correction complete; repeated live v4 evidence pending.

This record supersedes the temporary recommendation to split handwriting from
the `board` capability. The user rejected that split based on legacy product
trials. Source inspection and controlled provider tests support the user's
diagnosis: most of the apparent handwriting gap came from defective fixture
truth, and the remaining gap came from the request workflow.

## Decision

Two paths were evaluated:

1. Split printed/document recognition from handwriting. This would avoid one
   failing fixture but would turn a test defect into a public API distinction.
2. Keep one `board` capability, repair source truth, and test the complete-board
   workflow. This is implemented because the work and provider capability are
   the same, and the evidence does not justify capability-specific routing.

No handwriting profile, threshold exception, crop pipeline, OCR-model switch,
or model ensemble was added.

## Source Audit

The committed CC0 whiteboard fixture was compared with a 4160-pixel audit
derivative fetched through the provenance service. The derivative is audit
evidence only; it is not claimed to be the byte-identical Wikimedia original
and is not committed.

The old 25-token annotation had four material defects:

- The source literally reads `Enzymens`; the manifest incorrectly corrected it
  to `Enzymes`. Repeated Qwen3.7 output was source-faithful.
- Cursive initial case in `sticky`, `selection`, and `screening` is visually
  ambiguous, but the old truth required one exact case.
- The clearly visible `R-DNA / Replasmid` label was omitted. Correct output was
  therefore penalized for the words and for the `-` and `/` critical symbols.
- Genuine faint diagram labels such as nucleotide sequences and end markers
  were omitted, so recognizing more of the board reduced precision.

The corrected manifest has 30 required atomic occurrences, 16 optional
source-declared occurrences, and 10 critical text slots. Required content
controls recall. Required plus optional source content controls precision.
Optional absence never lowers recall, but undeclared inventions and unexpected
critical symbols still fail.

## Workflow Audit

Controlled calls changed one variable at a time:

- Whole-board perspective correction did not change the disputed readings.
- The legacy Chinese board prompt on the same crop did not change the core
  readings.
- A 4160-pixel perspective-corrected derivative exposed more micro-labels but
  did not change the disputed readings.
- Qwen3.7 thinking mode captured both visible `+` operators, the omitted
  `R-DNA / Replasmid` label, and additional faint labels.

The first three controls reject cropping, prompt transplantation, and input
resolution as the primary fix. Thinking mode is now pinned for comparable v4
evidence because it resolves the one genuine critical-symbol omission left by
the corrected annotation.

## Versioned Implementation

- Runtime prompt: `board.v4`, with an explicit complete-image/faint-label
  inspection instruction and no fixture-specific wording.
- Evidence request: Qwen3.7 Beijing endpoint, thinking enabled, high-resolution
  images enabled.
- Scoring dialect: `labeled-latex-restricted.v4`.
- Evidence schema: `ocrllm.phase1-quality-evidence.v4`.
- Manifest: 37,492 bytes, SHA-256
  `b0a38e364ca7e8a2b799548304a219392b5570ab515187ec72d52cd785bfbbb0`.
- The v4 normalizer treats only line-leading Unicode or LaTeX diagram arrows as
  layout. Inline arrows remain content and fail closed when unsupported.

Re-scoring each preserved v1 and v2 handwriting response removes six false
failure codes. Both retain only `text_critical_accuracy_below_one`, caused by
the genuinely missing second `+`. The captured thinking-mode response passes
the same unified `board` scorer offline with 30/30 required recall, all critical
tokens, all 10 critical slots, and precision above the unchanged 85% threshold.

## Verification

```powershell
uv run --no-project --isolated --with 'Pillow==12.3.0' `
  --with 'pytest>=8,<10' --with 'openai>=2.30,<3' `
  --python 'D:\Anaconda\envs\OCRLLM\python.exe' `
  python -m pytest -q -p no:cacheprovider
# 583 passed

uv run --no-project --isolated --with 'Pillow==12.3.0' `
  --python 'D:\Anaconda\envs\OCRLLM\python.exe' `
  python -m tests.quality.generators.generate_phase1_fixtures --check
# Phase 1 generated fixtures are byte-identical.

& 'D:\Anaconda\envs\OCRLLM\python.exe' -m compileall -q src tests
```

The base OCRLLM environment intentionally remains on Pillow 12.1.1; the pinned
12.3.0 generator proof uses the documented isolated overlay.

## Remaining Gate

This is not live GO evidence. Commit and push the offline contract, run the
strict no-network preflight from that exact clean commit, then write two fresh
complete v4 runs to a new evidence path. Keep Phase 1 NO-GO until both runs pass.

The earlier Qwen3.5-OCR document-parsing signed-URL response remains rejected.
No signed URL, query credential, private screenshot response, or temporary
high-resolution audit derivative is committed.
