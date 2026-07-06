# Legacy Filetrans and Codex Debugging Record

Status: legacy application recovery note.

Scope:

- Active code path: `legacy_app/`.
- New importable library path `src/ocrllm/` was not involved in these runtime
  failures.
- Persistent runtime evidence came from `legacy_app/logs/ocrllm.log`.
- Do not record API keys in this file.

## Current State

- Filetrans has one successful end-to-end run in the persistent log.
- Filetrans low-content and no-valid-fragment outcomes are warnings, not hard
  task failures. They should still create an audio Markdown artifact.
- Codex video frame recognition did use Codex for frame batches.
- A separate text hotword extraction step used Qwen after Codex frame
  recognition; that was a routing bug, not proof that Codex frame recognition
  was ignored.
- The stored Codex model setting must be honored exactly. Hidden migration from
  `gpt-5.4-mini` to the default `gpt-5.5` made a saved model look unsaved.
- 2026-07-06 robustness run found that Codex subprocess failures could be
  embedded into board Markdown as HTML comments. That is not a clean output.
  Affected outputs must be rerun only when a concrete dirty marker exists.

## Failure Timeline

### 2026-07-05 07:06 to 07:07

Filetrans was selected:

- `route=filetrans`
- `google_enabled=False`
- `audio_model=qwen3-asr-flash-filetrans`

Input:

- MP3 size: about 11.98 MB
- Duration: about 3140.9 seconds

Old behavior:

- DashScope returned `SUCCESS_WITH_NO_VALID_FRAGMENT`.
- The app raised `ASRNoValidFragmentError`.
- The user-visible error was that long audio async recognition failed because
  no valid speech fragment was detected.

Conclusion:

- The request was not accidentally routed to Google.
- Direct long-audio handling reached DashScope, but DashScope rejected the
  audio content as no valid fragment.
- The current policy is to create an audio Markdown artifact with a warning
  instead of failing the whole job.

### 2026-07-05 20:22 to 20:23

Filetrans was selected again, but the network layer failed before a useful
service result:

- Proxy target: `127.0.0.1:7890`
- Error class: `ProxyError`
- Connection refused by the local proxy port.
- The run was later canceled.

Conclusion:

- This failure was network/proxy state, not an ASR model decision.
- When the local proxy is configured but not running, DashScope upload fails.

### 2026-07-05 20:25 to 20:26

Filetrans was selected again on the same 3140.9-second MP3.

Old behavior:

- DashScope again returned `SUCCESS_WITH_NO_VALID_FRAGMENT`.

Conclusion:

- Retrying direct upload did not solve the false no-speech result.
- The current policy is still to preserve a warning artifact because blank,
  silent, or low-speech videos are valid inputs.

### 2026-07-05 20:56 to 20:57

After the OSS submission fix, the route changed materially:

- OSS upload started for the MP3.
- OSS upload completed with `scheme=oss`.
- Filetrans was submitted with `input=file_url`.
- The task completed after about 55.8 seconds.
- The service returned one transcription result.

Old behavior:

- The result was rejected by the local quality guard:
  `recognized text too short: 1 character`.

Conclusion:

- OSS submission fixed the transport/submission path.
- The service could complete the task, but that specific audio still produced
  unusably small transcript content.
- This should not fail the whole job. The current policy is to preserve the
  completed artifact and write an audio-recognition quality warning.

### 2026-07-05 21:12 to 21:17

Codex frame recognition was active:

- 77 frames were processed in 10 batches.
- Log entries showed `[CODEX]` with model `gpt-5.4`.
- Batch sizes were 8 images, with the last batch containing 5 images.

Failure:

- After Codex frame recognition completed, Phase 4 text hotword extraction used
  Qwen text routing.
- Qwen reported free-tier exhaustion and switched from `qwen-vl-plus` to
  `qwen-vl-max`.
- The user experience looked like "Codex mode still goes through Qwen".

Conclusion:

- The frame/image calls were Codex.
- The hotword text step was incorrectly allowed to call Qwen in Codex mode.
- Fix: Codex mode skips Qwen text hotword extraction.

### 2026-07-05 22:19 to 22:22

Filetrans succeeded end to end on a different extracted MP3:

- `route=filetrans`
- `google_enabled=False`
- `audio_model=qwen3-asr-flash-filetrans`
- MP3 size: about 38.35 MB
- Duration: about 10053.4 seconds
- OSS upload completed.
- Filetrans was submitted with `input=file_url`.
- The task completed after about 167.7 seconds.
- One transcription result was extracted.
- Markdown output was generated.
- Phase 5 completed.
- The video checkpoint reached 100 percent and was deleted.

Conclusion:

- This is the first durable log evidence that Qwen Filetrans worked end to end
  after the OSS submission path was fixed.

### 2026-07-06 00:05 to 01:31

Codex robustness monitoring found two separate issues during large batch runs:

- Blank PowerShell/Codex windows appeared while Codex vision subprocesses were
  running from the legacy GUI.
- Several board Markdown artifacts contained failure placeholders such as
  `<!-- 批次 N 失败: Codex 识图失败: Reading additional input from stdin... -->`.

Evidence:

- Persistent log entries showed repeated `Codex 识图失败: Reading additional
  input from stdin...` at batch level.
- `G:\人工智能（H）_2026-05-22_646927\...\_板书识别.md` contained multiple
  embedded Codex diagnostic dumps before later valid frame output.
- Some older statistics outputs contained only `[WinError 10061]` placeholder
  comments and no real frame markers.

Fix committed:

- Commit `ed6f12c` (`Harden legacy Codex vision subprocess handling`).
- `legacy_app/OCRLLM/core/codex_vision.py` now uses the existing Windows
  no-window subprocess kwargs for Codex CLI calls.
- Codex CLI nonzero exits are retried once and summarized to a single line so
  prompts/diagnostic dumps are not written into Markdown.
- `legacy_app/OCRLLM/processors/video.py` now treats Codex-mode batch or
  per-frame failures as Phase 4 failures instead of writing placeholder
  Markdown and continuing as if the output were clean.
- `legacy_app/OCRLLM/processors/audio.py` uses the existing cached duration
  probe for Filetrans cost logging instead of the missing `_get_duration`
  method.

Operational rule:

- Do not stop a live recognition job only because it is slow or has visible
  Codex windows.
- Rerun only outputs with concrete dirty evidence: batch/frame failure
  placeholders, `Reading additional input from stdin`, `[WinError 10061]`, a
  missing board/audio Markdown after the job has completed, or a hard failure
  in the persistent log.
- When rerunning after this fix, restart the legacy GUI first so new processes
  load commit `ed6f12c`.

### 2026-07-06 completion audit and board-only rerun fix

A later completion audit found no remaining active video recognition work:

- No active legacy `OCRLLM.cli video` or `social_long` worker process was left.
- No video checkpoint file was left.
- The only legacy GUI process was idle.
- The strict target-folder scan covered 40 course folders.
- All 40 folders had exactly two Markdown outputs: board plus audio.
- No target folder contained the known dirty Codex markers:
  `Reading additional input from stdin`, `[WinError 10061]`, Codex failure
  placeholder comments, or empty/missing Markdown outputs.

The audit also found a separate board-only rerun bug:

- A repair run using `--phases 2 3 4` cleaned dirty board Markdown.
- The old artifact invalidation path also deleted the existing Phase 5 audio
  transcript, even though audio was not selected.
- The affected audio transcript was restored from source artifacts.

Fix committed:

- Commit `afeb4ac` (`Harden legacy Bilibili course recognition`) includes the
  resume and artifact-preservation fixes that this audit depended on.
- `legacy_app/OCRLLM/processors/video_pipeline.py` now computes artifact
  invalidation from the selected phases and `skip_audio`.
- Phase 2/3/4 cleanup no longer deletes Phase 5 transcripts when audio is not
  part of the requested rerun.
- `legacy_app/OCRLLM/processors/audio.py` forwards the resume flag to
  Filetrans wait logic, preserving saved task IDs across resume paths.

Related Bilibili social-long note:

- The later full 33-part Bilibili CS231n run used the same Filetrans resume
  path for long per-part audio recognition.
- In-flight DashScope task IDs are now persisted next to the intended audio
  Markdown as `.filetrans_task.json` sidecars and cleared after the final audio
  Markdown is written.
- The Bilibili-specific download, comment/danmaku, two-Markdown contract, and
  social tab input fixes are recorded in
  `docs/legacy_bilibili_social_long_debug_record.md`.

Focused verification passed:

```powershell
$env:PYTHONPATH='legacy_app'
$env:QT_QPA_PLATFORM='offscreen'
D:\Anaconda\envs\OCRLLM\python.exe -m pytest `
  legacy_app\tests\test_resume_chain.py `
  legacy_app\tests\test_codex_vision.py `
  legacy_app\tests\test_failure_propagation.py `
  legacy_app\tests\test_audio_wait_result.py -q
```

Result: `53 passed`.

Completion rule after this audit:

- A folder is clean only when both expected Markdown files exist, both are
  non-empty, and neither contains the known Codex failure markers.
- Rerun only concrete dirty outputs. Do not rerun clean folders because API cost
  is material.

## Codex Model Persistence Failure

Observed QSettings state:

- `ui/codex_vision_enabled = true`
- `ui/codex_model = gpt-5.4-mini`
- `ui/vision_model = gpt-5.4-mini`

Fault:

- The GUI restore path called `migrate_stored_codex_vision_model()`.
- That function treated `gpt-5.4-mini` as a stale default and returned
  `gpt-5.5`.
- A real saved user choice therefore appeared to be lost after closing and
  reopening the GUI.

Fix direction:

- Preserve stored Codex model names exactly after trimming.
- Use validation at apply/run time to catch unsupported models.
- Do not silently rewrite explicit user model choices during restore.

## Operational Rules Learned

- Trust the persistent log before trusting the GUI label.
- Check `route=...`, `google_enabled=...`, and model fields together.
- Distinguish frame/image recognition from text hotword extraction.
- Distinguish direct file upload from OSS `file_url` submission.
- Treat `ProxyError` to `127.0.0.1:7890` as a local proxy state problem.
- Treat Filetrans low-content or no-speech outcomes as warnings. Blank,
  silent, or low-speech videos are valid product inputs.
- Continue failing on upload, polling, timeout, unknown status, and failed
  subtasks. Those are infrastructure or service errors, not valid media
  content states.
- Do not use hidden migrations for model settings unless the old value is
  known to be invalid and not user-selectable.

## Useful Verification Commands

Run from the repo root:

```powershell
$env:PYTHONPATH="legacy_app"
$env:QT_QPA_PLATFORM="offscreen"
python -m pytest legacy_app\tests\test_codex_settings_dialog.py legacy_app\tests\test_codex_vision.py -q
python -m pytest legacy_app\tests\test_audio_wait_result.py legacy_app\tests\test_google_audio_routing.py -q
```

Inspect current saved GUI settings:

```powershell
Get-ItemProperty -Path 'HKCU:\Software\OCRLLM\QCR\ui' | Format-List *
```

Inspect persistent runtime evidence:

```powershell
Get-Content legacy_app\logs\ocrllm.log -Tail 200
```
