"""Recognize one ordered image group with the board profile."""

from __future__ import annotations

import hashlib
from collections.abc import Sequence
from dataclasses import replace
from pathlib import Path

from ..config import Config
from ..errors import OCRLLMError, ProviderError
from ..processor_output import ProcessorOutput
from ..profiles.build_board_consensus_prompt import build_board_consensus_prompt
from ..profiles.build_board_prompt import BOARD_PROMPT_VERSION, build_board_prompt
from ..profiles.build_board_review_prompt import build_board_review_prompt
from ..profiles.build_board_sign_scout_prompt import (
    SIGN_SCOUT_PROMPT_VERSION,
    build_board_sign_scout_prompt,
)
from ..profiles.build_board_symbol_audit_prompt import build_board_symbol_audit_prompt
from ..providers.call_vision_provider import call_vision_provider
from ..providers.dashscope.resolve_sign_scout_enable_thinking import (
    resolve_sign_scout_enable_thinking,
)
from ..providers.resolve_vision_provider import resolve_vision_provider
from ..snapshot_config import snapshot_config
from .restore_quorum_standalone_signs import restore_quorum_standalone_signs


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
    scout_model = (
        config.dashscope.standalone_sign_scout_model
        if config.dashscope is not None
        else None
    )
    primary_prompt = (
        build_board_symbol_audit_prompt(base_prompt)
        if scout_model is not None
        else base_prompt
    )
    drafts: list[str] = []
    for candidate_index in range(config.preferences.draft_candidates):
        try:
            drafts.append(call_vision_provider(
                resolved_provider,
                image_paths,
                prompt=primary_prompt,
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
    restored_sign_count = 0
    abstained_scout_count = 0
    scout_prompt: str | None = None
    if scout_model is not None:
        assert config.dashscope is not None
        scout_enable_thinking = resolve_sign_scout_enable_thinking(scout_model)
        scout_config = replace(
            config,
            model=scout_model,
            dashscope=replace(
                config.dashscope,
                enable_thinking=scout_enable_thinking,
                standalone_sign_scout_model=None,
            ),
        )
        resolved_scout = resolve_vision_provider(scout_config)
        scout_prompt = build_board_sign_scout_prompt(markdown)
        scouts: list[str] = []
        for scout_index in range(3):
            try:
                scouts.append(
                    call_vision_provider(
                        resolved_scout,
                        image_paths,
                        prompt=scout_prompt,
                        config=scout_config,
                    )
                )
            except OCRLLMError as error:
                error._add_safe_detail(
                    "workflow_pass",
                    f"standalone_sign_scout_{scout_index + 1}",
                )
                error._add_safe_detail(
                    "provider_calls_attempted",
                    provider_call_count + scout_index + 1,
                )
                raise
        try:
            restored = restore_quorum_standalone_signs(
                markdown,
                tuple(scouts),
                minimum_agreement=2,
            )
        except ValueError:
            raise ProviderError(
                "The standalone-sign scout responses could not be merged safely.",
                code="PROVIDER_RESPONSE_INVALID",
                details={
                    "model": scout_model,
                    "provider": resolved_scout.name,
                    "provider_calls_attempted": provider_call_count + 3,
                    "workflow_pass": "standalone_sign_merge",
                },
            ) from None
        markdown = restored.markdown
        restored_sign_count = restored.restored_count
        abstained_scout_count = restored.abstained_scout_count
        provider_call_count += 3

    metadata: dict[str, str | int | bool | None] = {
        "image_count": len(image_paths),
        "model": resolved_provider.model,
        "prompt_version": BOARD_PROMPT_VERSION,
        "provider": resolved_provider.name,
        "profile": profile,
        "provider_call_count": provider_call_count,
        "draft_candidates": config.preferences.draft_candidates,
        "review_passes": config.preferences.review_passes,
        "standalone_sign_scout_model": scout_model,
        "standalone_sign_scout_count": 3 if scout_model is not None else 0,
        "standalone_signs_restored": restored_sign_count,
        "standalone_sign_scout_abstention_count": abstained_scout_count,
        "standalone_sign_scout_prompt_version": (
            SIGN_SCOUT_PROMPT_VERSION if scout_prompt is not None else None
        ),
        "standalone_sign_scout_prompt_sha256": (
            hashlib.sha256(scout_prompt.encode("utf-8")).hexdigest()
            if scout_prompt is not None
            else None
        ),
        "standalone_sign_scout_prompt_utf8_bytes": (
            len(scout_prompt.encode("utf-8")) if scout_prompt is not None else None
        ),
    }
    if resolved_provider.name == "dashscope" and config.dashscope is not None:
        metadata.update(
            {
                "provider_region": config.dashscope.region,
                "enable_thinking": config.dashscope.enable_thinking,
                "vl_high_resolution_images": (
                    config.dashscope.vl_high_resolution_images
                ),
                "standalone_sign_scout_enable_thinking": (
                    scout_enable_thinking if scout_model is not None else None
                ),
            }
        )

    return ProcessorOutput(
        media_type="image",
        profile=profile,
        markdown=markdown,
        metadata=metadata,
    )
