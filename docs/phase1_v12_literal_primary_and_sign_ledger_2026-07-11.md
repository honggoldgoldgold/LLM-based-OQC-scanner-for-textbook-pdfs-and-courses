# Phase 1 V12 Literal Primary And Sign Ledger Record

Date: 2026-07-11.

Status: targeted live probes and offline gates pass; complete live gate pending.

## Decision

V11 proved that full-transcript scouts do not reliably create sign quorum and
that the Qwen3.7 primary can append invented structural descriptions around
otherwise plausible OCR. V12 changes the shape of both requests without
splitting handwriting from the unified board profile.

The primary prompt now says Markdown structure may organize only literally
visible source text. It explicitly forbids model-created region captions,
diagram descriptions, item numbering, shape names, positional prose, appended
explanatory sections, and invented `Diagram`/`Labels` prefixes.

Each Qwen-VL Max scout now returns only a strict ledger:

```text
SIGN | BEFORE | AFTER
```

`BEFORE` and `AFTER` are nearest literal visible fragments of at most five
words, or exact `NONE`. Scouts are told not to output headings, bullets, code
fences, captions, explanations, Markdown separators, texture, or other prose.

## Strict Parser Boundary

Production accepts only nonempty lines matching the exact three-field format.
The sign must be one exact allowed conventional operator, not a repeated
thematic break. Neighbor fields are length-bounded, pipe-free, at most five
words, and must normalize to an alphanumeric anchor unless they are exact
`NONE`. Both neighbors cannot be `NONE`.

Any extra prose, heading, fence, unsupported sign, malformed spacing, overlong
neighbor, empty anchor, too many events, or invalid type rejects the entire
ledger and fails the recognition. Only parsed sign/anchor records reach the
existing two-of-three quorum merger. Scout prose cannot enter result Markdown.

The evidence request contract records a SHA-256 and UTF-8 byte count for the
fixed scout prompt in addition to the primary prompt identity.

## Targeted Live Proof

Five targeted Beijing requests were made before implementation: two Qwen3.7
primaries and three Qwen-VL Max ledgers.

- Primary 1 passed at 30/30 recall, 36/37 precision, and 6/6 critical tokens.
- Primary 2 passed at 30/30 recall, 38/39 precision, 6/6 critical tokens, and
  10/10 critical slots.
- Neither primary appended invented diagram captions.
- All three scout ledgers were byte-identical and strict:

```text
+ | foreign gene | I:V
+ | Transformation | Validation
- | Validation | Selection
- | Selection | Screening
```

The two genuine plus signs therefore have three-of-three independent ledger
agreement with usable literal anchors. These temporary outputs are ignored
diagnostic material, not committed gate evidence.

## Frozen V12 Contract

- Prompt: `board.v12`.
- Primary: one `qwen3.7-plus-2026-05-26`, thinking enabled.
- Scouts: three `qwen-vl-max`, thinking disabled, strict ledgers, two-of-three
  quorum.
- Formula scorer: `labeled-latex-restricted.v6`.
- Timeout: 180 seconds per call.
- Plan: 13 recognitions and 52 provider calls; no retry.
- Evidence schema: `ocrllm.phase1-quality-evidence.v12`.
- Manifest: 37,853 bytes, SHA-256
  `e2813e006d4de8db3b4b2fe3ef99a1e658935d98290e2a1735d75d4e80a164f6`.
- Exact isolated suite: 661 passed.

Phase 1 remains NO-GO pending two complete passing live runs and clean package
profiles.
