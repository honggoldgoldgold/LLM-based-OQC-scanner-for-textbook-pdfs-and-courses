# Legacy YouTube Playlist Social-Long Workflow

Status: legacy application workflow note.

Final proof on 2026-07-06: the full 97-item Modern Robotics playlist completed
through OCRLLM `social_long` with 97 board markdown files, 97 audio markdown
files, 97 downloaded MP4 files, zero dirty markdown files, and zero remaining
FileTrans sidecars. The personal combiner then produced 10 study markdown
pieces.

Scope:

- Active code path: `legacy_app/`.
- New importable library path `src/ocrllm/` is not involved.
- This workflow is for public course playlists that should be downloaded and
  recognized through OCRLLM's legacy `social_long` pathway.
- The final markdown-combination step is a personal post-process tool, not part
  of OCRLLM recognition.
- CLI, API, and GUI social mode all reach the same legacy
  `SocialLongVideoProcessor` for long videos and playlists. The full 97-item
  proof run used the CLI because it gives reproducible environment variables,
  output paths, resume commands, logs, and audit commands. The GUI entry is
  wired to the same processor, but the GUI itself is not the audited 97-item
  proof harness and does not yet expose the final audit or combiner as product
  actions.
- Do not record API keys, cookies, browser session state, or private account
  details in this file.

## Course Under Test

Public YouTube playlist:

```text
https://youtube.com/playlist?list=PLggLP4f-rq02vX0OQQ5vrCxbJrzamYDfx&si=6VZ5fem42kqyyasd
```

Observed metadata:

```text
Title: Modern Robotics, All Videos
Platform: youtube
Parts: 97
Total duration: about 26,789 seconds
First video: Modern Robotics: Introduction to the Lightboard
Last video: Modern Robotics, Chapter 13.5: Mobile Manipulation
```

## Boundary

Use this legacy CLI path:

```powershell
$env:PYTHONPATH='legacy_app'
D:\Anaconda\envs\OCRLLM\python.exe -m OCRLLM.cli social_long <playlist-url> `
  --parts 1-97 --resume -o output\youtube_modern_robotics_full
```

Do not expose this downloader as public `ocrllm` API. The public library
boundary remains `src/ocrllm/`.

## GUI Entry Reality

Current behavior in the legacy GUI social tab:

- The social URL field is a `QTextEdit` with rich text disabled. It accepts
  normal typed or pasted characters and free-form text.
- URL extraction accepts plain URLs, Markdown-style links, and surrounding
  explanatory text, then de-duplicates URLs.
- The "probe video information" action calls `probe_video_info()`. For YouTube
  playlists, the current downloader reports flat playlist entries as `parts`
  and `total_parts`.
- When probe finds more than one part, the parts selector becomes visible and
  all parts are checked by default. Leaving all checked returns
  `part_indices=None`, which means "process all parts".
- In automatic mode, `classify_video()` treats any multi-part playlist as
  `VideoCategory.LONG`, regardless of the duration of each short video.
- The run action passes the URL, selected `part_indices`, and prompt template to
  `SocialLongVideoProcessor.process()`. Therefore, pasting the playlist URL in
  GUI automatic mode or long-video mode should start the same playlist
  download/recognition pipeline.

Important product caveats:

- The proof run did not use GUI clicks as the harness; it used the CLI path
  above for reliable logging and resume.
- The GUI default output directory is based on `cfg.paths.output_dir` plus a
  label like `youtube_1`; it will not automatically choose
  `output\youtube_modern_robotics_full`.
- The GUI does not currently run `tools\audit_social_long_course_output.py`
  after completion, so it can finish without presenting the same explicit
  97/97 two-markdown proof.
- The GUI does not currently run the personal combiner. Combination remains a
  manual post-process.
- For a 97-item course, the GUI worker must stay alive for a long time. Resume
  support exists in the processor, but the GUI does not show a dedicated
  "resume this course and audit it" workflow.
- The GUI uses the app's saved settings. The CLI proof made Codex, DashScope,
  FileTrans, and concurrency settings explicit in the shell to remove ambiguity.

## Required Environment

The CLI does not automatically inherit GUI QSettings. For a reproducible run,
make the settings explicit in the same PowerShell session:

```powershell
$ui = Get-ItemProperty -Path 'HKCU:\Software\OCRLLM\QCR\ui'
$env:PYTHONPATH='legacy_app'
$env:PYTHONIOENCODING='utf-8'
$env:DASHSCOPE_API_KEY=$ui.api_key
$env:DASHSCOPE_BASE_URL=$ui.base_url
$env:OCRLLM_CODEX_VISION_ENABLED='1'
$env:OCRLLM_CODEX_COMMAND=$ui.codex_command
$env:OCRLLM_CODEX_MODEL=$ui.codex_model
$env:OCRLLM_CODEX_REASONING_EFFORT=$ui.codex_reasoning_effort
$env:OCRLLM_CODEX_PARALLEL_REQUESTS='4'
$env:OCRLLM_CODEX_REQUEST_STAGGER_SECONDS='10'
$env:OCRLLM_CODEX_VIDEO_FRAME_BATCH_SIZE=$ui.codex_video_frame_batch_size
$env:OCRLLM_SOCIAL_LONG_LLM_PARALLEL_REQUESTS='4'
$env:OCRLLM_SOCIAL_LONG_LLM_REQUEST_STAGGER_SECONDS='10'
```

Note: for `social_long` course processing with Codex vision enabled, OCRLLM now
caps the effective video frame batch size to 1 inside
`SocialLongVideoProcessor._video_processor_config()`. The registry value may
remain larger for other modes, but social-long uses the stable single-frame
Codex path to avoid incomplete multi-frame markers.

Then run:

```powershell
D:\Anaconda\envs\OCRLLM\python.exe -m OCRLLM.cli social_long `
  "https://youtube.com/playlist?list=PLggLP4f-rq02vX0OQQ5vrCxbJrzamYDfx&si=6VZ5fem42kqyyasd" `
  --parts 1-97 --resume -o output\youtube_modern_robotics_full
```

Use the same command to resume after interruption.

## Expected OCRLLM Output Contract

For every selected playlist item directory:

```text
*_板书识别.md
*_录音识别.md
```

The run is not complete if any selected part is missing either file, either
file is empty, a `*.filetrans_task.json` sidecar remains after the final run, or
known Codex failure markers appear in markdown.

YouTube subtitle downloads may return HTTP 429. That is not fatal when OCRLLM
successfully falls back to no-subtitle download, because the audio markdown is
generated by OCRLLM ASR rather than by YouTube subtitle files.

## Audit

Run from the repository root:

```powershell
D:\Anaconda\envs\OCRLLM\python.exe tools\audit_social_long_course_output.py `
  output\youtube_modern_robotics_full --expected-parts 97
```

Expected final result:

```text
PartDirs: 97
BoardMarkdown: 97
AudioMarkdown: 97
DownloadedMp4: 97
FileTransSidecars: 0
DirtyMarkdown: 0
IncompleteParts: 0
OK: True
```

## Personal Combination Step

This is not part of OCRLLM recognition. Use it after the audit passes:

```powershell
D:\Anaconda\envs\OCRLLM\python.exe tools\combine_social_long_course_markdowns.py `
  output\youtube_modern_robotics_full `
  --videos-per-piece 10 `
  --course-title "Modern Robotics, All Videos"
```

Default output:

```text
output\youtube_modern_robotics_full\combined_markdown\P001-P010_study.md
output\youtube_modern_robotics_full\combined_markdown\P011-P020_study.md
...
```

Use `--mode separate` if separate board and audio compilation files are needed.

## Implementation Notes

- YouTube playlist probing must return playlist entries and `total_parts > 1`.
- Auto-routing must classify playlists as `social_long`, not `social_short`.
- yt-dlp must run with playlist support enabled for non-Bilibili playlist URLs.
- `--parts` applies to YouTube playlist entries through yt-dlp
  `playlist_items`, as well as to Bilibili pages.
- Existing MP4 downloads under `_downloads` are reusable on `--resume`.
- Partial playlist download success is not acceptable; missing selected entries
  must fail the run.
- In Codex social-long mode, the effective video frame batch size is capped at
  1. Larger batches were observed to produce incomplete frame markers and force
  slow fallback reruns.
- Video debug temp directories must be Windows-safe and must not end in spaces
  or dots. YouTube titles can produce such stems when naively truncated.
- Social-long part output directories must strip trailing spaces, dots, and
  underscores after the legacy 80-character truncation. Windows may create a
  normalized path while Python still tries to scan the unnormalized name.
- Social-long `VideoProcessor` artifact stems must be shortened when the board,
  audio, hotword, or temporary output paths would exceed the Windows-safe path
  budget. The skip logic first accepts an existing clean board/audio pair so
  older completed outputs are not duplicated when the naming policy changes.
- DashScope FileTrans task sidecars must be shortened based on the resolved
  absolute `.tmp` sidecar path length, not only the relative output path length.
- OCRLLM's qwen/DashScope audio route may use the short synchronous qwen ASR
  model for very short clips and FileTrans for longer clips.

## Full Debug And Decision Record

This section records the material workflow changes, failures, decisions, and
proof steps from the task. No workflow or implementation decision from the task
is intentionally omitted. Secrets, account state, and API keys are intentionally
not recorded.

### 1. Boundary Decision

Problem:

- The user asked whether the final successful path is "what OCRLLM does".
- The repo has two OCRLLM surfaces: the new importable library in
  `src/ocrllm/` and the legacy application in `legacy_app/`.

Decision:

- Keep this work in `legacy_app/`.
- Do not move social downloading, GUI, yt-dlp, DashScope/FileTrans, or Codex
  social-video behavior into `src/ocrllm/`.

Reason:

- `START_HERE.md`, `MIGRATION_STATUS.md`, and `legacy_app/README_LEGACY.md`
  define social download/GUI behavior as legacy compatibility work.
- The public `ocrllm` library is intentionally lightweight and should not import
  GUI, FastAPI, social downloader, or heavy media dependencies at import time.

Result:

- The reusable workflow is OCRLLM legacy-app behavior:
  `python -m OCRLLM.cli social_long ...` and the GUI/API social path that calls
  the same `SocialLongVideoProcessor`.
- It is not yet a stable public `import ocrllm` API.

### 2. Proof Harness Decision

Problem:

- The user needed a proven 97-video course workflow, not a half-done feature.
- A GUI-only proof would be harder to resume, audit, and document.

Paths considered:

- Prove through the GUI because the user eventually wants product reuse.
- Prove through the CLI and then verify the GUI routes into the same processor.

Decision:

- Use CLI for the full 97-item proof, then inspect/test the GUI routing path.

Reason:

- CLI made the settings, output directory, resume command, logs, and audit
  commands reproducible.
- GUI is still relevant, but it lacks built-in final audit and combined-output
  actions.

Result:

- The full course proof used:
  `python -m OCRLLM.cli social_long <playlist-url> --parts 1-97 --resume`.
- GUI remains wired to the same processor but should be treated as a product
  entry point that still needs UX hardening.

### 3. YouTube Playlist Probe

Problem:

- The legacy downloader handled single social links better than full YouTube
  playlists.
- A playlist of short videos must route to course/long processing even when
  individual videos are short.

Change:

- `probe_video_info()` now uses flat playlist extraction for YouTube playlists.
- It reports playlist entries as `parts` and sets `total_parts` from
  `playlist_count` or entry count.
- `classify_video()` treats any multi-part playlist as `VideoCategory.LONG`.

Reason:

- The social-long processor must process each playlist item as a course part.
- Duration-based routing alone would misclassify many short course clips as
  short-video social content.

Proof:

- `legacy_app/tests/test_social_long_youtube_playlist.py` covers playlist probe
  and long-course routing.

### 4. YouTube Playlist Download

Problem:

- Single-link yt-dlp options used `noplaylist=True`, which is wrong for a course
  playlist.
- The user needed selected ranges such as `--parts 1-97` to map to YouTube
  playlist entries, not only Bilibili parts.

Change:

- `_build_ydl_opts()` accepts playlist mode.
- `_download_yt_dlp()` enables playlist mode for playlist URLs.
- `part_indices` maps to yt-dlp `playlist_items`.
- Playlist filenames include playlist index, title, and video id.
- Missing selected playlist entries now fail the run instead of silently
  producing a partial course.

Reason:

- Partial success is dangerous for a course workflow. The user asked for two
  markdowns per course video, so the downloader must fail loudly if an item is
  missing.

Proof:

- Tests assert `noplaylist=False`, `playlist_items="1,3"`, and failure when a
  selected playlist entry has no downloaded file.
- Final audit found 97 downloaded MP4 files.

### 5. YouTube Subtitle 429 Handling

Observation:

- During the real run, YouTube subtitle fetches sometimes returned HTTP 429.

Decision:

- Treat subtitle 429 as non-fatal when the MP4 download succeeds.
- Continue using OCRLLM audio recognition for the audio markdown.

Reason:

- The required audio markdown comes from OCRLLM ASR/qwen/FileTrans, not from
  YouTube subtitles.
- Failing the whole course because optional subtitles are throttled would make
  the product less robust.

Result:

- The run completed with audio markdown generated by OCRLLM.

### 6. Codex Vision Stability

Problem:

- Larger social-long Codex video frame batches could leave incomplete frame
  markers or dirty markdown output.

Change:

- In social-long Codex mode, OCRLLM caps effective `video.batch_size` and
  `codex_vision.video_frame_batch_size` to 1.
- Dirty markers are rejected when deciding whether existing markdown output is
  complete.

Reason:

- A 97-item course favors deterministic completion over frame-level batching
  speed.
- Dirty output must not be accepted as a completed board markdown.

Proof:

- Focused tests cover the social-long batch cap.
- Final audit found `DirtyMarkdown: 0`.

### 7. Resume And Clean-Skip Logic

Problem:

- Long runs are interruptible. Completed parts should not be repeated, but
  dirty or partial parts must be rerun.
- After changing output-stem shortening, old completed outputs risked being
  duplicated under new shorter names.

Change:

- Social-long checks for exactly one clean board markdown and matching clean
  audio markdown before choosing a new output stem.
- Existing clean pairs are skipped.
- Dirty markers, empty files, and incomplete board/audio pairs are not accepted.

Reason:

- Resume must be safe across interrupted runs and across naming-policy changes.

Proof:

- Partial/dirty P17-style output was recovered.
- Clean preexisting P3-style output was accepted instead of duplicated.
- Final audit found `IncompleteParts: 0`.

### 8. Windows Path Length And Trailing-Space Failures

Problem:

- Long YouTube titles plus nested course folders produced Windows path-length
  failures.
- One part directory, observed around P44, failed because truncation left a
  trailing space. Windows normalized the actual directory name while Python
  later scanned the unnormalized name.

Change:

- Part output names strip trailing spaces, dots, and underscores after the
  legacy 80-character truncation.
- Video output stems are shortened only when board/audio/hotword/temp paths
  would exceed the Windows-safe path budget.
- Shortened stems keep a readable prefix and digest.
- Video debug temp directories were made Windows-safe.

Reason:

- The workflow must survive real course titles, not only small toy URLs.

Proof:

- Tests cover the trailing-space regression and output-stem shortening.
- The full 97-item course completed after these path fixes.

### 9. Incremental Markdown Temp Path

Problem:

- Even after shortening final output stems, the incremental writer could create
  a temporary `<output>.tmp` path that exceeded the Windows-safe budget.

Change:

- `incremental_writer.py` now uses a shorter same-directory
  `.ocrllm-<digest>.tmp` path when needed.

Reason:

- Atomic-ish incremental writes still need temp files, but the temp path must
  not be longer than the final target.

Proof:

- `legacy_app/tests/test_incremental_writer.py` covers the shortened temp path.

### 10. DashScope FileTrans Sidecar Path

Problem:

- FileTrans task sidecar names could exceed the path budget because shortening
  was based on the visible output path, not the resolved absolute `.tmp` path.

Change:

- `audio_filetrans_task_state.py` now shortens sidecar paths based on the
  resolved absolute temp sidecar length.
- It can fall back to `prefix.digest.filetrans_task.json` or
  `audio.<digest>.filetrans_task.json`.

Reason:

- Long course titles and nested output directories otherwise break resume for
  audio recognition.

Proof:

- Tests cover absolute sidecar path shortening.
- Final audit found `FileTransSidecars: 0`.

### 11. Per-Part Output Contract

Problem:

- The success criterion was two markdowns per course video: board/graph and
  audio.

Change:

- Social-long output validation now explicitly checks the user-facing board and
  audio markdown outputs after each part.
- It removes legacy merged-board draft files when they are separate transient
  artifacts.

Reason:

- Success must be based on actual markdown artifacts, not only successful
  function return values.

Proof:

- Final audit found `BoardMarkdown: 97` and `AudioMarkdown: 97`.

### 12. Audit Tool

Problem:

- A 97-folder course is too large to inspect manually.

Change:

- Added `tools\audit_social_long_course_output.py`.
- The tool counts part directories, board markdowns, audio markdowns,
  downloaded MP4 files, FileTrans sidecars, dirty markdowns, and incomplete
  parts.
- It has JSON output for machine checks and Windows stdout fallback for Unicode
  console issues.

Reason:

- "Looks done" is not enough for this workflow. The proof must be repeatable.

Proof:

- Final audit output:

```text
PartDirs: 97
BoardMarkdown: 97
AudioMarkdown: 97
DownloadedMp4: 97
FileTransSidecars: 0
DirtyMarkdown: 0
IncompleteParts: 0
OK: True
```

### 13. Personal Combiner Tool

Problem:

- The user did not want 97 separate folders to be the only readable study
  output.
- The user also said combination should not become OCRLLM recognition logic.

Change:

- Added `tools\combine_social_long_course_markdowns.py`.
- Default mode combines board and audio markdowns interleaved per video.
- Default chunk size used in the proof was 10 videos per file.
- The tool also supports `--mode separate`.

Reason:

- This satisfies the personal readability requirement while keeping OCRLLM's
  workflow boundary clean.

Proof:

- The proof produced 10 combined files:
  `P001-P010_study.md` through `P091-P097_study.md`.

### 14. GUI Character Input

Problem:

- The user mentioned that social media mode had a UI problem where characters
  could not be entered.

Observed current state:

- The social tab URL input is currently `QTextEdit`, uses
  `setAcceptRichText(False)`, and reads `toPlainText()`.
- The URL extractor accepts free-form typed text and Markdown links.
- Tests cover extracting URLs from plain explanatory text and Markdown-style
  pasted links.

Decision:

- No additional GUI input edit was made in this task because the current code
  already addresses the reported symptom at the URL-input level.

Remaining risk:

- This has code-level/test-level coverage, but it was not part of the full
  97-item GUI click proof.

### 15. Final Verification And Commit

Commands run:

```powershell
$env:PYTHONPATH='legacy_app'
D:\Anaconda\envs\OCRLLM\python.exe -m pytest legacy_app\tests\test_social_long_bilibili_course.py legacy_app\tests\test_social_long_youtube_playlist.py legacy_app\tests\test_audio_wait_result.py legacy_app\tests\test_resume_chain.py legacy_app\tests\test_incremental_writer.py tests\test_social_long_course_tools.py -q

D:\Anaconda\envs\OCRLLM\python.exe -m pytest -q

D:\Anaconda\envs\OCRLLM\python.exe tools\audit_social_long_course_output.py output\youtube_modern_robotics_full --expected-parts 97

D:\Anaconda\envs\OCRLLM\python.exe tools\combine_social_long_course_markdowns.py output\youtube_modern_robotics_full --videos-per-piece 10 --course-title "Modern Robotics, All Videos"
```

Results:

- Focused tests: 53 passed.
- Root tests: 8 passed.
- Final audit: OK.
- Final commit from the hardening task:
  `a9b8adc Harden legacy YouTube playlist social-long workflow`.

## Verification Commands

Focused tests:

```powershell
$env:PYTHONPATH='legacy_app'
$env:QT_QPA_PLATFORM='offscreen'
D:\Anaconda\envs\OCRLLM\python.exe -m pytest `
  legacy_app\tests\test_social_long_youtube_playlist.py `
  legacy_app\tests\test_social_long_bilibili_course.py `
  legacy_app\tests\test_social_url_input.py `
  legacy_app\tests\test_audio_wait_result.py `
  legacy_app\tests\test_resume_chain.py `
  tests\test_social_long_course_tools.py -q
```

Root import contract:

```powershell
D:\Anaconda\envs\OCRLLM\python.exe -m pytest -q
```

Final evidence from the proven run:

```text
D:\Anaconda\envs\OCRLLM\python.exe tools\audit_social_long_course_output.py output\youtube_modern_robotics_full --expected-parts 97
PartDirs: 97
BoardMarkdown: 97
AudioMarkdown: 97
DownloadedMp4: 97
FileTransSidecars: 0
DirtyMarkdown: 0
IncompleteParts: 0
OK: True

D:\Anaconda\envs\OCRLLM\python.exe tools\combine_social_long_course_markdowns.py output\youtube_modern_robotics_full --videos-per-piece 10 --course-title "Modern Robotics, All Videos"
combined_markdown\P001-P010_study.md
combined_markdown\P011-P020_study.md
combined_markdown\P021-P030_study.md
combined_markdown\P031-P040_study.md
combined_markdown\P041-P050_study.md
combined_markdown\P051-P060_study.md
combined_markdown\P061-P070_study.md
combined_markdown\P071-P080_study.md
combined_markdown\P081-P090_study.md
combined_markdown\P091-P097_study.md

$env:PYTHONPATH='legacy_app'
D:\Anaconda\envs\OCRLLM\python.exe -m pytest legacy_app\tests\test_social_long_bilibili_course.py legacy_app\tests\test_social_long_youtube_playlist.py legacy_app\tests\test_audio_wait_result.py legacy_app\tests\test_resume_chain.py legacy_app\tests\test_incremental_writer.py tests\test_social_long_course_tools.py -q
53 passed

D:\Anaconda\envs\OCRLLM\python.exe -m pytest -q
8 passed
```
