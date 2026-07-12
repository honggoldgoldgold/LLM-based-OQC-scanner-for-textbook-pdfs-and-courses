"""Call one resolved vision provider and validate one Markdown response."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

from ..config import Config
from ..errors import ConfigError, OCRLLMError, ProviderError
from .map_injected_provider_error import map_injected_provider_error
from .provider_request_start_gate import wait_for_provider_request_start
from .resolved_vision_provider import ResolvedVisionProvider
from .validate_provider_markdown import validate_provider_markdown


def call_vision_provider(
    resolved_provider: ResolvedVisionProvider,
    image_paths: Sequence[Path],
    *,
    prompt: str,
    config: Config,
) -> str:
    """Return one complete provider response or one redacted typed failure."""

    provider = resolved_provider.value
    lookup_error: ProviderError | OCRLLMError | None = None
    try:
        recognize_method = getattr(provider, "recognize_images", None)
    except Exception as error:
        lookup_error = map_injected_provider_error(
            error,
            model=resolved_provider.model,
        )
    if lookup_error is not None:
        del provider
        raise lookup_error
    if not callable(recognize_method):
        del provider, recognize_method
        raise ConfigError(
            "Config.provider must be an injected object with a callable recognize_images method.",
            code="CONFIG_INVALID",
        )

    wait_for_provider_request_start(config.cancellation)
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
    return markdown
