# Phase 1 V15 Thinking Scout And Allowlist Extraction Record

Date: 2026-07-11.

Status: targeted Beijing probes and all offline gates pass; complete live gate
pending.

## Decision

V14 proved that every structural sign-restoration guard works live and one full
run can pass. Its only remaining failure occurred when a primary omitted one
plus and two of three Qwen-VL Max scout responses abstained. Lowering quorum to
one would accept uncorroborated insertions. V15 instead changes the auxiliary
model role while preserving the same unified board profile, three-scout pool,
two-of-three quorum, and 52-call plan.

The primary and scouts now use the same pinned
`qwen3.7-plus-2026-05-26` model. They remain independent calls with different
tasks: the primary returns the complete transcript; each scout returns only an
allowlisted sign ledger. All four calls use thinking because live probes show
that non-thinking sign scouts are fast but miss the delicate plus.

This is not handwriting routing. Every dispatch receives the same primary and
three-scout workflow regardless of image class.

## Post-V14 Probe Accounting

Twenty-three Beijing diagnostic requests were made after the frozen v14 gate:

- 7 Qwen-VL Max handwriting scouts completed in 58.7 seconds. Four responses
  parsed, but two contained 15 and 38 mostly invented plus records. Three were
  malformed. Scaling this behavior was rejected.
- 5 thinking-enabled Qwen3.7 handwriting scouts completed in 410.8 seconds.
  All five contained both genuine plus records, including
  `+ | foreign gene | I:V`; all also listed unsupported visible punctuation,
  usually `/`, so the old whole-response parser rejected them.
- 3 thinking-enabled Qwen3.7 clean-slide scouts completed in 173.8 seconds.
  All reported the real `≥` relation. V14's source-equivalent representation
  count blocks duplication when the primary already contains it.
- 5 non-thinking Qwen3.7 handwriting scouts completed in 25.2 seconds. Only one
  found `foreign gene + I:V`; non-thinking mode was rejected despite its speed.
- 3 final allowlisted, thinking-enabled Qwen3.7 handwriting scouts completed in
  181.6 seconds. All three returned exactly the same two genuine plus records
  and no unsupported punctuation.

None of these calls is relabeled as gate evidence.

## Defensive Extraction Boundary

The final prompt explicitly restricts `SIGN` to the supported operator set and
forbids colon, slash, apostrophe, period, and comma records. Prompt compliance
is not trusted by itself.

`extract_supported_standalone_sign_events.py` processes at most 256 nonempty
response lines. It retains only lines that independently satisfy the existing
exact three-field parser and supported-sign allowlist. Unsupported punctuation,
headings, explanations, and malformed rows are discarded and cannot enter
Markdown. Exact whole-response `NONE` remains valid empty evidence. A response
with no supported exact row abstains as a whole. Exact duplicate records within
one scout are deduplicated before cross-scout clustering.

Extracted records still need agreement from two distinct scouts, matching
anchors in the primary, the source-equivalent occurrence budget, anchor-line
conflict exclusion, and table protection. Line extraction does not bypass any
v14 guard.

## Fixed Thinking Contract

`resolve_sign_scout_enable_thinking.py` makes model behavior explicit:

- `qwen-vl-max` scouts run with thinking disabled;
- pinned `qwen3.7-plus-2026-05-26` scouts run with thinking enabled;
- unpinned scout models have no contract and are rejected.

The public DashScope settings now allow the pinned Qwen3.7 snapshot as a scout,
including when it equals the primary model. Existing Qwen-VL Max scout
configuration remains supported for callers, but it is no longer the Phase 1
evidence baseline.

## Frozen V15 Contract

- Prompt: `board.v15` with the explicit sign allowlist.
- Primary: one `qwen3.7-plus-2026-05-26`, thinking enabled.
- Scouts: three independent `qwen3.7-plus-2026-05-26`, thinking enabled,
  allowlist extraction, two-of-three quorum.
- Formula scorer: `labeled-latex-restricted.v6`.
- Timeout: 180 seconds per call.
- Plan: 13 recognitions and exactly 52 Beijing provider calls; no retry.
- Evidence schema: `ocrllm.phase1-quality-evidence.v15`.
- Manifest: 37,864 bytes, SHA-256
  `9c5fe09635142c457c464d52f2c4bba8e78964f61e3c06cb4b786d8bf6bf3c11`.
- Focused workflow suite: 159 passed.
- Exact isolated repository suite: 696 passed.
- Generated fixtures are byte-identical; compileall, Ruff, diff, and conflict
  checks pass.

Phase 1 remains NO-GO pending a fresh complete live gate with two passing full
runs and clean package profiles.
