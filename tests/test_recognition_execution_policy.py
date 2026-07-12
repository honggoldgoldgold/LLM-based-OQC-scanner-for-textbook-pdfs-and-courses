from dataclasses import FrozenInstanceError

import pytest

from ocrllm import Config, RecognitionExecutionPolicy, recognize
from ocrllm.errors import ConfigError, InvalidSource


class CountingProvider:
    def __init__(self) -> None:
        self.calls = []

    def recognize_images(self, image_paths, *, prompt, config):
        self.calls.append(tuple(image_paths))
        return "# Unexpected provider call\n"


def test_execution_policy_defaults_are_safe_and_immutable():
    policy = RecognitionExecutionPolicy()

    assert policy.maximum_images_per_request == 10
    assert policy.max_parallel_requests == 1
    assert policy.provider_request_start_interval_seconds == 0.0
    assert Config().execution == policy
    assert not hasattr(policy, "__dict__")
    with pytest.raises(FrozenInstanceError):
        policy.max_parallel_requests = 2  # type: ignore[misc]


@pytest.mark.parametrize(
    ("field_name", "bad_value"),
    [
        ("maximum_images_per_request", True),
        ("maximum_images_per_request", 0),
        ("maximum_images_per_request", 11),
        ("maximum_images_per_request", 1.0),
        ("max_parallel_requests", True),
        ("max_parallel_requests", 0),
        ("max_parallel_requests", 33),
        ("max_parallel_requests", 1.0),
        ("provider_request_start_interval_seconds", True),
        ("provider_request_start_interval_seconds", -0.01),
        ("provider_request_start_interval_seconds", 600.1),
        ("provider_request_start_interval_seconds", float("nan")),
        ("provider_request_start_interval_seconds", float("inf")),
        ("provider_request_start_interval_seconds", "0.5"),
    ],
)
def test_execution_policy_rejects_invalid_or_unbounded_values(field_name, bad_value):
    kwargs = {field_name: bad_value}

    with pytest.raises(ConfigError, match=field_name) as captured:
        RecognitionExecutionPolicy(**kwargs)

    assert captured.value.code == "CONFIG_INVALID"


def test_config_requires_an_exact_execution_policy():
    class PolicySubclass(RecognitionExecutionPolicy):
        pass

    with pytest.raises(ConfigError, match="exact RecognitionExecutionPolicy"):
        Config(execution=PolicySubclass())

    with pytest.raises(ConfigError, match="exact RecognitionExecutionPolicy"):
        Config(execution=object())  # type: ignore[arg-type]


def test_config_revalidates_a_mutated_execution_policy():
    policy = RecognitionExecutionPolicy(max_parallel_requests=2)
    object.__setattr__(policy, "max_parallel_requests", 0)

    with pytest.raises(ConfigError, match="max_parallel_requests"):
        Config(execution=policy)


def test_config_owns_a_revalidated_execution_policy_snapshot():
    policy = RecognitionExecutionPolicy(
        maximum_images_per_request=3,
        max_parallel_requests=2,
        provider_request_start_interval_seconds=1,
    )

    config = Config(execution=policy)

    assert config.execution == policy
    assert config.execution is not policy
    assert config.execution.provider_request_start_interval_seconds == 1.0


def test_configured_image_limit_fails_before_file_or_provider_access(tmp_path):
    provider = CountingProvider()
    missing_sources = (tmp_path / "missing-a.png", tmp_path / "missing-b.png")
    config = Config(
        provider=provider,
        execution=RecognitionExecutionPolicy(maximum_images_per_request=1),
    )

    with pytest.raises(InvalidSource) as captured:
        recognize(missing_sources, config=config)

    assert captured.value.code == "SOURCE_TOO_LARGE"
    assert captured.value.details == {
        "image_count": 2,
        "maximum_image_count": 1,
        "limit_source": "recognition_execution_policy",
    }
    assert provider.calls == []


def test_configured_image_limit_accepts_the_exact_boundary(tmp_path):
    provider = CountingProvider()
    source = tmp_path / "missing.png"
    config = Config(
        provider=provider,
        execution=RecognitionExecutionPolicy(maximum_images_per_request=1),
    )

    with pytest.raises(InvalidSource) as captured:
        recognize(source, config=config)

    assert captured.value.code == "SOURCE_NOT_FOUND"
    assert provider.calls == []
