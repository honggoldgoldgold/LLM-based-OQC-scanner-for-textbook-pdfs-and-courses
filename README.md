# OCRLLM

Read this first if you are returning to the project after losing context:
`START_HERE.md`.

Then read `MIGRATION_STATUS.md` for the migration history and next steps.
Read `docs/ocrllm_library_go_no_go.md` before implementing any new library
feature; it is the authoritative execution decision.

OCRLLM is an importable Python library under active staged development. Other
projects import it as `ocrllm`. The previous application code was moved into
`legacy_app/` and should be treated as a reference implementation, not as the
dependency surface for new projects.

## Active Direction

The active package is `src/ocrllm`.

Phase 0 contract honesty is GO. The current phase is **Phase 1 -- real
board/image**.

The current verified contract:

- Valid `.png`, `.jpg`, and `.jpeg` files are decoded before provider dispatch.
- The synchronous injected provider receives request-scoped validated snapshots
  isolated from later caller-path changes, not the caller's source paths.
- Provider failures and invalid output become typed, redacted public errors.
- Results use canonical `source_type="image"` and `profile="board"`.
- File output is optional. `output_dir=None` means in-memory results only.
- Requested Markdown output uses deterministic collision handling and atomic
  publication.
- Pillow is installed only through `ocrllm[image]` and is imported lazily.
- The built-in DashScope adapter is installed only through
  `ocrllm[dashscope]`; plain `import ocrllm` imports neither `openai` nor
  transitive `httpx`.

Phase 1 now contains one lazy DashScope vision adapter with offline boundary
tests. It requires immutable `DashScopeSettings` with an explicit region and
OpenAI-compatible endpoint, accepts only `qwen3.7-plus` or the default pinned
`qwen3.7-plus-2026-05-26`, constructs `OpenAI(max_retries=0)`, and sends ordered
Base64 data URLs rather than local paths.

Offline checkpoint `e328253` committed the licensed five-class corpus,
deterministic generators, exact scorers, and integrated manifest-authenticated
live-scoring gate. The current versioned `board.v3` manifest is `35,400` bytes
with SHA-256
`43c548fdfda1d114b6851def2ce05284cc213bd3478e1e0eea9faa6242a27966`.
Its 20 artifacts include 5 images and total `17,914,515` bytes, leaving
`8,299,885` bytes under the 25 MiB corpus limit. The pinned full suite passed
`574` tests; regenerated fixtures were byte-identical and `compileall` passed.
The boundary suite now hits exact one-below, at, and one-above values for every
per-source byte, decoded-pixel, group-count, aggregate-source-byte, and
aggregate-pixel cap; every rejecting integration case proves zero provider
calls.

Runner checkpoint `fb23d1e` is committed. Its offline fake/evidence tests and a
direct live-preflight check pass without a provider/API call. The public live
entrypoint closes over real dependencies and exposes no injection parameters;
the private fake path labels its output `simulated` and cannot set the live gate
to passed. The frozen zero-retry plan is exactly one clean-slide smoke, six
dispatches in run A, and six independently dispatched entries in run B.

The first fixed Beijing gate completed all 13 zero-retry calls on 2026-07-11.
Both full runs completed, but neither passed; Phase 1 remains NO-GO. There were
no provider request failures. The live record separates a real handwriting
quality miss from a deterministic mismatch between reasonable Qwen
Markdown/LaTeX presentation variants and the frozen v1 scorer grammar. The
evidence remains unchanged. The later v2 gate also completed all 13 calls and
failed on undeclared relation typography and line-leading diagram arrows. The
offline `board.v3` correction is implemented and tested: it normalizes only
those content-preserving forms and leaves both handwriting content failures
intact. See
`docs/phase1_live_quality_result_2026-07-11.md`. The local user screenshots
under `docs/` remain untracked, supplemental, and non-redistributable; they are
not part of pass/fail evidence.

Provider cost/reliability assumptions are recorded in
`docs/provider_cost_and_reliability_policy.md`. The complete checkpoint,
parallel-review, and atomic-writer history is in
`docs/phase1_implementation_record.md`.

Pushed packaging hotfix `3414f47` renamed `resolve_dashscope_api_key.py` /
`resolve_dashscope_api_key` to `resolve_dashscope_credential.py` /
`resolve_dashscope_credential`. The old legitimate filename matched the
existing `*_api_key*` secret-ignore pattern; the rename fixed that defect
without weakening secret protection. A clean Git-archive build from the hotfix
produced a `50,094`-byte wheel and passed an isolated explicit-key resolver
round-trip without a provider call.

The active library also has no local OCR mode, API-key pools, automatic retries
or model fallback, resume/checkpoint support, PDF recognition, audio
recognition, or video recognition. Those features must enter through their own
approved phases rather than through the injected-provider scaffold.

Active PDF work will use PDFium through `pypdfium2`. PyMuPDF/`fitz` is
legacy-only and must not enter `src/ocrllm`. HarmonyOS/ArkTS compatibility is
deferred and is not an active claim.

The old Rust/PyO3 rewrite plan in `Architecture.md` is suspended and kept only
as a future reference.

## Current Public API

Install the current image and provider extras together for the built-in adapter:

```bash
pip install "ocrllm[image,dashscope]"
```

The built-in call shape is explicit about its regional endpoint:

```python
from ocrllm import Config, DashScopeSettings, recognize


settings = DashScopeSettings(
    region="ap-southeast-1",
    base_url=(
        "https://your-workspace-id.ap-southeast-1.maas.aliyuncs.com/"
        "compatible-mode/v1"
    ),
)
result = recognize(
    "board.jpg",
    config=Config(provider="dashscope", dashscope=settings),
)
print(result.markdown)
```

Supply the key through `Config.api_key` or `DASHSCOPE_API_KEY`; Coding Plan
`sk-sp-` credentials are not accepted. Replace the example workspace ID with a
real endpoint in the same region. Only the floating alias `qwen3.7-plus` and the
default pinned snapshot `qwen3.7-plus-2026-05-26` are accepted in Phase 1.

The injected-provider contract remains available to host applications that own
their clients and network policy. The library validates and snapshots the image
before calling the provider; this offline example is contract evidence, not
recognition-quality evidence.

```python
from ocrllm import Config, recognize


class Provider:
    def recognize_images(self, image_paths, *, prompt, config):
        return "# Recognized board\n"


result = recognize("board.jpg", config=Config(provider=Provider()))
print(result.markdown)
print(result.source_type)  # image
print(result.profile)      # board
```

Set `output_dir` to request a Markdown file. Without it, recognition stays
in-memory. Image resume is not implemented.

## Repository Map

```text
START_HERE.md                         One-screen new/old/suspended repo map.
AGENTS.md                             Repo-level boundary instructions.
src/ocrllm/                           Active importable library package.
src/ocrllm/README_ACTIVE_LIBRARY.md   Local active-library boundary.
src/ocrllm/AGENTS.md                  Local active-library agent rules.
tests/                                Active library contract and licensed
                                      Phase 1 quality-gate tests.
legacy_app/                           Old GUI/CLI/FastAPI application.
legacy_app/README_LEGACY.md           Local legacy-app boundary.
legacy_app/AGENTS.md                  Local legacy-app agent rules.
docs/                                 Active migration decisions.
docs/ocrllm_library_go_no_go.md       Authoritative execution decision.
docs/phase1_live_quality_result_2026-07-11.md
                                      First Beijing live-gate result.
Architecture.md                       Suspended future architecture reference.
output/, temp/, ocrllm_social_e2e/    Runtime artifacts, not source.
```

## Legacy Runtime Notes

The old GUI, Codex video mode, Filetrans audio mode, and Bilibili/social-long
workflow are read-only behavior references under `legacy_app/` for this
migration. Historical runtime incident notes live in:

```text
docs/legacy_bilibili_social_long_debug_record.md
docs/legacy_filetrans_codex_debug_record.md
```

For a separately authorized legacy-maintenance task, use the Bilibili record
first when touching multi-part course downloads, comment/danmaku capture,
`social_long --parts`, social URL input, or resume behavior. It is not an
active-library phase gate.

The 2026-07-06 robustness record reported a clean supervised Bilibili CS231n
course run with the following output. Treat this as historical legacy evidence,
not as a currently revalidated active-library test:

```text
33 part directories
33 downloaded MP4 files
33 *_板书识别.md files
33 *_录音识别.md files
0 FileTrans task sidecars
bilibili_social_context.md with shared comments, resource links, and per-part danmaku
```

For any completed legacy course/video folder, the expected per-part recognition
artifacts are exactly these two Markdown files:

```text
*_板书识别.md
*_录音识别.md
```

Known dirty markers include Codex batch/frame placeholders, `Reading additional
input from stdin`, `[WinError 10061]`, embedded Codex diagnostic dumps, or a
missing board/audio Markdown after the job has completed. These checks belong
to the legacy workflow; they are not part of the public `ocrllm` library API.

The historical Bilibili course command is documented in
`docs/legacy_bilibili_social_long_debug_record.md`. It is reference evidence,
not an active-library verification command:

```powershell
$env:PYTHONPATH='legacy_app'
D:\Anaconda\envs\OCRLLM\python.exe -m OCRLLM.cli social_long <bilibili-url> `
  --parts 1-33 --resume -o output\bilibili_cs231n_full
```

## Rules For New Work

- New projects must import only from `ocrllm`, never from `legacy_app`.
- Do not port a legacy module wholesale. Extract one tested vertical slice at a
  time.
- Do not make GUI, FastAPI, social download, or heavyweight media dependencies
  import on `import ocrllm`.
- Do not make package-relative output directories the default.
- Keep the public API boring and stable before revisiting Rust internals.
- Use PDFium through `pypdfium2` for active PDF work; do not port PyMuPDF.
- Follow the phase gates in `docs/ocrllm_library_go_no_go.md`; code existence,
  mocks, and historical output are not enough to mark a feature supported.
- Do not start HarmonyOS/ArkTS work without a new explicit decision.

## Verification

```powershell
uv run --no-project --isolated --with 'Pillow==12.3.0' `
  --with 'pytest>=8,<10' --with 'openai>=2.30,<3' `
  --python 'D:\Anaconda\envs\OCRLLM\python.exe' `
  python -m pytest -q -p no:cacheprovider
uv run --no-project --isolated --with 'Pillow==12.3.0' `
  --python 'D:\Anaconda\envs\OCRLLM\python.exe' `
  python -m tests.quality.generators.generate_phase1_fixtures --check
& 'D:\Anaconda\envs\OCRLLM\python.exe' -m compileall -q src tests
```

These are the pinned offline checkpoint checks. The clean Git-archive wheel
build, isolated install, outside-repo import, and heavy-module guard are in
`docs/ocrllm_library_go_no_go.md`.
