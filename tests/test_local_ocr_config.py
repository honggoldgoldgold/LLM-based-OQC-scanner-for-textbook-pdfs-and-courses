from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from ocrllm import (
    Config,
    DashScopeSettings,
    LocalOCRSettings,
    RecognitionPreferences,
    VisionModelSettings,
)
from ocrllm.errors import ConfigError


def test_local_ocr_settings_are_frozen_slotted_and_normalized() -> None:
    settings = LocalOCRSettings(minimum_confidence=1)

    assert settings.minimum_confidence == 1.0
    assert not hasattr(settings, "__dict__")
    with pytest.raises(FrozenInstanceError):
        settings.minimum_confidence = 0.5  # type: ignore[misc]


@pytest.mark.parametrize(
    "value",
    [True, -0.01, 1.01, float("nan"), float("inf"), "0.5"],
)
def test_local_ocr_settings_reject_invalid_confidence(value) -> None:
    with pytest.raises(ConfigError, match="minimum_confidence"):
        LocalOCRSettings(minimum_confidence=value)  # type: ignore[arg-type]


def test_ocr_mode_constructs_default_settings_without_provider_fields() -> None:
    config = Config(image_mode="ocr")

    assert config.image_mode == "ocr"
    assert config.local_ocr == LocalOCRSettings()
    assert config.provider is None
    assert config.vision_model == VisionModelSettings()


def test_ocr_mode_revalidates_and_copies_exact_settings() -> None:
    settings = LocalOCRSettings(minimum_confidence=0.75)

    config = Config(image_mode="ocr", local_ocr=settings)

    assert config.local_ocr == settings
    assert config.local_ocr is not settings


def test_vision_mode_rejects_local_ocr_settings() -> None:
    with pytest.raises(ConfigError, match="only when image_mode='ocr'"):
        Config(local_ocr=LocalOCRSettings())


@pytest.mark.parametrize("value", [None, "local_ocr", "OCR", 1, True])
def test_config_rejects_unknown_or_nontext_image_mode(value) -> None:
    with pytest.raises(ConfigError, match="image_mode"):
        Config(image_mode=value)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "kwargs",
    [
        {"provider": object()},
        {
            "provider": DashScopeSettings(
                region="cn-beijing",
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            ),
        },
        {"vision_model": VisionModelSettings(name="model-sentinel")},
        {"preferences": RecognitionPreferences(review_passes=1)},
        {"input_languages": ("zh-Hans",)},
        {"output_language": "en"},
    ],
)
def test_ocr_mode_rejects_fields_that_would_be_silently_ignored(kwargs) -> None:
    with pytest.raises(ConfigError):
        Config(image_mode="ocr", **kwargs)


def test_ocr_mode_accepts_resume_with_output_directory(tmp_path) -> None:
    config = Config(image_mode="ocr", resume=True, output_dir=tmp_path)

    assert config.resume is True


def test_config_rejects_local_ocr_settings_subclass() -> None:
    class SettingsSubclass(LocalOCRSettings):
        pass

    with pytest.raises(ConfigError, match="exact LocalOCRSettings"):
        Config(image_mode="ocr", local_ocr=SettingsSubclass())


def test_config_revalidates_mutated_local_ocr_settings() -> None:
    settings = LocalOCRSettings()
    object.__setattr__(settings, "minimum_confidence", 2)

    with pytest.raises(ConfigError, match="minimum_confidence"):
        Config(image_mode="ocr", local_ocr=settings)
