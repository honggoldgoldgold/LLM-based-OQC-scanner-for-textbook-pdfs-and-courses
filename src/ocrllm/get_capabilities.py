"""Report every atomic OCRLLM capability without network or optional imports."""

from __future__ import annotations

from .config import Config
from .contracts.capability_report import CapabilityReport
from .providers.dashscope.resolve_dashscope_model import DEFAULT_DASHSCOPE_MODEL
from .snapshot_config import snapshot_config


_CAPABILITY_NAMES = (
    "image.board.png",
    "image.board.jpeg",
    "provider.dashscope.vision",
    "provider.dashscope.audio-short",
    "provider.dashscope.filetrans",
    "worker.jsonl.v1alpha1",
    "worker.jsonl.v1alpha2",
    "pdf.text",
    "pdf.vision",
    "pdf.text.resume",
    "pdf.vision.resume",
    "audio.short.wav-pcm-s16",
    "audio.short.mp3-mpeg-layer3",
    "audio.short.m4a-aac-lc",
    "audio.long.wav-pcm-s16",
    "audio.long.mp3-mpeg-layer3",
    "audio.long.m4a-aac-lc",
    "video.mp4-h264",
    "video.mp4-h264-aac",
)
_PHASE_BY_DEFERRED_CAPABILITY = {
    "provider.dashscope.audio-short": "Phase 4",
    "provider.dashscope.filetrans": "Phase 4",
    "worker.jsonl.v1alpha2": "Phase 3",
    "pdf.text": "Phase 3",
    "pdf.vision": "Phase 3",
    "pdf.text.resume": "Phase 3",
    "pdf.vision.resume": "Phase 3",
    "audio.short.wav-pcm-s16": "Phase 4",
    "audio.short.mp3-mpeg-layer3": "Phase 4",
    "audio.short.m4a-aac-lc": "Phase 4",
    "audio.long.wav-pcm-s16": "Phase 4",
    "audio.long.mp3-mpeg-layer3": "Phase 4",
    "audio.long.m4a-aac-lc": "Phase 4",
    "video.mp4-h264": "Phase 5",
    "video.mp4-h264-aac": "Phase 5",
}


def get_capabilities(config: Config | None = None) -> tuple[CapabilityReport, ...]:
    """Return deterministic installed/configured/proven atomic capabilities."""

    if config is None:
        image_status = "available"
        image_reason = (
            "Phase 1 implementation, live quality, and packaging gates passed."
        )
        provider_status = "unavailable"
        provider_reason = (
            "Explicit DashScope region and endpoint settings are required for use."
        )
    else:
        validated = snapshot_config(config)
        image_status, image_reason, provider_status, provider_reason = (
            _configured_image_status(validated)
        )

    reports: list[CapabilityReport] = []
    for name in _CAPABILITY_NAMES:
        if name in {"image.board.png", "image.board.jpeg"}:
            reports.append(
                CapabilityReport(name=name, status=image_status, reason=image_reason)
            )
        elif name == "provider.dashscope.vision":
            reports.append(
                CapabilityReport(
                    name=name,
                    status=provider_status,
                    reason=provider_reason,
                )
            )
        elif name == "worker.jsonl.v1alpha1":
            reports.append(
                CapabilityReport(
                    name=name,
                    status="experimental",
                    reason=(
                        "Command, event, and JSONL I/O contracts pass; process control, "
                        "cancellation, Node, and live gates remain."
                    ),
                )
            )
        else:
            phase = _PHASE_BY_DEFERRED_CAPABILITY[name]
            reports.append(
                CapabilityReport(
                    name=name,
                    status="deferred",
                    reason=f"Intentionally deferred to {phase}.",
                )
            )
    return tuple(reports)


def _configured_image_status(
    config: Config,
) -> tuple[str, str, str, str]:
    if config.provider is None:
        reason = "The explicit configuration has no vision provider."
        return "unavailable", reason, "unavailable", reason
    if type(config.provider) is not str:
        return (
            "experimental",
            "An injected provider satisfies the offline protocol only; no stable live identity is proven.",
            "unavailable",
            "The explicit configuration does not select the built-in DashScope provider.",
        )
    if config.provider != "dashscope" or config.dashscope is None:
        reason = "The explicit configuration does not select a usable DashScope vision workflow."
        return "unavailable", reason, "unavailable", reason

    settings = config.dashscope
    is_exact_v17 = (
        (config.model is None or config.model == DEFAULT_DASHSCOPE_MODEL)
        and settings.region == "cn-beijing"
        and settings.base_url == "https://dashscope.aliyuncs.com/compatible-mode/v1"
        and settings.enable_thinking is True
        and settings.vl_high_resolution_images is True
        and settings.standalone_sign_scout_model == DEFAULT_DASHSCOPE_MODEL
    )
    if is_exact_v17:
        reason = (
            "The exact pinned Beijing v17 workflow passed live and packaging gates."
        )
        return "available", reason, "available", reason
    reason = (
        "The DashScope workflow is configured and offline-valid but differs from "
        "the exact live-proven v17 workflow."
    )
    return "experimental", reason, "experimental", reason
