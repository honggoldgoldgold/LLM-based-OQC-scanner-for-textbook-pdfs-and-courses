"""Recognize one ordered image group with the board profile."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

from ..config import Config
from ..errors import ConfigError, OCRLLMError, ProviderError
from ..processor_output import ProcessorOutput
from ..profiles.build_board_prompt import build_board_prompt
from ..providers.map_injected_provider_error import map_injected_provider_error
from ..providers.validate_provider_markdown import validate_provider_markdown


def recognize_images(
    image_paths: Sequence[Path],
    *,
    profile: str,
    config: Config,
) -> ProcessorOutput:
    """Call one injected vision provider and reject false-success output."""
    provider = config.provider
    if provider is None or isinstance(provider, str):
        error_code = "CONFIG_MISSING" if provider is None else "CONFIG_INVALID"
        del provider
        raise ConfigError(
            "Config.provider must be an injected object with a callable recognize_images method.",
            code=error_code,
        )

    lookup_error: ProviderError | OCRLLMError | None = None
    try:
        recognize_method = getattr(provider, "recognize_images", None)
    except Exception as error:
        lookup_error = map_injected_provider_error(error, model=config.model)
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
    dispatch_error: OCRLLMError | None = None
    try:
        provider_value = recognize_method(tuple(image_paths), prompt=prompt, config=config)
    except Exception as error:
        dispatch_error = map_injected_provider_error(error, model=config.model)
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
            details={"model": config.model},
        )
    if validation_error is not None:
        del provider, recognize_method, provider_value
        raise validation_error

    return ProcessorOutput(
        media_type="image",
        profile=profile,
        markdown=markdown,
        metadata={
            "image_count": len(image_paths),
            "model": config.model,
            "profile": profile,
        },
    )
