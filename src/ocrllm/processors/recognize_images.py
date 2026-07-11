"""Recognize one ordered image group with the board profile."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

from ..config import Config
from ..errors import OCRLLMError
from ..processor_output import ProcessorOutput
from ..profiles.build_board_consensus_prompt import build_board_consensus_prompt
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
    drafts: list[str] = []
    for candidate_index in range(config.preferences.draft_candidates):
        try:
            drafts.append(call_vision_provider(
                resolved_provider,
                image_paths,
                prompt=base_prompt,
                config=config,
            ))
        except OCRLLMError as error:
            error._add_safe_detail(
                "workflow_pass",
                "draft" if candidate_index == 0 else "draft_2",
            )
            error._add_safe_detail("provider_calls_attempted", candidate_index + 1)
            raise

    markdown = drafts[0]
    if config.preferences.review_passes:
        consensus = config.preferences.draft_candidates == 2
        review_prompt = (
            build_board_consensus_prompt(base_prompt, (drafts[0], drafts[1]))
            if consensus
            else build_board_review_prompt(base_prompt, drafts[0])
        )
        try:
            markdown = call_vision_provider(
                resolved_provider,
                image_paths,
                prompt=review_prompt,
                config=config,
            )
        except OCRLLMError as error:
            error._add_safe_detail(
                "workflow_pass",
                "consensus_review" if consensus else "review",
            )
            error._add_safe_detail(
                "provider_calls_attempted",
                config.preferences.draft_candidates + 1,
            )
            raise

    provider_call_count = (
        config.preferences.draft_candidates + config.preferences.review_passes
    )
    metadata: dict[str, str | int | bool | None] = {
        "image_count": len(image_paths),
        "model": resolved_provider.model,
        "prompt_version": BOARD_PROMPT_VERSION,
        "provider": resolved_provider.name,
        "profile": profile,
        "provider_call_count": provider_call_count,
        "draft_candidates": config.preferences.draft_candidates,
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
