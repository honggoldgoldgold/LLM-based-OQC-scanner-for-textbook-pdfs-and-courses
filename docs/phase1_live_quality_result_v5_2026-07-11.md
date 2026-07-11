# Phase 1 Live Quality V5: 2026-07-11

Status: complete 13-call evidence; one of two full runs passed, so Phase 1
remains NO-GO.

Evidence is preserved at
`evidence/phase1/phase1-quality-v5-2026-07-11-cn-beijing.json`.

## Bound Contract

- Source commit: `081dd2d8bb3d9f47f3fa3998476481294c1fa111`
- Provider/model: DashScope / `qwen3.7-plus-2026-05-26`
- Region/endpoint kind: `cn-beijing` / shared
- Prompt/scorer/evidence: `board.v5` /
  `labeled-latex-restricted.v5` /
  `ocrllm.phase1-quality-evidence.v5`
- Thinking/high-resolution: enabled / enabled
- Planned calls: 13, with zero runner and SDK retries

The no-network preflight authenticated 104 clean relevant files, all 20
artifacts, the exact plan, credential presence without disclosure, and an
absent evidence path.

## Result

All 13 provider calls returned successfully. Smoke passed. Both full runs
completed. Run B passed all six dispatches. In run A, printed slide, projected
slide, formula board, table, and ordered request passed; only handwriting
failed.

```text
recognize_invocations = 13
completed_full_runs = 2
passed_full_runs = 1
phase1_gate_passed = false
provider_failures = 0
```

The run-A handwriting score was:

```text
required recall = 30/30
content precision = 38/40
critical token accuracy = 6/6
critical slot accuracy = 10/10
failure code = text_unexpected_critical_units
```

The sole unexpected critical occurrence was `111110`. Source comparison shows
that the model reinterpreted six short hatch strokes on a plasmid segment as
digits. They are drawing texture, not source text. The scorer correctly rejects
the hallucination. Run B did not hallucinate the digits and passed with 30/30
required recall, 6/6 critical tokens, 10/10 slots, and precision above the
unchanged threshold.

The complete 95,483-byte evidence file has SHA-256
`0ceb74a7f05ed2ca5cbcac8eb3eb1c340dfac4bf43ceb84e6883cbe4c40e2343`.

## Decision

Do not add `111110` to optional truth and do not weaken unexpected-critical
gating. The next generic prompt correction should distinguish textual operator
marks from repeated hatch/fill/texture strokes. Test it on the same unified
`board` capability before another complete gate.
