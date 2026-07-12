"""Immutable limits for one recognition workflow."""

from __future__ import annotations

import math
from dataclasses import dataclass

from .errors import ConfigError
from .image_group_limits import MAX_IMAGE_GROUP_COUNT


MAX_PARALLEL_REQUESTS = 32
MAX_REQUEST_START_INTERVAL_SECONDS = 600.0


@dataclass(frozen=True, slots=True)
class RecognitionExecutionPolicy:
    """Bound image groups, concurrent jobs, and provider dispatch cadence."""

    maximum_images_per_request: int = MAX_IMAGE_GROUP_COUNT
    max_parallel_requests: int = 1
    provider_request_start_interval_seconds: float = 0.0

    def __post_init__(self) -> None:
        if (
            type(self.maximum_images_per_request) is not int
            or not 1
            <= self.maximum_images_per_request
            <= MAX_IMAGE_GROUP_COUNT
        ):
            raise ConfigError(
                "RecognitionExecutionPolicy.maximum_images_per_request must be "
                f"an integer in [1, {MAX_IMAGE_GROUP_COUNT}].",
                code="CONFIG_INVALID",
            ) from None
        if (
            type(self.max_parallel_requests) is not int
            or not 1 <= self.max_parallel_requests <= MAX_PARALLEL_REQUESTS
        ):
            raise ConfigError(
                "RecognitionExecutionPolicy.max_parallel_requests must be an "
                f"integer in [1, {MAX_PARALLEL_REQUESTS}].",
                code="CONFIG_INVALID",
            ) from None

        interval = self.provider_request_start_interval_seconds
        if isinstance(interval, bool) or not isinstance(interval, (int, float)):
            raise ConfigError(
                "RecognitionExecutionPolicy.provider_request_start_interval_seconds "
                "must be a finite number.",
                code="CONFIG_INVALID",
            ) from None
        normalized_interval = float(interval)
        if (
            not math.isfinite(normalized_interval)
            or not 0.0
            <= normalized_interval
            <= MAX_REQUEST_START_INTERVAL_SECONDS
        ):
            raise ConfigError(
                "RecognitionExecutionPolicy.provider_request_start_interval_seconds "
                f"must be in [0, {MAX_REQUEST_START_INTERVAL_SECONDS:g}].",
                code="CONFIG_INVALID",
            ) from None
        object.__setattr__(
            self,
            "provider_request_start_interval_seconds",
            normalized_interval,
        )
