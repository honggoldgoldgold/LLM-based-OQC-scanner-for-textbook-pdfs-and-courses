# Provider Workflow Configuration Checkpoint

Date: 2026-07-12.

Status: GO for the adapter-owned configuration foundation and the existing
DashScope OpenAI-compatible adapter. Additional provider adapters remain
separate checkpoints.

## Public API Migration

The preferred and only built-in DashScope call shape is now:

```python
from ocrllm import (
    Config,
    DashScopeSettings,
    VisionModelSettings,
    recognize,
)

result = recognize(
    "board.png",
    config=Config(
        provider=DashScopeSettings(
            region="cn-beijing",
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            api_key="...",  # or use DASHSCOPE_API_KEY
        ),
        vision_model=VisionModelSettings(
            name="qwen3.7-plus-2026-05-26",
        ),
    ),
)
```

The removed pre-1.0 fields are `Config.api_key`, `Config.model`, and
`Config.dashscope`. The removed string selector is
`Config(provider="dashscope")`. There is no compatibility bridge; see
`provider_workflow_configuration_decision_2026-07-12.md` for the rationale.

An injected provider remains:

```python
Config(
    provider=my_provider,
    vision_model=VisionModelSettings(name="host-owned-model"),
)
```

The injected object retains its identity. Exact built-in settings and nested
model/execution/preference values are reconstructed and revalidated for every
Config snapshot.

## Adapter Selection And Credentials

The exact `DashScopeSettings` type selects the current built-in
OpenAI-compatible adapter. String categories and settings subclasses raise
`CONFIG_INVALID` before source or optional dependency work. Future Google SDK,
DashScope SDK, and Codex subprocess/session adapters require their own settings
types; no fake closed enum or unused placeholder class was added.

`DashScopeSettings.api_key` is optional, secret, and absent from repr. The
adapter resolves the explicit value first and then `DASHSCOPE_API_KEY`.
Malformed and Coding Plan `sk-sp-` credentials fail without echo. The worker
continues to build a credential-free Beijing settings value and resolves the
environment only inside the recognition child.

The user's Aliyun workflow remains `cn-beijing`; the library still requires an
explicit matching region and endpoint so a credential never silently selects a
different region.

## Vision Model Capability

`VisionModelSettings` is exact, frozen, slotted, and contains:

- `name: str | None`; and
- `maximum_images_per_request: int | None`.

The DashScope adapter has an explicit capability entry for every supported
model. The effective pre-upload group limit is the minimum of library safety,
execution policy, built-in model capability, and a stricter explicit model
limit. A model/group mismatch raises `SOURCE_TOO_LARGE` before file access or
provider dispatch. Unsupported built-in model names raise `CONFIG_INVALID`
before source or optional SDK work.

The worker v1alpha1 wire model remains a JSON string. Its internal builder now
converts that string to `VisionModelSettings`; no wire fixture or command/event
contract changed.

## Files And Responsibilities

```text
src/ocrllm/vision_model_settings.py
    Validate public vision model identity and a stricter image capability.
src/ocrllm/resolve_effective_image_limit.py
    Select the strictest safe pre-upload image limit.
src/ocrllm/providers/dashscope/resolve_dashscope_maximum_images.py
    Own approved model image caps for the current adapter.
src/ocrllm/providers/dashscope/provider_settings.py
    Own DashScope endpoint, credential, and evidence-affecting settings.
src/ocrllm/providers/resolve_vision_provider.py
    Resolve exact built-in settings or preserve an injected provider.
src/ocrllm/config.py
    Compose and freshly revalidate one workflow without provider strings.
src/ocrllm/worker/build_worker_image_config.py
    Convert the frozen worker request to the new direct-Python configuration.
tests/test_vision_model_settings.py
    Prove exact types, bounds, mutation resistance, limits, and early failures.
```

Phase 1 prompts, request body shape, zero SDK retries, response parsing, error
mapping, sign restoration, output schema, and quality truth were not changed.
Printed, projected, handwritten, formula, table, and ordered-image inputs still
share one `board.v17` workflow.

## Verification

Decision commit `fb3ef8f` and implementation commit `3dd1ba3` are pushed.

- Affected configuration/provider/quality/worker suite: 278 passed.
- Authoritative isolated full suite with Pillow 12.3.0: 912 passed, 1 optional
  RapidOCR-profile test skipped.
- Phase 1 generated fixtures: byte-identical.
- Ruff over `src` and `tests`, `compileall`, `git diff --check`, and the lazy
  provider-workflow import probe: passed.
- Plain import loads no optional image/OCR/provider/network stack, batch
  scheduler, provider dispatch gate, or provider protocol module.
- Clean Git archive at `3dd1ba3` builds a 119,519-byte wheel with SHA-256
  `78e5cf0883e65cf0b35313a875d7175b5e841de2305fe237b04b3cb7aac19cae`.
- Its no-dependency target is 550,146 bytes with exact extras
  `dashscope`, `dev`, `image`, and `ocr`.
- Thirty measured imports after two discarded warmups pass the budget: wall
  median/p95/max `41.7100/47.4858/49.2955` ms and CPU
  median/p95/max `46.875/46.875/46.875` ms.
- A fresh `image,dashscope` install adds 32,653,863 bytes, below the 64 MiB
  ceiling, with Pillow 12.3.0, OpenAI 2.45.0, and HTTPX 0.28.1.
- An installed generated 12×13 PNG completed one exact pinned-model request
  through the real OpenAI client boundary and an HTTPX mock transport. The
  result reported provider `dashscope` and exactly one call.

The first installed probe deliberately used no external HTTP but accidentally
generated a 9×7 PNG. The library correctly raised `SOURCE_INVALID` before the
mock provider because both provider image dimensions must exceed 10 pixels.
The corrected independent 12×13 probe passed. No external provider/API HTTP
request was made in either run.

Private screenshots and `docs/Textbook.pdf` were not staged or redistributed.

## Remaining Provider Work

This checkpoint does not claim built-in Google SDK, DashScope SDK, or Codex
execution. It establishes how those adapters compose without changing Config
again:

- each implemented adapter gets one exact settings type and its own credential
  rules;
- model capabilities and error taxonomy must fail safely before pools;
- no API key is invented for Codex subprocess/session execution;
- credential pools remain stateful runtime schedulers, not tuples in Config;
- automatic retry, fallback, switching, and image resume remain unimplemented.

The next provider checkpoint must choose one real adapter or finish a shared
error-disposition contract based on measured need. Do not add empty settings
classes for all examples at once.
