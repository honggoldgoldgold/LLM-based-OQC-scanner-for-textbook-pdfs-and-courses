# Phase 1 Exploratory Robustness: 2026-07-11

Status: diagnostic evidence only; not a GO gate.

This record covers API calls made after the immutable v2 gate under the user's
unrestricted API authorization. It records failures as well as successes. Raw
private screenshot content and responses are not committed.

## Call Inventory

Thirteen exploratory network requests were attempted: twelve returned provider
responses and one model request returned HTTP 403. All requests used the
confirmed Beijing-compatible endpoint and zero client retries.

| Calls | Candidate | Result |
|---:|---|---|
| 1 | `qwen3.7-plus-2026-05-26`, `board.v3`, original handwriting | Same seven handwriting quality failures as v2. |
| 1 | Original handwriting plus four deterministic enhanced crops | Same transcription and seven failures; overview dominated. |
| 1 | Four enhanced crops without overview | Rejected on a new down-arrow presentation and did not demonstrate a quality gain. Cropping rejected. |
| 4 | Four private dense optimization screenshots | Four complete responses; no provider error or truncation. |
| 2 | `qwen3.5-ocr` and `qwen-vl-ocr-latest`, chat API | Qwen3.5 returned; Qwen-VL-OCR was unavailable to the credential/endpoint with HTTP 403. |
| 1 | Qwen3.5-OCR repeat separating provider and scorer errors | Read `Enzymes` but wrapped the whole result in unsupported LaTeX and changed/missed other content. |
| 1 | Qwen3.5-OCR with a plain-text OCR-specific prompt | Read more micro-labels and `Enzymes`, but changed the ratio and other content; scorer rejected an unsupported visible symbol. |
| 1 | Qwen3.7 with thinking enabled | Slower and more verbose; retained `Sticky`/`Enzymens` errors and added micro-labels. Rejected. |
| 1 | Qwen3.5-OCR Responses `document_parsing` | Returned a signed temporary OSS image link instead of text-only recognition. Rejected for result-contract and secret-surface risk. |

## Private Screenshot Diagnostics

The local files are authorized for private testing and provider submission, not
redistribution. Only non-content identities and coverage summaries are recorded.

| Case | Source SHA-256 | Markdown bytes | Visible marker groups |
|---|---|---:|---:|
| Diet optimization | `0494d33c412f3efc42a6ec478580ca34a70a46384f888e80a58e4464cb1d7dbf` | 2,176 | 3/4 |
| Standard-form conversion | `b19b54ff5d8e92b4e32a2afd3467a5c8c48b548d800e65a8dced04db4933c2db` | 2,464 | 3/4 |
| First simplex pivot | `dd03e482d57368a90f749ed60ee2bedd7510d864d1feed4253e16144ba2518d2` | 3,169 | 4/4 |
| Second simplex pivot | `49201948d894393692b25d8ddcf1c6cf6bf80de317f1f3a875aeef0ded8d3800` | 2,480 | 4/4 |

All four returned `status="complete"` with `prompt_version="board.v3"`. These
checks prove transport and dense formula/table coverage only. They are not exact
recognition scores because the private sources have no frozen complete
transcription.

## Handwriting Ground-Truth Audit

Visual inspection found that the committed handwriting manifest omits the
clearly visible `R-DNA / Replasmid` label. The current prompt requires all
visible text, but the precision scorer penalizes this correct output as
unexpected, including its punctuation as unexpected critical units. A future
manifest version must add a complete source-derived annotation before another
comparable handwriting gate.

That omission does not explain all failures. Qwen3.7 repeatedly changed visible
lowercase `sticky` to `Sticky`, changed `Enzymes` to `Enzymens`, and capitalized
other handwritten labels. Qwen3.5-OCR fixed `Enzymes` but introduced different
ratio, symbol, layout, and extra-content errors. No tested single-model path met
the frozen handwriting gate.

## Security Incident Avoided

The Qwen3.5-OCR Responses document-parsing task returned Markdown containing a
temporary signed OSS URL with query credentials rather than text-only output.
It appeared only in transient console output and was not written to Git,
evidence, or a local result file. Never expose this response shape as a public
recognition result. A future Responses adapter would need an explicit text-only
contract, URL rejection/redaction, and dedicated tests before any use.

## Model Evidence

Alibaba's official documentation describes Qwen-OCR as optimized for documents,
tables, formulas, multilingual extraction, and handwritten content, while the
visual-model catalog recommends Qwen3.7 as the general flagship model:

- https://help.aliyun.com/en/model-studio/qwen-vl-ocr
- https://help.aliyun.com/en/model-studio/vision-model/

Local evidence does not justify adding either OCR model to the active allowlist:
one is inaccessible and Qwen3.5-OCR did not pass the handwriting contract.

## Architecture Decision Required

The current `board` profile bundles two materially different capabilities:
dense printed/formula/table recognition, which is viable, and photographed
handwriting, which no tested baseline passes. Do not hide this by lowering
thresholds or an unproven two-model ensemble.

Recommended path: split a printed/document image capability from an explicit
handwriting capability. Finish the printed/formula/table gate and keep
handwriting NO-GO until a provider and complete annotation pass independently.
The alternative is to keep the monolithic `board` gate, which blocks later
library phases despite strong printed-document evidence.
