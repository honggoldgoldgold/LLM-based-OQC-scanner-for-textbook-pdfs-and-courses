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
