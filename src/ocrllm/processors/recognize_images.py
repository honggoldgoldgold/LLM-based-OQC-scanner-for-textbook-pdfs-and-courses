"""Recognize one ordered image group with the board profile."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

from ..config import Config
from ..errors import ConfigError, OCRLLMError, ProviderError
from ..processor_output import ProcessorOutput
from ..profiles.build_board_prompt import BOARD_PROMPT_VERSION, build_board_prompt
from ..providers.map_injected_provider_error import map_injected_provider_error
from ..providers.resolve_vision_provider import resolve_vision_provider
from ..providers.validate_provider_markdown import validate_provider_markdown
from ..raise_if_cancelled import raise_if_cancelled
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
    provider = resolved_provider.value

    lookup_error: ProviderError | OCRLLMError | None = None
    try:
        recognize_method = getattr(provider, "recognize_images", None)
    except Exception as error:
        lookup_error = map_injected_provider_error(error, model=resolved_provider.model)
    if lookup_error is not None:
        del provider
        raise lookup_error
    if not callable(recognize_method):
        del provider, recognize_method
        raise ConfigError(
            "Config.provider must be an injected object with a callable recognize_images method.",
            code="CONFIG_INVALID",
        )

    prompt = build_board_prompt(config.input_languages, config.output_language)
    raise_if_cancelled(config.cancellation)
    dispatch_error: OCRLLMError | None = None
    try:
        provider_value = recognize_method(tuple(image_paths), prompt=prompt, config=config)
    except Exception as error:
        if resolved_provider.built_in and isinstance(error, OCRLLMError):
            dispatch_error = error
        else:
            dispatch_error = map_injected_provider_error(
                error,
                model=resolved_provider.model,
            )
    if dispatch_error is not None:
        del provider, recognize_method
        raise dispatch_error

    validation_error: ProviderError | None = None
    try:
        markdown = validate_provider_markdown(provider_value)
    except ProviderError as error:
        validation_error = ProviderError(
            str(error),
            code=error.code,
            details={
                "model": resolved_provider.model,
                "provider": resolved_provider.name,
            },
        )
    if validation_error is not None:
        del provider, recognize_method, provider_value
        raise validation_error

    metadata: dict[str, str | int | bool | None] = {
        "image_count": len(image_paths),
        "model": resolved_provider.model,
        "prompt_version": BOARD_PROMPT_VERSION,
        "provider": resolved_provider.name,
        "profile": profile,
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
