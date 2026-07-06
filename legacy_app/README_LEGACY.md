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
- Keep public APIs in `src/ocrllm`.
- Add tests against fake providers before wiring real providers.
- Avoid dragging GUI, FastAPI, social download, or package-relative path
  behavior into the new library.

## Maintained Compatibility Workflow: Social Long Video

The legacy social-long processor is still the active compatibility path for
multi-part Bilibili courses. It is intentionally not a new public library API.

Read the detailed robustness record before changing this path:

```text
docs/legacy_bilibili_social_long_debug_record.md
```

Run it through the legacy CLI:

```powershell
$env:PYTHONPATH='legacy_app'
D:\Anaconda\envs\OCRLLM\python.exe -m OCRLLM.cli social_long <bilibili-url> `
  --parts 1-33 --resume -o output\bilibili_cs231n_full
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
- Any requested part download failure fails the run instead of silently
  returning a partial course.
- Bilibili XML danmaku failures fall back to the segmented protobuf API.
- Comments are captured once from the shared course comment zone; danmaku is
  captured per part.
- Resume reuses downloads, video phase artifacts, and saved FileTrans task IDs.
- The social tab accepts free-form text and Markdown-style pasted URLs.

The verified CS231n output had 33 part directories, 33 MP4 files, 33 board
Markdown files, 33 audio Markdown files, no FileTrans sidecars, and a
`bilibili_social_context.md` file with the course resource link plus per-part
danmaku.

## Codex Video Mode Robustness

Codex video mode is maintained here as legacy GUI/CLI behavior. It is not a
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
