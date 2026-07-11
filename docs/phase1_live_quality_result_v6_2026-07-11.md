# Phase 1 Live Quality V6: 2026-07-11

Status: complete review evidence; one of two full runs passed, so Phase 1
remains NO-GO.

Evidence is preserved at
`evidence/phase1/phase1-quality-v6-2026-07-11-cn-beijing.json`.

## Bound Contract

- Source commit: `ef63a432ed8c5af61eb164ed754a2d2c1f9dda66`
- Provider/model: DashScope / `qwen3.7-plus-2026-05-26`
- Region/endpoint kind: `cn-beijing` / shared
- Prompt/scorer/evidence: `board.v6` /
  `labeled-latex-restricted.v5` /
  `ocrllm.phase1-quality-evidence.v6`
- Thinking/high-resolution: enabled / enabled
- Review passes: 1
- Plan: 13 recognition invocations, 26 provider calls, zero retries

The preflight authenticated 107 clean relevant files, all 20 artifacts, exact
review configuration, credential presence without disclosure, and an absent
evidence path.

## Result

All 13 recognition invocations and all 26 provider calls returned. Every result
reported `review_passes=1` and `provider_call_count=2`. Both full runs completed
without a transport failure. Run A passed all six dispatches. In run B, every
dispatch except the formula board passed.

```text
recognize_invocations = 13 / 13
reported_provider_calls = 26 / 26
completed_full_runs = 2
passed_full_runs = 1
phase1_gate_passed = false
```

Handwriting passed independently in both runs. The review workflow therefore
closed both earlier failure modes: neither run missed the center `+`, and
neither hallucinated hatch strokes as digits.

The run-B formula failure was one review regression in F04:

```text
source/draft: s_4 = 1 + 2 + 3 + 4 = 10
review:       S_4 = 1 + 2 + 3 + 4 = 10
failure: formula_unexpected_atoms
signature accuracy: 11/12
atom precision: 132/133
critical atoms: 108/108
```

The hard formula gate correctly rejected the lowercase-to-uppercase identifier
change. Do not add uppercase `S` as an accepted form: the source is lowercase.

The complete 97,150-byte evidence file has SHA-256
`bc256bfbdc73f7d5f80806eb95767d4e68f17cb512f76c9e6daaba5278504707`.

## Next Action

Preserve v6 unchanged. Version the review prompt to be conservative: change a
draft item only when pixels clearly contradict it; otherwise preserve exact
identifier spelling and case. Continue to restore clear omissions and remove
unsupported hallucinations. Test both handwriting repair and formula
non-regression before another full gate.
