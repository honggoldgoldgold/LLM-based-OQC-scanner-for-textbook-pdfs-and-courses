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
Base64 data URLs rather than local paths. This is an experimental implementation,
not recognition-quality evidence. Phase 1 remains NO-GO until the committed,
licensed five-class corpus/scorer, live smoke, two independent full-corpus live
runs, and final clean-profile gate all pass. The local user screenshots are
supplemental and non-redistributable; they do not replace that corpus.

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
tests/                                Active library import-contract tests.
legacy_app/                           Old GUI/CLI/FastAPI application.
legacy_app/README_LEGACY.md           Local legacy-app boundary.
legacy_app/AGENTS.md                  Local legacy-app agent rules.
docs/                                 Active migration decisions.
docs/ocrllm_library_go_no_go.md       Authoritative execution decision.
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

```bash
pip install -e .
python -c "import ocrllm; print(ocrllm.__version__)"
pytest
```

This is the short local check. The required temporary-wheel install,
outside-repo import, and heavy-module guard are in
`docs/ocrllm_library_go_no_go.md`.
