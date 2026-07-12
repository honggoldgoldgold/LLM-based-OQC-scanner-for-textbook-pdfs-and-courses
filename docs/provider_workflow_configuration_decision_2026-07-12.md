# Provider Workflow Configuration Decision

Date: 2026-07-12.

Status: active implementation decision. This checkpoint is a deliberate
pre-1.0 API migration.

## Goal

One `Config` represents one recognition workflow while keeping provider
transport, model capability, execution, recognition preferences, retry, and
credential-pool state as distinct responsibilities.

Handwriting, printed pages, projected slides, formulas, and tables continue to
use the same `board` workflow. Provider configuration does not introduce
content-class routing.

## Chosen Shape

```python
from ocrllm import (
    Config,
    DashScopeSettings,
    RecognitionExecutionPolicy,
    VisionModelSettings,
)

config = Config(
    provider=DashScopeSettings(
        region="cn-beijing",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        api_key="...",
        enable_thinking=True,
        vl_high_resolution_images=True,
    ),
    vision_model=VisionModelSettings(
        name="qwen3.7-plus-2026-05-26",
        maximum_images_per_request=10,
    ),
    execution=RecognitionExecutionPolicy(max_parallel_requests=4),
)
```

`Config.provider` accepts either:

- an exact settings value for one built-in adapter; or
- an injected provider object implementing synchronous `recognize_images()`.

The concrete settings type selects the adapter. There is no closed provider
category enum and no string such as `provider="dashscope"`. Future
OpenAI-compatible providers, Google SDK, DashScope SDK, and Codex
subprocess/session integrations receive separate settings types only when each
adapter is implemented and tested. Codex settings will not pretend to have an
API key.

The existing `DashScopeSettings` type continues to mean the DashScope
OpenAI-compatible transport. A future direct DashScope SDK adapter must use a
different settings type; it must not overload this one.

## Deliberate Pre-1.0 Break

Remove this duplicated shape:

```python
Config(
    provider="dashscope",
    api_key="...",
    model="qwen3.7-plus-2026-05-26",
    dashscope=DashScopeSettings(...),
)
```

Replace it with:

```python
Config(
    provider=DashScopeSettings(api_key="...", ...),
    vision_model=VisionModelSettings(name="qwen3.7-plus-2026-05-26"),
)
```

No compatibility bridge is retained. The package is `0.1.0`, all known uses
are within this repository, and keeping both shapes would make configuration
ambiguous during the exact period when the public boundary should become
coherent. Worker wire model strings remain unchanged; the worker converts them
to `VisionModelSettings` internally, so the frozen v1alpha1 JSON contract does
not change.

## Credentials

An API credential belongs to the adapter settings that know how to validate
and use it. `Config.api_key` is removed.

- `DashScopeSettings.api_key` is optional and omitted from repr.
- The existing `DASHSCOPE_API_KEY` fallback remains adapter-owned.
- Local OCR rejects every provider/model configuration.
- Injected providers own their own credential state; `Config.provider` is
  already omitted from repr.
- Errors, results, metadata, pool state, and documentation never store raw
  credentials.

This is not a credential pool. Multiple credentials later become separate
secret-safe runtime slots scheduled by fair rotation/cooldown, never a tuple in
one immutable settings value.

## Vision Model Settings

`VisionModelSettings` is exact, immutable, frozen, and slotted:

- `name: str | None` selects a model or lets the adapter use its pinned default.
- `maximum_images_per_request: int | None` declares a stricter known model
  capability when needed.

The effective pre-upload limit is the minimum of:

1. the library hard image-group safety cap;
2. `Config.execution.maximum_images_per_request`;
3. the selected built-in adapter/model capability; and
4. an explicit stricter `VisionModelSettings.maximum_images_per_request`.

Built-in adapter capability is authoritative. A caller cannot raise a known
model limit by declaring a larger value. Unknown injected providers retain the
library safety cap unless their explicit model settings lower it.

Model name and capability remain separate from quality/cost preferences. Do
not encode rules such as “reserve Pro for audio” into this image model value.

## Validation And Error Boundaries

- Exact built-in settings types are reconstructed during every Config snapshot.
- String provider names and settings subclasses are rejected with
  `CONFIG_INVALID` before source or optional dependency work.
- Missing provider in vision mode remains `CONFIG_MISSING` at provider
  resolution, preserving memory-only configuration construction.
- Unsupported built-in model names and inconsistent claimed capabilities fail
  before upload.
- Model/group mismatch raises `SOURCE_TOO_LARGE` with the effective limit and a
  safe limit-source label.
- No implicit paid provider, region, endpoint, retry, fallback, or model switch
  is introduced.

## Implementation Order

1. Add and test `VisionModelSettings` plus effective model/image limit
   resolution.
2. Move `api_key` into `DashScopeSettings` and make that exact value select the
   built-in adapter.
3. Migrate direct facade, capability reporting, quality runner, worker builder,
   and tests without changing recognition prompts or provider requests.
4. Run the full pinned suite, fixture identity, live-evidence identity, static
   checks, clean wheel/import budgets, and an offline built-in request probe.
5. Update recovery/public docs and push a formal checkpoint before beginning
   another provider adapter.

Credential pools, automatic retry/model switching, image resume, PDF, audio,
video, UI, service, and Rust remain outside this checkpoint.
