# Legacy Bilibili Social-Long Robustness Record

Status: legacy application recovery note.

Scope:

- Active code path: `legacy_app/`.
- New importable library path `src/ocrllm/` was not involved.
- This records the 2026-07-06 supervised Bilibili multi-part course run and the
  fixes made while the run exposed real failures.
- Do not record cookies, API keys, or private Bilibili account state in this
  file.

## Course Under Test

Public course URL:

```text
https://www.bilibili.com/video/BV1nJ411z7fe?vd_source=d62783f4d1bd04042e6f22d2f3964cf4&p=33&spm_id_from=333.788.videopod.episodes
```

Observed Bilibili metadata:

```text
Title: 【公开课】最新斯坦福李飞飞cs231n计算机视觉课程【附中文字幕】
BVID: BV1nJ411z7fe
AID: 77752864
Parts: 33
Shared comment zone: yes
Observed comments: included https://github.com/Divsigma/Courses
Observed P33 cid: 133014498
Observed P33 duration: about 9608 seconds
```

The course has one shared Bilibili comment zone even though it has 33 parts.
The comments can contain course resources and assignments, so comments are part
of the expected captured course context, not optional debug output.

## Final Reusable Workflow

Run from the repository root:

```powershell
$env:PYTHONPATH='legacy_app'
$env:PYTHONIOENCODING='utf-8'
D:\Anaconda\envs\OCRLLM\python.exe -m OCRLLM.cli social_long `
  "https://www.bilibili.com/video/BV1nJ411z7fe?vd_source=d62783f4d1bd04042e6f22d2f3964cf4&p=33&spm_id_from=333.788.videopod.episodes" `
  --parts 1-33 --resume -o output\bilibili_cs231n_full
```

Use this same command to resume after interruption. The intended pathway is the
same one OCRLLM uses internally:

1. Probe Bilibili through the legacy social downloader.
2. Classify multi-part Bilibili videos as `social_long`, even when individual
   parts are short.
3. Download or reuse the selected part MP4s under `_downloads`.
4. Capture shared comments once and per-part danmaku separately.
5. Write shared course context to `bilibili_social_context.md`.
6. For each selected part, run the normal video pipeline.
7. Produce exactly one board Markdown and exactly one audio Markdown per part.
8. Reuse completed downloads, completed video phases, and in-flight FileTrans
   task IDs on later `--resume` runs.

## Output Contract

For every selected part directory:

```text
*_板书识别.md
*_录音识别.md
```

There must not be a third per-part `*_识别.md` compatibility output pretending
to be the final result.

Shared Bilibili context belongs here:

```text
output\bilibili_cs231n_full\bilibili_social_context.md
```

That file should include:

- Platform, BVID, AID, and part count.
- Resource links extracted from shared comments.
- Shared comments.
- Per-part danmaku sections.

## Problems Found Halfway And Fixes

### 1. Multi-part Bilibili Needed Long-Course Routing

Problem:

- The classifier could treat a Bilibili page as a short video when looking only
  at duration-style metadata.
- A parted course needs playlist/course handling, not short-video handling.

Fix:

- `legacy_app/OCRLLM/processors/social/platform_router.py` treats Bilibili
  metadata with multiple `parts` or `total_parts > 1` as a long playlist.
- `legacy_app/OCRLLM/cli.py` exposes `social_long --parts`, with range parsing
  such as `1,3,5-8`.

Regression coverage:

- `legacy_app/tests/test_social_long_bilibili_course.py`
  - `test_bilibili_parts_route_as_long_playlist`
  - `test_cli_part_indices_support_ranges`

### 2. Partial Download Success Was Not Acceptable

Problem:

- A multi-part run can appear useful even when one part failed to download.
- For this task, partial success is failure because the success criterion is
  exactly two recognition Markdown files for every selected part.

Fix:

- `legacy_app/OCRLLM/processors/social/downloader.py` accumulates per-part
  download failures and raises a hard `RuntimeError` if any requested part
  fails.
- Existing non-empty MP4 files are reused on resume.

Regression coverage:

- `test_bilibili_download_fails_when_any_requested_part_fails`

### 3. Bilibili Stream Downloads Needed Real Resume Behavior

Problem:

- Long DASH/FLV downloads can be interrupted.
- Retrying from the beginning wastes time and can make a 33-part run fragile.

Fix:

- `legacy_app/OCRLLM/processors/social/bilibili_api.py` downloads via system
  `curl` when available.
- Downloads use `.part` files, retry flags, Bilibili referer/user-agent
  headers, and range resume.
- If a CDN rejects range resume, the partial is deleted and the part is
  restarted cleanly.
- The curl path falls back to session streaming if needed.

Operational note:

- `_downloads` is intentionally reusable runtime state. Do not delete it before
  a resume unless you intentionally want to redownload the course.

### 4. Comments And Danmaku Needed Different Capture Rules

Problem:

- Bilibili multi-part videos have one shared comment zone, but danmaku is
  attached to part CIDs.
- Capturing comments per part would duplicate shared resource comments.
- Capturing only the first part's danmaku would miss per-lecture context.

Fix:

- Comments are fetched once using the video AID.
- Danmaku is fetched per target part CID.
- `DownloadPart` carries `danmaku_texts`.
- `DownloadResult` still exposes flattened unique danmaku for short-video
  compatibility.
- `SocialLongVideoProcessor` writes comments/resource links/danmaku to
  `bilibili_social_context.md`.

Regression coverage:

- `test_bilibili_download_captures_danmaku_per_part`

### 5. Bilibili XML Danmaku Endpoint Hit Risk Control

Problem observed during the real run:

- `https://api.bilibili.com/x/v1/dm/list.so?oid=<cid>` returned a Bilibili 412
  risk-control HTML page in this environment.
- Strict XML parsing logged failures such as `mismatched tag`.
- The first context file therefore contained `No danmaku captured`.

Fix:

- `fetch_danmaku()` first tries the old XML endpoint.
- If strict XML fails, it tries a lenient `<d ...>...</d>` extractor.
- If the payload looks like Bilibili 412/risk-control HTML, it falls back to
  `https://api.bilibili.com/x/v2/dm/web/seg.so`.
- The segment API returns protobuf bytes; `bilibili_api.py` decodes only the
  needed fields locally:
  - field 2: progress milliseconds
  - field 7: danmaku content

Evidence from the successful context refresh:

```text
P33 cid=133014498 fetched 74 danmaku items through the fallback path.
```

Regression coverage:

- `test_fetch_danmaku_keeps_items_from_malformed_xml`
- `test_fetch_danmaku_falls_back_to_segment_api_for_bilibili_412`

### 6. Recognition Needed A Strict Two-Markdown Contract

Problem:

- The old social-long shape could blur final recognition output into a single
  compatibility Markdown file.
- For course study, board recognition and audio recognition must be separate
  artifacts so each lecture has two readable notes.

Fix:

- `legacy_app/OCRLLM/processors/social/long_video.py` validates that each part
  has both:
  - `*_板书识别.md`
  - `*_录音识别.md`
- It removes legacy `*_识别.md` output when present.
- It skips a part on resume only when the expected two files already exist.
- Missing board or audio Markdown is a hard part failure.

Regression coverage:

- `test_social_long_preserves_board_and_audio_markdown`
- `test_social_long_fails_when_audio_markdown_is_missing`

### 7. Long ASR Polling Needed FileTrans Task Reuse

Problem observed during the real run:

- Some long DashScope FileTrans waits ended after task submission but before
  local Markdown was written.
- Without saving the provider task ID, a resume would upload and submit the
  same long audio again, increasing cost and time.

Fix:

- `legacy_app/OCRLLM/processors/audio_filetrans_task_state.py` persists
  in-flight task IDs next to the intended audio Markdown:

  ```text
  <output>.md.filetrans_task.json
  ```

- The sidecar records model and audio fingerprint.
- `legacy_app/OCRLLM/processors/audio.py` loads the task ID when `resume=True`.
- It clears the sidecar after writing the final audio Markdown.
- It leaves the sidecar on generic polling/upload failures so the next resume
  can continue waiting for the provider task.

Evidence from the successful run:

```text
P33 resumed task_id=194c6bc2-0bf7-4d37-a829-ed949c044472
P33 audio Markdown completed after reused polling in about 0.2 seconds.
Final audit found 0 FileTrans sidecars.
```

Regression coverage:

- `legacy_app/tests/test_audio_wait_result.py`
- `legacy_app/tests/test_resume_chain.py`

### 8. Video Resume Needed Artifact Reuse, Not Only Checkpoint Trust

Problem observed during the real run:

- A phase could have valid output artifacts while the checkpoint file had not
  marked the phase complete before process exit.
- Resume based only on the checkpoint could redo expensive board recognition.

Fix:

- `legacy_app/OCRLLM/processors/video_pipeline.py` lets a resumable phase skip
  work when `can_resume()` proves valid artifacts exist.
- The phase is then marked complete and the checkpoint is updated.
- `legacy_app/OCRLLM/processors/video.py` forwards `resume=True` into the ASR
  phase so FileTrans task reuse works through the video pipeline.

Regression coverage:

- `test_video_phase_resume_reuses_valid_artifacts_without_checkpoint`
- `test_video_phase5_forwards_resume_to_audio`

### 9. Social-Long Needed Stability Defaults

Problem:

- A 33-part course creates many large visual and ASR calls.
- Running with aggressive general-purpose concurrency makes live runs harder to
  diagnose and can pressure provider limits.
- Text-model hotword extraction after visual recognition can make a run appear
  to route through the wrong provider.

Fix:

- `legacy_app/OCRLLM/config.py` adds social-long-specific LLM concurrency and
  request-stagger settings.
- `SocialLongVideoProcessor` applies those values to the video processor.
- Text-model hotword extraction is disabled for social-long course runs.

Regression coverage:

- `test_social_long_caps_video_llm_concurrency_for_course_runs`

### 10. Social Media UI Input Could Not Handle Real Free-Form Text

Problem:

- The social tab extracted URLs only from lines that started with `http://` or
  `https://`.
- A real pasted Markdown link or text with surrounding explanation could be
  ignored.
- The tab also lacked `set_input_paths()`, even though the main app router calls
  that method on routed tabs.

Fix:

- `legacy_app/OCRLLM/gui/tabs/extract_social_urls.py` extracts unique HTTP(S)
  URLs from free-form text, including Markdown-style input.
- `legacy_app/OCRLLM/gui/tabs/social_tab.py` uses plain-text paste mode,
  `extract_social_urls()`, and `set_input_paths()`.

Regression coverage:

- `legacy_app/tests/test_social_url_input.py`
- Offscreen PyQt smoke test confirmed the tab accepts surrounding text and
  extracts the Bilibili URL.

## Verification Commands

### Output Audit

```powershell
$root='output\bilibili_cs231n_full'
$parts = Get-ChildItem -Directory $root -Filter 'P*_*' |
  Where-Object { $_.Name -ne '_downloads' }
$files = rg --files $root
[pscustomobject]@{
  PartDirs = $parts.Count
  Board = ($files | Where-Object { $_ -like '*_板书识别.md' } | Measure-Object).Count
  Audio = ($files | Where-Object { $_ -like '*_录音识别.md' } | Measure-Object).Count
  Mp4 = ($files | Where-Object { $_ -like '*.mp4' } | Measure-Object).Count
  FileTransSidecars = ($files | Where-Object { $_ -like '*.filetrans_task.json' } | Measure-Object).Count
}
```

Expected result for the supervised course output:

```text
PartDirs: 33
Board: 33
Audio: 33
Mp4: 33
FileTransSidecars: 0
```

### Context Audit

```powershell
Select-String -Path output\bilibili_cs231n_full\bilibili_social_context.md `
  -Pattern 'github.com/Divsigma/Courses|^### P33|进度条感人' -Encoding UTF8
```

Expected evidence:

- At least one hit for `github.com/Divsigma/Courses`.
- A `### P33 ...` danmaku section.
- Real danmaku bullets, not `No danmaku captured`.

### Code Verification

```powershell
$env:PYTHONPATH='legacy_app'
D:\Anaconda\envs\OCRLLM\python.exe -m py_compile `
  legacy_app\OCRLLM\processors\audio.py `
  legacy_app\OCRLLM\processors\audio_filetrans_task_state.py `
  legacy_app\OCRLLM\processors\video.py `
  legacy_app\OCRLLM\processors\video_pipeline.py `
  legacy_app\OCRLLM\processors\social\bilibili_api.py `
  legacy_app\OCRLLM\processors\social\downloader.py `
  legacy_app\OCRLLM\processors\social\long_video.py `
  legacy_app\OCRLLM\gui\tabs\social_tab.py `
  legacy_app\OCRLLM\gui\tabs\extract_social_urls.py
```

```powershell
$env:PYTHONPATH='legacy_app'
D:\Anaconda\envs\OCRLLM\python.exe -m pytest `
  legacy_app\tests\test_audio_wait_result.py `
  legacy_app\tests\test_resume_chain.py `
  legacy_app\tests\test_social_long_bilibili_course.py `
  legacy_app\tests\test_social_url_input.py -q
```

Expected focused result from the 2026-07-06 audit:

```text
40 passed
```

Root active-library tests should still pass because this work does not change
the public `ocrllm` package:

```powershell
pytest -q
```

Expected root result from the 2026-07-06 audit:

```text
5 passed
```

### UI Smoke Test

```powershell
$env:PYTHONPATH='legacy_app'
$env:QT_QPA_PLATFORM='offscreen'
$env:PYTHONIOENCODING='utf-8'
@'
import sys
from PyQt5.QtWidgets import QApplication
from OCRLLM.gui.tabs.social_tab import SocialTab
from OCRLLM.config import AppConfig

app = QApplication.instance() or QApplication(sys.argv)
tab = SocialTab(lambda: AppConfig(), lambda task: True)
tab._url_input.setPlainText(
    'note before https://www.bilibili.com/video/BV1nJ411z7fe?vd_source=x&p=33 trailing'
)
print(tab._get_urls())
tab.set_input_paths(['https://youtu.be/example123'])
print(tab._get_urls())
'@ | D:\Anaconda\envs\OCRLLM\python.exe -
```

Expected output:

```text
['https://www.bilibili.com/video/BV1nJ411z7fe?vd_source=x&p=33']
['https://youtu.be/example123']
```

## Current Evidence Snapshot

The successful supervised run produced:

```text
output\bilibili_cs231n_full
33 part directories
33 *_板书识别.md files
33 *_录音识别.md files
33 downloaded MP4 files
0 FileTrans task sidecars
0 active video checkpoints
bilibili_social_context.md with resource comments and per-part danmaku
```

The robustness commit for the Bilibili course path is:

```text
afeb4ac Harden legacy Bilibili course recognition
```

## Operational Rules

- Treat a missing part, missing board Markdown, missing audio Markdown, or a
  third legacy `*_识别.md` result as incomplete.
- Do not delete `_downloads` before a resume unless intentionally redownloading.
- Do not delete `.filetrans_task.json` sidecars during an interrupted ASR wait;
  they are what lets OCRLLM reuse the provider-side task.
- Do not promote `legacy_app/OCRLLM/processors/social/*` as public `ocrllm`
  API. Port only a future tested vertical slice when the active library has a
  stable public contract for it.
- Do not treat `No danmaku captured` as success for this tested Bilibili course
  unless Bilibili has genuinely removed or blocked all danmaku sources and the
  fallback segment API has been checked.
- For UI reports about social media input, test both direct URL lines and
  free-form text containing a URL.
