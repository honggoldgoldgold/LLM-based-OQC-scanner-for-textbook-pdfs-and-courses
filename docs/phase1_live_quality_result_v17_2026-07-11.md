# Phase 1 V17 Live Quality Result

Date: 2026-07-11.

Status: complete provider execution; both full runs passed.

## Bound Contract

- Commit: `7f1fd98666b681b0e4a276cf89989fee0e4f54a6`
- Region: `cn-beijing`
- Prompt: `board.v17`
- Primary: one `qwen3.7-plus-2026-05-26`, thinking enabled
- Scouts: three independent `qwen3.7-plus-2026-05-26`, thinking enabled
- Scout prompt: primary-conditioned `board-sign-omission.v1`
- Plan: 13 recognitions and exactly 52 provider calls; no retry
- Formula dialect: `labeled-latex-restricted.v7`
- Manifest: 37,864 bytes, SHA-256
  `4ec1440f531e88492eb06795a29308256a5718c2748625ce2ad9b1230807e393`

The run started at `2026-07-11T23:33:50.775668Z` and finished at
`2026-07-12T00:27:38.816550Z`, about 53 minutes 48 seconds. All 13
recognitions and all 52 reported provider calls completed with no terminal
failure and no retry.

Preserve
`evidence/phase1/phase1-quality-v17-2026-07-11-cn-beijing.json`: 107,246
bytes, SHA-256
`6f0454d634dbe76f68f29c07a4c0ced4a047c080e46bb75dda2cb84ffca3a96b`.
Both full runs completed and passed.

## Run A

All six dispatches passed. The clean slide, projected slide, handwriting,
formula, table, and ordered slide-plus-formula request used zero restorations
and recorded zero scout abstentions.

## Run B

All six dispatches passed. The primary-conditioned scouts restored exactly one
missing handwriting sign with two-of-three agreement. The handwriting scorer
then passed, and no scout abstained. The clean slide, projected slide, formula,
table, and ordered slide-plus-formula request passed with zero restorations.

## What V17 Proved

The handwriting gap was a prompt/workflow omission, not a separate recognition
capability. The same model, `board` profile, provider adapter, primary prompt,
and structural guards serve every fixture class. Scouts receive the primary
transcript only as inert quoted context and return only source-visible missing
arithmetic or relation signs. They do not route by handwriting, fixture name,
or image class.

The two independent full runs cover both important outcomes:

1. When the primary already contains the source signs, the auxiliary path makes
   no change.
2. When the primary omits a small handwriting sign, two independent scouts can
   restore exactly that sign while formula, table, and ordered-image guards
   remain intact.

The evidence file was written atomically after each complete dispatch and again
at terminal completion. Its reported provider-call total matches the frozen
52-call plan. A post-run scan found neither the active environment credential
nor an `sk-...` token pattern.

The live quality gate is passed. Phase 1 changes from NO-GO to GO only after
the clean committed-wheel base, image, and image-plus-DashScope profiles also
pass and the required boundary documents are updated together.
