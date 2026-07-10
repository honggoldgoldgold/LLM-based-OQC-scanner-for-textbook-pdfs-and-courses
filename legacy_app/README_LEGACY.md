# Legacy App Notice

This folder contains the old OCRLLM application code.

It is preserved for reference, comparison, and gradual porting. It is not the
active library package and should not be imported by new downstream projects.

Read `legacy_app/AGENTS.md` before making changes in this directory.

## Boundary Summary

```text
legacy_app/OCRLLM/     Old application package.
legacy_app/tests/      Old application tests.
legacy_app/docs/       Old application docs.
legacy_app/launch_gui.bat
                       Current launcher for the old GUI compatibility app.
```

Use the root package instead:

```python
import ocrllm
```

Do not use this as a new dependency boundary:

```python
import legacy_app.OCRLLM
```

When porting from this folder:

- Port one vertical slice at a time.
- Follow `docs/ocrllm_library_go_no_go.md`; migrate proven behavior, not legacy
  classes or file structure.
- Keep public APIs in `src/ocrllm`.
- Add tests against fake providers before wiring real providers.
- Avoid dragging GUI, FastAPI, social download, or package-relative path
  behavior into the new library.
- Do not port the PyMuPDF/`fitz` renderer. The active PDF implementation must be
  rewritten against PDFium through `pypdfium2`.
- Active-library trials must not modify legacy code or legacy tests. Create new
  fixtures and contract tests under root `tests/`; read legacy files and outputs
  only as behavior evidence.

## Historical Compatibility Workflow: Social Long Video

The legacy social-long processor records the prior compatibility path for
multi-part Bilibili and YouTube course playlists. For the active-library
migration it is read-only reference code, not a test surface or public API.

For a separately authorized legacy-maintenance task, read the detailed
robustness records before changing this path:

```text
docs/legacy_bilibili_social_long_debug_record.md
docs/legacy_youtube_playlist_social_long_workflow.md
```

The historical Bilibili command was:

```powershell
$env:PYTHONPATH='legacy_app'
D:\Anaconda\envs\OCRLLM\python.exe -m OCRLLM.cli social_long <bilibili-url> `
  --parts 1-33 --resume -o output\bilibili_cs231n_full
```

The historical YouTube command used the same shape with the playlist URL and
selected playlist item range:

```powershell
$env:PYTHONPATH='legacy_app'
D:\Anaconda\envs\OCRLLM\python.exe -m OCRLLM.cli social_long <youtube-playlist-url> `
  --parts 1-97 --resume -o output\youtube_modern_robotics_full
```

For each selected part, the expected recognition output is exactly:

```text
*_板书识别.md
*_录音识别.md
```

Shared Bilibili course context is written to `bilibili_social_context.md`,
including comments, resource links, and per-part danmaku. The `--resume` path
reuses downloaded MP4 files, completed video phases, and saved DashScope
FileTrans task IDs.

Important behavior fixed during the 2026-07-06 Bilibili CS231n run:

- Multi-part Bilibili links route to `social_long`.
- `--parts` supports lists and ranges such as `1,3,5-8`.
- YouTube `--parts` maps to yt-dlp `playlist_items`.
- Any requested part download failure fails the run instead of silently
  returning a partial course.
- Bilibili XML danmaku failures fall back to the segmented protobuf API.
- Comments are captured once from the shared course comment zone; danmaku is
  captured per part.
- Resume reuses downloads, video phase artifacts, and saved FileTrans task IDs.
- The social tab accepts free-form text and Markdown-style pasted URLs.
- In Codex social-long mode, OCRLLM caps the effective video frame batch size
  at 1 for stable per-frame markers.

The 2026-07-06 run record reported 33 part directories, 33 MP4 files, 33 board
Markdown files, 33 audio Markdown files, no FileTrans sidecars, and a
`bilibili_social_context.md` file with the course resource link plus per-part
danmaku. This is historical compatibility evidence, not a currently rerun
active-library gate.

## Codex Video Mode Robustness

Codex video mode is preserved here as legacy GUI/CLI behavior. It is not a
public `ocrllm` library boundary.

The current expected clean output for each completed course/video folder is:

```text
*_板书识别.md
*_录音识别.md
```

A Codex-mode board result is dirty and should be rerun only when there is
concrete evidence, such as:

- Codex batch/frame failure placeholder comments.
- `Reading additional input from stdin`.
- `[WinError 10061]`.
- Embedded Codex prompt or diagnostic dumps.
- Missing board/audio Markdown after the job has completed.

Operational rules:

- Do not stop a live recognition job only because it is slow or because a blank
  Windows console appears.
- Restart the legacy GUI after changing Codex/Filetrans subprocess code so new
  workers load the patched code.
- Use board-only reruns for dirty board Markdown:

  ```powershell
  $env:PYTHONPATH='legacy_app'
  D:\Anaconda\envs\OCRLLM\python.exe -m OCRLLM.cli video <video.mp4> `
    --phases 2 3 4 --resume -o <existing-output-dir>
  ```

- Board-only reruns now preserve existing Phase 5 audio transcripts. Older code
  invalidated transcripts during `--phases 2 3 4`; see
  `docs/legacy_filetrans_codex_debug_record.md`.

Focused regression check:

```powershell
$env:PYTHONPATH='legacy_app'
$env:QT_QPA_PLATFORM='offscreen'
D:\Anaconda\envs\OCRLLM\python.exe -m pytest `
  legacy_app\tests\test_resume_chain.py `
  legacy_app\tests\test_codex_vision.py `
  legacy_app\tests\test_failure_propagation.py `
  legacy_app\tests\test_audio_wait_result.py -q
```
