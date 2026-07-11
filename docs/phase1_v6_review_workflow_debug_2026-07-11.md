# Phase 1 V6 Review Workflow Debug: 2026-07-11

Status: implementation and offline gates complete; clean live v6 gate pending.

V5 proved that one Qwen3.7 run can pass the unified board contract, but one of
two full runs hallucinated `111110` from hatch strokes. Subsequent single-pass
experiments also continued to miss the center `+` stochastically. Re-running
until lucky, weakening the critical gate, or splitting handwriting are rejected.

## Post-V5 Diagnostic Call Inventory

Twenty-eight targeted provider calls were invoked under the user's unrestricted
API authorization. Twenty-seven returned complete results and one glyph-count
attempt timed out. Every completed output was written through the library's
atomic Markdown writer under ignored `temp/` paths.

| Invoked | Experiment | Result |
|---:|---|---|
| 2 | V5 plus hatch/texture exclusion | No hatch hallucination; one pass, one missing `+`. |
| 2 | Overview plus broad lower detail | Both missed the center `+`; rejected. |
| 2 | Overview plus focused center detail | One pass, one duplication/hallucination failure; rejected. |
| 2 | Explicit per-glyph counting | One missing-`+` result, then one provider timeout; rejected. |
| 3 | Explicit seed `1234` | Three reproducible missing-`+` failures; rejected. |
| 3 | Seeds `42`, `3407`, `20260711` | All missed the same `+`; seed tuning rejected. |
| 6 | Three raw-readable draft-to-review trials | All three reviewed results passed; one repaired a failing draft. |
| 4 | Production workflow with JSON-string draft framing | Both reviewed results missed the `+`; JSON framing rejected as too opaque. |
| 4 | Production workflow with line-by-line quoted draft framing | Both reviewed results passed with two reported provider calls each. |

Alibaba's official Chat Completions documentation confirms that `seed` is a
supported reproducibility parameter, but the local screen proves an explicit
seed makes this visual omission consistently worse. No seed field is added:

- https://help.aliyun.com/en/model-studio/qwen-api-via-openai-chat-completions

## Architecture Decision

One `Config` still describes one provider/model workflow. The new immutable
`RecognitionPreferences` holds quality-versus-cost choices separately from API
settings:

```python
Config(
    provider="dashscope",
    dashscope=DashScopeSettings(...),
    preferences=RecognitionPreferences(review_passes=1),
)
```

`review_passes=0` remains the default and makes one provider call.
`review_passes=1` makes a second call to the same resolved provider and model,
with the original images plus the first response framed as a fallible quoted
checklist. Values outside 0/1 and subclasses fail closed. This is not retry,
fallback, provider switching, or best-of-N selection.

Only the reviewed Markdown can become a result or atomic output. A review
failure fails the recognition request; the draft is never returned as a silent
fallback. Metadata records `review_passes` and `provider_call_count`. The draft
prompt prefixes every draft line with `>` and explicitly treats it as untrusted
data, so delimiter-like or instruction-like text remains quoted rather than
becoming review instructions.

Provider invocation logic moved to `call_vision_provider.py`; orchestration
remains in `recognize_images.py`, and prompt construction lives in
`build_board_review_prompt.py`. Each filename has one recoverable responsibility.

## V6 Evidence Contract

- Prompt: `board.v6`, including generic hatch/fill/texture exclusion.
- Scorer dialect: unchanged `labeled-latex-restricted.v5`.
- Evidence schema: `ocrllm.phase1-quality-evidence.v6`.
- Review passes: 1.
- Plan: 13 library recognition invocations and 26 confirmed provider calls.
- Manifest: 37,685 bytes, SHA-256
  `c058a68b4a17d1ed13c74bd31429269fc4287539afeb23e20c8dfb0be6f50a27`.

The runner validates `review_passes=1`, `provider_call_count=2` on every success,
and requires 26 reported provider calls before GO. Its confirmation argument is
therefore 26, while the immutable dispatch order remains one smoke plus two
six-dispatch runs.

## Verification

```text
599 passed
Phase 1 generated fixtures are byte-identical.
compileall passed
Ruff changed-file checks passed
git diff --check passed
```

The two actual production quoted-review probes each scored 30/30 required
recall, 6/6 critical tokens, zero unexpected critical tokens, and passing
precision. Their reviewed outputs are frozen as scorer regressions; temporary
provider output files are not committed.

## Remaining Gate

Commit and push v6, run the strict no-network preflight from that full commit,
then execute a new 13-recognition/26-provider-call evidence path. Phase 1 stays
NO-GO until both complete runs pass. Provider failures remain terminal; review
does not authorize hidden retry.
