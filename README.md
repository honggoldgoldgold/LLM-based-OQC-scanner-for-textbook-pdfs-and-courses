# OCRLLM

Read this first if you are returning to the project after losing context:
`START_HERE.md`.

Then read `MIGRATION_STATUS.md` for the migration history and next steps.
Read `docs/ocrllm_library_go_no_go.md` before implementing any new library
feature; it is the authoritative execution decision.

OCRLLM is now being extracted into a Python library that other projects can
import as `ocrllm`. The previous application code was moved into
`legacy_app/` and should be treated as a reference implementation, not as the
dependency surface for new projects.

## Active Direction

The active package is `src/ocrllm`.

The active goal is small and concrete:

- Make the current contract honest: invalid or missing images and empty
  provider responses must fail before they can look successful.
- Complete one real board/image path with a lazy provider adapter and real
  fixtures.
- Establish a versioned JSON-safe contract, then prove a one-job JSONL worker
  for Electron.
- Add PDF, audio, and video only as separately gated vertical slices.
- Keep file output optional. `output_dir=None` means in-memory results only.

Active PDF work will use PDFium through `pypdfium2`. PyMuPDF/`fitz` is
legacy-only and must not enter `src/ocrllm`. HarmonyOS/ArkTS compatibility is
deferred and is not an active claim.

The old Rust/PyO3 rewrite plan in `Architecture.md` is suspended and kept only
as a future reference.

## Current Public API

This example shows the current injected-provider scaffold. It is useful for
contract tests but is not evidence of validated image support; the current
implementation can still accept invalid paths or empty provider output.

```python
from ocrllm import Config, recognize


class Provider:
    def recognize_images(self, image_paths, *, prompt, config):
        return "# Recognized board\n"


result = recognize("board.jpg", config=Config(provider=Provider()))
print(result.markdown)
```

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
