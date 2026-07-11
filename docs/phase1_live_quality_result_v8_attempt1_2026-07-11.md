# Phase 1 V8 Live Quality Result, Attempt 1

Date: 2026-07-11.

Decision: NO-GO. Preserve this partial evidence; do not resume or overwrite it.

## Bound Contract

- Commit: `04a7c9f9a36dd880afd9bc29ebb315798804d7ee`
- Provider/model: DashScope / `qwen3.7-plus-2026-05-26`
- Region/endpoint kind: `cn-beijing` / shared
- Prompt/workflow: `board.v8`, two independent drafts plus one consensus review
- Planned work: 13 recognitions, exactly 39 provider calls, no SDK or runner retry
- Manifest: 37,712 bytes, SHA-256
  `7200d16ea44b365301ce491bd3353433520d6c8ba2cc686debe6562173623e35`
- Evidence: `evidence/phase1/phase1-quality-v8-2026-07-11-cn-beijing.json`

The first launch attempt made no provider call and created no evidence because
`PYTHONPATH=src;.` duplicated the repository `tests` namespace. The import-origin
guard rejected it. Relaunching with `PYTHONPATH=src` proved exact repository
origins and used the unchanged call plan.

## Result

The guarded run started at `2026-07-11T16:35:58.500125Z` and stopped at
`2026-07-11T16:53:15.356553Z`. The evidence is 59,675 bytes with SHA-256
`fd34fb9f3ec7d37674ba7f779f3db743a36b76af81371a27090e8c1b7d75fe94`.

- Smoke passed perfectly and reported three calls.
- Five single-fixture Run A recognitions completed and reported 15 calls.
- Four of those five passed: clean slide, projected slide, formula board, and
  table.
- Formula consensus passed 12/12 signatures, 133/133 atom precision, and
  108/108 critical atoms. V8 therefore prevented the prior `s_4` to `S_4`
  mutation in this independent run.
- Handwriting failed only `text_critical_accuracy_below_one`: 29/30 recall,
  35/37 precision, 5/6 critical-token accuracy, 10/10 critical slots, and no
  unexpected critical token. It omitted one genuine standalone `+` again.
- Run A's ordered request timed out on its first draft after 120.954 seconds.
  It produced no result contract and was not scored.
- Run B never started.

The evidence summary reports 7 recognition invocations, 18 provider calls from
successful recognition metadata, zero completed full runs, and zero passed full
runs. Including the failed ordered-request draft, 19 provider calls were
attempted. The terminal failure is retryable `PROVIDER_TIMEOUT` with
`workflow_pass=draft` and `provider_calls_attempted=1`.

## Diagnosis

Consensus fixes destructive formula rewriting but does not reliably solve the
small standalone-mark omission. The targeted v8 handwriting pass was real but
not robust under an independent full-run dispatch. This is still one unified
board problem: no evidence supports adding handwriting-specific routing or
weakening source truth. The plus is visibly present and remains required.

The next experiment must preserve whole-run evidence and remain generic across
board content. It should make one-sided small signs explicit disagreement items
that the final pass must adjudicate and account for, rather than asking the
model to rewrite two whole drafts without an auditable difference checklist.
Do not selectively retry this failed ordered dispatch or call this attempt a
completed Run A.
