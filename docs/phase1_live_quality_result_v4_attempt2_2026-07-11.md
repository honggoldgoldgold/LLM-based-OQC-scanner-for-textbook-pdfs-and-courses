# Phase 1 Live Quality V4 Attempt 2: 2026-07-11

Status: partial run aborted by timeout; useful handwriting diagnostic, not a GO
gate.

Evidence is preserved at
`evidence/phase1/phase1-quality-v4-attempt2-2026-07-11-cn-beijing.json`.

## Bound Contract

- Source commit: `78892445f300128e8a9b252d9483c5608cbaf796`
- Provider/model: DashScope / `qwen3.7-plus-2026-05-26`
- Region/endpoint kind: `cn-beijing` / shared
- Prompt/evidence: `board.v4` / `ocrllm.phase1-quality-evidence.v4`
- Thinking/high-resolution: enabled / enabled
- Planned calls: 13, with zero runner and SDK retries

The no-network preflight authenticated 103 clean relevant files, all 20
artifacts, the fixed plan, credential presence without disclosure, and a new
absent evidence path.

## Result

Seven calls were invoked. The smoke and the five single-fixture dispatches all
returned provider results. Printed slide, projected slide, formula board, and
table passed. Handwriting returned all 10 critical text slots, but its scorer
failed:

```text
required recall = 29/30
content precision = 33/40
critical token accuracy = 5/6
critical slot accuracy = 10/10
failure codes = content_precision_below_threshold,
                text_critical_accuracy_below_one,
                text_unexpected_critical_units
```

The output still missed the center standalone `+`. It also represented the two
line-leading diagram connectors as ASCII `->`; v4 declared Unicode and LaTeX
forms but not this equivalent layout spelling, so the two `-` and two `>` tokens
were false critical insertions. The remaining unmatched words were faint
micro-label readings and require source inspection rather than automatic
acceptance.

The final ordered request in run A then timed out. The adapter recorded
retryable `PROVIDER_TIMEOUT`; the runner aborted without starting run B.

```text
recognize_invocations = 7
completed_full_runs = 0
passed_full_runs = 0
phase1_gate_passed = false
terminal_code = PROVIDER_TIMEOUT
```

The 57,929-byte evidence file has SHA-256
`936edd25c72d3d58f0d70fed4621c603ced023eca572901a8cf773d62635cc6e`.

## Next Action

Preserve this evidence and do not resume or overwrite it. Add a corruption-
tested line-leading ASCII connector equivalence, audit the faint labels, and
experiment on the handwriting fixture before another complete gate. The
missing center `+` is a real workflow problem and must not be normalized away or
made optional merely to pass.
