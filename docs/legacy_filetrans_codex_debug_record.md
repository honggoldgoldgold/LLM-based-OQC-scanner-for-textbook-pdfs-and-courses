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
