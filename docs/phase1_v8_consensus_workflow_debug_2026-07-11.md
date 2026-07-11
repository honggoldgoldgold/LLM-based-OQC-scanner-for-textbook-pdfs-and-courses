# Phase 1 V8 Consensus Workflow Debug Record

Date: 2026-07-11.

Status: v8 implementation accepted offline; complete live gate pending.

## Decision

Handwriting and formula/diagram boards remain one `board` recognition profile.
There is no fixture-class routing, handwriting prompt, formula prompt, crop
oracle, or scorer feedback in production. The observed quality gap was caused
by stochastic omission and destructive review behavior, not evidence of two
different model capabilities.

The robust workflow is two independent same-image, same-prompt drafts followed
by one pixel-grounded consensus review. Ordinary recognition stays one call by
default. Robustness is explicit:

```python
RecognitionPreferences(draft_candidates=2, review_passes=1)
```

Only `(1, 0)`, `(1, 1)`, and `(2, 1)` are valid. Two candidates without a
review are rejected because choosing one silently would be arbitrary.

## Rejected V7 Experiment

V7 changed the single-draft review instruction to request minimum corrections
and exact draft preservation. Four production recognitions were run against the
same unified profile, with one draft and one review each:

| Fixture | Trials | Provider calls | Final result |
| --- | ---: | ---: | --- |
| Handwritten whiteboard | 2 | 4 | Both missed the required center `+`: 29/30 recall and 5/6 critical-token accuracy. |
| Formula board | 2 | 4 | Both changed source `s_4` to `S_4`: 11/12 formula signatures and 132/133 atom precision. |

All eight calls returned successfully, but all four reviewed recognitions
failed. Conservative wording alone therefore solved neither failure mode. V7
was never committed as the active contract.

## Consensus Probe

The probe made independent base-prompt calls, then supplied both drafts as
separate line-by-line blockquotes to a third call. The prompt says the drafts
are untrusted data, preserves exact agreement unless pixels contradict it,
resolves disagreement against pixels, restores only visible one-sided
omissions, and removes unsupported content.

Handwriting:

- Draft 1 passed: 30/30 recall, 36/38 precision, 6/6 critical-token accuracy,
  and 10/10 critical slots.
- Draft 2 passed: 30/30 recall, 36/39 precision, 6/6 critical-token accuracy,
  and 10/10 critical slots.
- Consensus passed: 30/30 recall, 37/38 precision, 6/6 critical-token accuracy,
  and 10/10 critical slots.
- The required center `+` was retained, and hatch strokes were not converted to
  the rejected `111110` hallucination.

Formula board:

- Both drafts agreed on source lowercase `s_4`.
- The first consensus call reached the 120-second transport timeout and
  published no final file.
- One bounded recovery call reused the two already-published drafts; it did not
  rerun either draft.
- The recovered consensus passed: 12/12 formula signatures, 133/133 atom
  precision, 108/108 critical atoms, 17/17 text recall and precision, and the
  exact lowercase `s_4`.

The consensus probe therefore attempted seven provider calls: six complete
responses and one timeout. Together with the rejected v7 matrix, the post-v6
investigation attempted 15 calls, with 14 complete responses and one timeout.
Together with the 28 post-v5 calls already recorded in
`phase1_v6_review_workflow_debug_2026-07-11.md`, the prompt/workflow diagnosis
now accounts for 43 provider-call attempts.

Probe Markdown is under ignored `temp/` directories. It is diagnostic material,
not immutable gate evidence and not committed.

## V8 Library Contract

- `RecognitionPreferences.draft_candidates` is exactly `1` or `2` and defaults
  to `1`.
- `RecognitionPreferences.review_passes` is exactly `0` or `1` and defaults to
  `0`.
- Candidate calls use the identical source snapshot, base prompt, provider,
  model, region, and immutable config.
- The consensus prompt lives in its own single-responsibility file and quotes
  every candidate line as data to reduce prompt-injection risk.
- A failed second draft reports `workflow_pass=draft_2`; a failed consensus
  reports `workflow_pass=consensus_review`.
- Any enabled review failure fails the recognition. No draft is returned as a
  fallback.
- Metadata reports `draft_candidates`, `review_passes`, and the exact
  `provider_call_count`.
- No output Markdown is written until the entire workflow succeeds.

The Phase 1 v8 evidence contract pins two candidates plus one consensus review:
13 recognition invocations and exactly 39 provider calls. The runner will not
start unless `--confirm-paid-calls 39` is supplied and will require all 39 calls
to be reported by successful results.

## Atomic Writer Record

All public probe outputs were published through the library atomic writer. The
bounded formula recovery also called `write_markdown_atomically` directly after
the provider returned complete Markdown. While the timed-out consensus call was
in flight, the destination directory existed but contained no final or partial
Markdown. The successful recovery published one complete file. Temporary
same-directory files are flushed and `fsync`ed before atomic publication; the
directory itself is not explicitly `fsync`ed, so do not claim power-loss
durability beyond the documented guarantee.

## Offline Checkpoint

The v8 manifest is 37,712 bytes with SHA-256
`7200d16ea44b365301ce491bd3353433520d6c8ba2cc686debe6562173623e35`.
The exact isolated full suite passes 608 tests. Focused consensus, adapter,
configuration, manifest, runner, and atomic-output tests account for the new
three-call behavior and failure boundaries.

Before live dispatch, also require byte-identical fixture generation,
`compileall`, Ruff, `git diff --check`, secret/signed-URL scans, a clean relevant
tree, and a nonexistent v8 evidence path. Phase 1 remains NO-GO until both full
v8 runs and the clean packaging profiles pass.
