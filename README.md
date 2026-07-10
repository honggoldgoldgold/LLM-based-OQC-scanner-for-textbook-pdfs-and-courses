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

Phase 1 now adds one lazy DashScope vision adapter and a committed, reproducible
quality corpus/scorer with real-provider evidence. There is no built-in real
provider yet, so Phase 0 GO does not advertise board/image recognition as an
available capability.

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

This example shows the current synchronous injected-provider contract. The
library validates and snapshots the image before calling the provider. The
provider shown here is still caller-supplied; it is not the future built-in
DashScope adapter or recognition-quality evidence.

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
