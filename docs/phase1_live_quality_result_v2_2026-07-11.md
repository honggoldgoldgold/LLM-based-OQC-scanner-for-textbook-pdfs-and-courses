# Phase 1 V2 Live Quality Result: 2026-07-11

Status: complete live evidence; Phase 1 NO-GO.

This is the immutable result for the first `board.v2` /
`labeled-latex-restricted.v2` gate. It does not replace or reinterpret the v1
evidence. Complete raw Markdown and metrics are in
`evidence/phase1/phase1-quality-v2-2026-07-11-cn-beijing.json`.

## Evidence Identity

| Field | Value |
|---|---|
| Evidence schema | `ocrllm.phase1-quality-evidence.v2` |
| State / mode | `complete` / `live` |
| Source commit | `94d5187ff8718f2683f67e4c5f75e95c3a9d9070` |
| Region | `cn-beijing` |
| Calls | 13 planned, 13 invoked, zero retries |
| Full runs | 2 completed, 0 passed |
| Provider failures | 0 |
| Terminal failure | none |
| Evidence bytes | 78,235 |
| Evidence SHA-256 | `03275cf5922a46dd59fc75e4ab6dc6499e3aeea973190f1d3a6f48b0c556df0b` |

Independent validation strict-loaded the JSON, verified every Markdown byte
count and hash, and found neither the current credential nor full endpoint in
raw or JSON-escaped form.

## Gate Result

| Dispatch | Run A | Run B | Result |
|---|---|---|---|
| Printed slide | Rejected | Rejected | Qwen used Unicode `⩾` (U+2A7E); the v2 tokenizer has no declared equivalence to `≥`. |
| Projected slide | Passed | Passed | All gates passed. |
| Handwriting | Rejected | Rejected | Qwen preserved two diagram connectors as line-leading `→` (U+2192); v2 has no declared structural-arrow treatment. |
| Formula board | Passed | Passed | All gates passed. |
| Calibration table | Passed | Passed | All gates passed. |
| Ordered slide + formula | Rejected | Rejected | The printed-slide `⩾` rejection propagates into the ordered request. |

The runner printed the correct evidence hash, but the PowerShell stdin pipeline
reported process exit code 1 rather than the runner's documented gate-failure
code 5. The complete JSON has no terminal failure and is authoritative. No call
was repeated because of the shell-code anomaly.

## Decision

Phase 1 remains NO-GO. Do not modify or rescore this evidence. The next
correction must be separately versioned and may only canonicalize
content-preserving typography (`⩾`/`⩽`) and line-leading diagram connectors. It
must preserve inline arrows, wrong relations, wrong values, and all exact
content thresholds as failures.
