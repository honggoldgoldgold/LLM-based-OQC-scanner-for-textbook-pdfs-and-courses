"""Recognize one ordered image group with the board profile."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

from ..config import Config
from ..errors import OCRLLMError
from ..processor_output import ProcessorOutput
from ..profiles.build_board_prompt import BOARD_PROMPT_VERSION, build_board_prompt
from ..profiles.build_board_review_prompt import build_board_review_prompt
from ..providers.call_vision_provider import call_vision_provider
from ..providers.resolve_vision_provider import resolve_vision_provider
from ..snapshot_config import snapshot_config


def recognize_images(
    image_paths: Sequence[Path],
    *,
    profile: str,
    config: Config,
) -> ProcessorOutput:
    """Call one injected vision provider and reject false-success output."""
    if type(config.provider) is str:
        config = snapshot_config(config)
    resolved_provider = resolve_vision_provider(config)
    base_prompt = build_board_prompt(config.input_languages, config.output_language)
    try:
        markdown = call_vision_provider(
            resolved_provider,
            image_paths,
            prompt=base_prompt,
            config=config,
        )
    except OCRLLMError as error:
        error._add_safe_detail("workflow_pass", "draft")
        error._add_safe_detail("provider_calls_attempted", 1)
        raise
    for _ in range(config.preferences.review_passes):
        try:
            markdown = call_vision_provider(
                resolved_provider,
                image_paths,
                prompt=build_board_review_prompt(base_prompt, markdown),
                config=config,
            )
        except OCRLLMError as error:
            error._add_safe_detail("workflow_pass", "review")
            error._add_safe_detail("provider_calls_attempted", 2)
            raise

    metadata: dict[str, str | int | bool | None] = {
        "image_count": len(image_paths),
        "model": resolved_provider.model,
        "prompt_version": BOARD_PROMPT_VERSION,
        "provider": resolved_provider.name,
        "profile": profile,
        "provider_call_count": 1 + config.preferences.review_passes,
        "review_passes": config.preferences.review_passes,
    }
    if resolved_provider.name == "dashscope" and config.dashscope is not None:
        metadata.update(
            {
                "provider_region": config.dashscope.region,
                "enable_thinking": config.dashscope.enable_thinking,
                "vl_high_resolution_images": (
                    config.dashscope.vl_high_resolution_images
                ),
            }
        )

    return ProcessorOutput(
        media_type="image",
        profile=profile,
        markdown=markdown,
        metadata=metadata,
    )
