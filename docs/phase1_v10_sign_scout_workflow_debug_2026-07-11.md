# Phase 1 V10 Standalone-Sign Scout Workflow Debug Record

Date: 2026-07-11.

Status: implementation and offline gates complete; clean live v10 gate pending.

## Root Cause

Handwriting and other board content remain one capability. V8 proved that two
Qwen3.7 drafts plus a generative consensus review can preserve formula case,
but the full-run handwriting result still omitted one genuine standalone `+`.
V9 made draft differences explicit and still failed:

- Handwriting trial 1: base draft had 30/30 recall but duplicated a critical
  slot; symbol-audit draft passed; diff-aware final passed.
- Formula trial 1: both drafts were byte-identical and perfect at 12/12
  signatures and 133/133 atoms; the final changed only `s_4` to `S_4` and
  failed at 11/12 and 132/133.
- Handwriting trial 2: base, symbol-audit, and final all missed the same plus at
  29/30 recall and 5/6 critical-token accuracy.

This isolates two separate workflow defects. A generative final can damage
already-correct agreement, and no disagreement reviewer can recover content
that every input draft omitted.

## Model and Legacy Audit

Current official Alibaba documentation identifies `qwen3.7-max-2026-06-08` as
the largest Qwen3.7 model with visual input support. One bounded handwriting
call still missed the same plus at 29/30 and 5/6. Model size did not fix the
failure.

The read-only legacy application defaults to `qwen-vl-max` for vision. Two
independent current `qwen-vl-max` calls each captured both genuine standalone
plus signs and reached 6/6 critical-token accuracy in about ten seconds. They
were weaker on prose: both corrected source `Enzymens` incorrectly and
misspelled `Replasmid`, reaching only 8/10 critical text slots. This is useful
as narrow visual evidence, not as the final transcript.

One `qwen3-vl-plus` request was rejected before inference with provider code
`AllocationQuota.FreeTierOnly`; its free quota is exhausted and paid use is
disabled in the account console. One initial `qwen-vl-max` request was rejected
before inference because thinking was enabled; the model requires a zero
thinking budget. Both rejections wrote no output and are not quality results.

Official references used for the model audit:

- https://help.aliyun.com/zh/model-studio/vision-model
- https://help.aliyun.com/en/model-studio/newly-released-models
- https://help.aliyun.com/en/model-studio/qwen-vl-compatible-with-openai

## Rejected Heterogeneous Rewrite

A Qwen3.7 final received one strong-text Qwen3.7 draft, one `qwen-vl-max`
visual-sign draft containing both plus signs, their deterministic line diff,
and the original image. It still dropped the plus and failed at 29/30 and 5/6.
The final rewrite is therefore removed from the accepted workflow.

## Accepted V10 Workflow

V10 is explicit and provider-scoped:

1. Qwen3.7 receives the unified board prompt plus a generic silent inventory of
   text-bearing regions, small standalone operators, exact identifiers, and
   texture exclusion. It returns the only prose/formula draft.
2. Two independent `qwen-vl-max` calls receive the original unified prompt with
   thinking disabled. They are untrusted visual-sign scouts.
3. Local deterministic code extracts only lines made entirely of a bounded
   sign alphabet. Scout prose can never enter the result.
4. A sign becomes quorum evidence only when both scouts report it with a
   matching previous or following normalized text anchor.
5. The merger first counts isolated sign tokens already present in the Qwen3.7
   base, including inline forms such as `+ Validation`. It inserts only a
   missing quorum occurrence and only at a matching anchor. Unmatched events
   are ignored.
6. There is no generative final review. The Qwen3.7 transcript stays
   byte-identical when no sign restoration is needed.

This is not handwriting routing. The same three-call workflow and merger apply
to every board fixture. It is not retry, fallback, or automatic provider
switching. It is activated only by explicit
`DashScopeSettings(standalone_sign_scout_model="qwen-vl-max")`; defaults remain
one Qwen3.7 call. Scout mode rejects nondefault `RecognitionPreferences` to
avoid ambiguous combinations.

Metadata records the primary model, scout model, scout count, primary/scout
thinking modes, exact provider-call count, and restored-sign count. A scout
failure reports `standalone_sign_scout_1` or `_2` and fails the whole request.
Any unsafe merge failure is typed and redacted. Only the final deterministic
Markdown reaches the existing atomic writer.

## Targeted Proof

The deterministic merger was applied to two independent Qwen3.7 handwriting
symbol-audit drafts using the same two independent VL scouts:

- Trial 1 already contained both plus signs. The merger restored zero signs,
  left the Markdown unchanged, and passed 30/30 recall, 35/37 precision, 6/6
  critical tokens, and 10/10 slots.
- Trial 2 missed one plus. The merger restored exactly one sign between
  `foreign gene` and `I:V` and passed 30/30 recall, 36/37 precision, 6/6
  critical tokens, and 10/10 slots.
- Two formula scouts produced no applicable standalone-sign restoration. The
  perfect Qwen3.7 formula draft remained byte-identical at 12/12 signatures,
  133/133 atoms, and 108/108 critical atoms.

Post-v8 exploratory API accounting before v10 implementation: 17 request
attempts, 15 complete inference outputs, and two pre-inference provider
rejections. This is separate from the 19 provider attempts already preserved
in the partial v8 live gate.

## Frozen V10 Contract

- Primary model: `qwen3.7-plus-2026-05-26`, thinking enabled.
- Scout model: `qwen-vl-max`, two independent calls, thinking disabled.
- Prompt: `board.v10`.
- Timeout: 180 seconds per provider call.
- Runner plan: 13 recognition invocations, exactly 39 provider calls, no SDK or
  runner retry.
- Manifest: 37,853 bytes, SHA-256
  `15a7018084cd1d53c82acbf260bb19095ccb29664cc357beaaaefd9044b8f971`.
- Exact isolated suite: 628 passed.

The fixture remains unchanged and the center plus remains required. Phase 1 is
NO-GO until a clean committed v10 attempt completes both full runs, final clean
packaging profiles pass, and the authoritative decision is updated.
