# Phase 1 Live Quality V4 Attempt 1: 2026-07-11

Status: transport-aborted; no quality conclusion.

Evidence is preserved at
`evidence/phase1/phase1-quality-v4-2026-07-11-cn-beijing.json`.

## Bound Contract

- Source commit: `a4fc4181e2aa37207224df4de5a2e9c30863d2a8`
- Provider/model: DashScope / `qwen3.7-plus-2026-05-26`
- Region/endpoint kind: `cn-beijing` / shared
- Prompt: `board.v4`
- Thinking/high-resolution: enabled / enabled
- Evidence schema: `ocrllm.phase1-quality-evidence.v4`
- Planned calls: 13, zero runner retries, zero SDK retries

The direct no-network preflight authenticated 103 clean relevant files, all 20
artifacts, the exact 13-call plan, the credential's presence without printing
it, and an absent evidence path.

## Result

The clean-slide smoke was invoked once. DashScope returned HTTP 500 with
provider code `internal_server_error`. The adapter mapped it to retryable
`PROVIDER_UNAVAILABLE`, and the guarded runner aborted without invoking another
dispatch.

```text
recognize_invocations = 1
completed_full_runs = 0
passed_full_runs = 0
phase1_gate_passed = false
terminal_code = PROVIDER_UNAVAILABLE
```

The atomic 27,245-byte evidence file has SHA-256
`49e5a3981d13137c5a8ca543b96290bf3b30595ed5cd6d19ca58362c19134015`.
It is a valid transport-failure record, not failed recognition-quality evidence.

## Next Action

Do not overwrite this evidence and do not retry the smoke inside this plan.
Under the user's unrestricted API authorization, a later attempt may start a
new complete zero-retry plan from a new clean commit and a new evidence path.
Phase 1 remains NO-GO until two full runs in one complete attempt pass.
