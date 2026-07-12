# Local OCR Implementation Checkpoint

Date: 2026-07-12.

Status: implementation, deterministic tests, maintained-engine test, and two
authorized screenshot probes pass. `image.ocr.rapidocr` remains experimental
until the committed clean-wheel and fresh-extra gates pass.

## Public Contract

Local OCR uses the existing direct facade:

```python
from ocrllm import Config, LocalOCRSettings, recognize

result = recognize("board.png", config=Config(image_mode="ocr"))
result = recognize(
    ("page-1.png", "page-2.jpg"),
    config=Config(
        image_mode="ocr",
        local_ocr=LocalOCRSettings(minimum_confidence=0.70),
    ),
)
```

`image_mode="vision"` remains the default and preserves the Phase 1 v17 path.
OCR mode constructs default immutable settings and rejects provider, API key,
model, DashScope, language-hint, LLM review/scout, and resume fields instead of
silently ignoring them. Output directory, overwrite, temporary directory, and
cancellation-before-each-image retain their existing meanings.

The frozen Phase 2 v1alpha1 command remains DashScope-only. This checkpoint does
not change its recognition request shape.

## Adapter Boundary

The maintained `rapidocr>=3.9,<4` package and `onnxruntime>=1.23,<2` are
available only through the `ocr` extra. The old installed
`rapidocr_onnxruntime==1.4.4` package was used only as an initial feasibility
probe and is not a dependency.

The adapter:

1. validates and snapshots PNG/JPEG inputs through the existing image boundary;
2. lazily imports RapidOCR only after explicit OCR selection;
3. initializes one engine per ordered request;
4. sets `Global.log_level=critical` and the explicit confidence threshold;
5. checks cancellation before engine initialization and before every image;
6. validates backend text/score sequences without retaining backend objects;
7. filters non-visible or low-confidence lines;
8. preserves per-image reading order and adds `## Image N` boundaries only for
   multi-image requests; and
9. returns normal `RecognitionResult`/atomic Markdown output with zero provider
   and network calls in metadata.

No source paths, OCR boxes, private text, backend exceptions, or model paths
enter result metadata or public errors.

## Error Taxonomy

```text
DEPENDENCY_MISSING   maintained optional OCR dependencies are absent
OCR_BACKEND_FAILED   import, initialization, or inference failed
OCR_RESULT_INVALID   backend result structure/text/scores are malformed
OCR_NO_TEXT          no visible line survives confidence filtering
```

Initialization and inference errors add only engine, phase, and zero-based
image index details. Backend exception messages are discarded. These errors do
not share provider retry semantics.

## Metadata And Honest Limit

Successful results report:

```text
recognition_mode
ocr_engine / ocr_engine_version
image_count
detected_line_count / retained_line_count / empty_image_count
minimum_confidence / mean_confidence
provider_call_count = 0
network_call_count = 0
```

Every result warns that local OCR extracts reading-order text lines but does not
reconstruct formula, table, handwriting, or layout semantics like the vision
workflow. The two modes are not split by content class: the caller chooses one
strategy for any image group.

## Real Offline Evidence

The fresh maintained profile used RapidOCR 3.9.1, ONNX Runtime 1.23.2, and
Pillow 12.3.0.

A generated ordered PNG/JPEG test passed with `requests` network access forced
to fail. Both expected ASCII texts were recognized, the public result reported
zero provider/network calls, and captured stdout/stderr were empty.

One ordered request over two user-authorized untracked Chinese/formula/table
screenshots also passed with network access forced to fail:

```text
input byte sizes            208,014 and 168,837
input dimensions            879x1114 and 922x1197
elapsed                     about 45.48 seconds
detected/retained lines      191 / 191
mean confidence             0.9553138743455502
Markdown UTF-8 bytes        3,307
Markdown SHA-256            a9ebeae0c0e0e87a172d3bb5219ed5865d344f7f527b0473a2ffe9cc5de2848a
selected prose tokens       8 / 8
provider/network calls      0 / 0
captured stdout/stderr       0 / 0 bytes
```

The private images and full OCR Markdown remain untracked and are not
redistributed. Token checks cover inexpensive text extraction only; they are not
a formula/table/layout accuracy score.

## Verification

- Local OCR/config/loader/capability/worker focused suite: `64 passed`.
- Real maintained RapidOCR generated-image test: `1 passed`.
- Full base suite: `870 passed, 1 skipped`.
- Phase 1 generated fixtures: byte-identical.
- `compileall`: passed.
- Ruff across `src` and `tests`: passed.
- Node syntax checks: passed.
- `git diff --check`: passed.

## Next Gate

Commit and push this checkpoint, then build from its Git archive. Prove the base
wheel/import budgets, install `ocrllm[ocr]` into a fresh target, rerun the real
generated-image and private screenshot probes from committed code, measure the
OCR profile, and only then graduate `image.ocr.rapidocr` from experimental to
available.
