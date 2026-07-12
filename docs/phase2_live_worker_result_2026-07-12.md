# Phase 2 Beijing Live Worker Result

Date: 2026-07-12.

Status: the opt-in production-worker smoke passes; the formal Phase 2 GO
decision follows the clean committed-source proof.

## Scope

Node launched exactly:

```text
D:\Anaconda\envs\OCRLLM\python.exe -m ocrllm.worker
```

using an argument array with `shell: false`. `PYTHONPATH` selected the active
library source, `DASHSCOPE_API_KEY` remained environment-only, and no output
directory was requested. Every stdout line passed the independent Node event
validator. The worker used the unified `profile="board"` workflow; there was no
handwriting branch, alternate prompt, alternate model, application retry, or SDK
retry.

The local inputs were user-authorized, untracked screenshots. They remain
uncommitted and are not copied into evidence. The recognized Markdown is also
not stored; only size and SHA-256 are recorded.

## Timeout Debug Record

The first dense formula/table attempt used the frozen worker default of 120
seconds per provider call. It returned typed `PROVIDER_TIMEOUT` after about
245.2 seconds. That verifier version did not retain the safe error details, so
the failing workflow pass is unknown and is not inferred.

The final Phase 1 v17 evidence used 180 seconds per call. Changing the frozen
protocol default globally was rejected because it would silently alter every
wire caller. The live verifier instead requests `timeout_seconds: 180`
explicitly.

The second dense formula/table attempt then returned typed `PROVIDER_TIMEOUT`
after about 185.2 seconds with exact safe details:

```text
workflow_pass            draft
provider_calls_attempted 1
provider                 dashscope
model                    qwen3.7-plus-2026-05-26
```

TCP port 443 and DNS resolution for `dashscope.aliyuncs.com` were healthy. The
failure was therefore provider response latency during the primary model call,
not Node transport, child isolation, URI decoding, scout merge, handwriting
routing, or local filesystem workflow. Neither failed job retried itself.

## Passing Smoke

A final independent job used a simpler formula/prose screenshot at the proven
180-second timeout. It completed in about 560.3 seconds and produced exactly:

```text
accepted -> progress 0/1 -> progress 1/1 -> result
```

The validated result evidence is:

```text
provider                         dashscope
provider region                  cn-beijing
model                            qwen3.7-plus-2026-05-26
source type                      image
profile                          board
status                           complete
provider calls                   4
standalone signs restored        0
scout abstentions                0
Markdown UTF-8 bytes             2,439
Markdown SHA-256                 d56184357c69848b94d4d9d00eeaaa4c99c00004b4bdb449a182028e99275e03
Node-validated stdout lines      4
```

This is an operational worker smoke, not a new recognition-quality corpus or a
manual transcription comparison. The two-run Phase 1 v17 gate remains the
authority for printed, projected, handwriting, formula, table, and ordered-image
quality. The live smoke proves that the production Node-to-worker boundary can
execute that same workflow successfully against Beijing.

## Evidence

Machine-readable summary:
`evidence/phase2/phase2-live-worker-2026-07-12-cn-beijing.json`.

The successful worker source was full commit
`b313d3efec65f32026d60e9c2135e8f20c30b55f`. The live verifier bytes have
SHA-256 `c6801fc842d42044cf684e6e2b865fe845d8c22e62124e09e972791ce827f77a`;
they become immutable in the checkpoint commit that adds this record.

## Remaining Decision Step

Run the full offline suite and clean Git-archive proof for the checkpoint commit.
If both pass, every Phase 2 GO condition is satisfied. Keep the result scoped to
a development worker with an explicitly configured Python executable; it does
not claim packaged Electron compatibility.
