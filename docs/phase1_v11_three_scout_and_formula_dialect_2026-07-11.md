# Phase 1 V11 Three-Scout And Formula-Dialect Record

Date: 2026-07-11.

Status: offline gates complete; clean live v11 evidence pending.

## Changes From V10

V10 completed all 39 calls and one full run passed, but exposed three issues:

1. Two sign scouts produced no usable quorum for one handwriting run, which
   left the genuine standalone plus missing.
2. The formula scorer rejected source-equivalent `\text{P}` and `\text{E}`
   LaTeX even though all source atoms were correct.
3. The sign merger treated a Markdown `---` thematic break as source content.

V11 fixes only those verified problems. It does not split handwriting from
boards, change fixture truth, relax critical thresholds, add retry, or perform
a generative final rewrite.

## Two-Of-Three Sign Quorum

Scout mode now makes three independent `qwen-vl-max` calls with thinking
disabled. A standalone sign needs agreement from at least two scouts at a
matching previous or following normalized text anchor. Events are clustered
across distinct scout calls, so one scout cannot vote twice. Primary Markdown
still supplies all prose and formulas.

The parser explicitly excludes repeated hyphen or equals lines of length three
or greater. Thus Markdown thematic breaks such as `---` and `===` cannot become
sign events. A regression test supplies the same separator from all three
scouts and proves the base remains byte-identical with zero restoration.

The merger remains bounded to eight scouts and 256 quorum events, although the
public v11 workflow fixes exactly three scouts and a minimum agreement of two.
Invalid tuple types, empty scouts, boolean/integer quorum confusion, unmatched
anchors, nonquorum signs, and inline sign counting are covered offline.

## Formula Dialect V6

The new scorer dialect unwraps `\text{X}` only when all of these are true:

- the line has an exact `F01`-style label;
- the formula uses one complete `$...$` wrapper;
- the `\text{}` payload is exactly one ASCII letter.

Ordinary prose is unchanged. Empty, numeric, multi-letter, whitespace-bearing,
nested-command, malformed-label, and missing-wrapper forms remain visible to
the strict parser and are rejected. The preserved v10 Run A formula now scores
12/12 signatures, 133/133 atom precision, and 108/108 critical atoms without
changing its raw evidence.

## Frozen Contract

- Prompt: `board.v11`.
- Primary: `qwen3.7-plus-2026-05-26`, thinking enabled.
- Scouts: three `qwen-vl-max`, thinking disabled, two-of-three quorum.
- Timeout: 180 seconds per call.
- Plan: 13 recognitions and exactly 52 provider calls; no retry.
- Scorer: `labeled-latex-restricted.v6`.
- Evidence schema: `ocrllm.phase1-quality-evidence.v11`.
- Manifest: 37,853 bytes, SHA-256
  `3b5c5392b1e10ed40261ac08dc5fbf692f0b451c6c13c4c71a44b710f28ec86b`.

## Verification

```text
647 passed
Ruff changed-file check passed
```

Before live dispatch also require byte-identical fixture generation,
`compileall`, `git diff --check`, signed-URL/credential audits, a clean relevant
tree, pushed commit identity, exact repository import origins, and a nonexistent
v11 evidence path. Phase 1 remains NO-GO.
