from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

from ocrllm import CapabilityReport, Config, DashScopeSettings, get_capabilities
from ocrllm.errors import ConfigError
from ocrllm.providers.dashscope.resolve_dashscope_model import DEFAULT_DASHSCOPE_MODEL


EXPECTED_NAMES = (
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


def _by_name(config: Config | None = None) -> dict[str, CapabilityReport]:
    return {report.name: report for report in get_capabilities(config)}


def _proven_config(*, api_key: str | None = None) -> Config:
    return Config(
        provider="dashscope",
        api_key=api_key,
        model=DEFAULT_DASHSCOPE_MODEL,
        dashscope=DashScopeSettings(
            region="cn-beijing",
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            enable_thinking=True,
            vl_high_resolution_images=True,
            standalone_sign_scout_model=DEFAULT_DASHSCOPE_MODEL,
        ),
    )


def test_zero_argument_registry_is_complete_ordered_and_atomic() -> None:
    reports = get_capabilities()

    assert isinstance(reports, tuple)
    assert all(type(report) is CapabilityReport for report in reports)
    assert tuple(report.name for report in reports) == EXPECTED_NAMES
    assert len(set(EXPECTED_NAMES)) == len(EXPECTED_NAMES)
    assert {report.status for report in reports} <= {
        "available",
        "experimental",
        "unavailable",
        "deferred",
    }
    assert all(report.reason.strip() for report in reports)


def test_zero_argument_reports_local_image_gates_without_guessing_provider_region(
    monkeypatch,
) -> None:
    monkeypatch.setenv("DASHSCOPE_API_KEY", "secret-sentinel")
    reports = _by_name()

    assert reports["image.board.png"].status == "available"
    assert reports["image.board.jpeg"].status == "available"
    assert reports["provider.dashscope.vision"].status == "unavailable"
    assert "region" in reports["provider.dashscope.vision"].reason
    assert "secret-sentinel" not in repr(reports)


def test_exact_pinned_beijing_v17_configuration_is_available() -> None:
    reports = _by_name(_proven_config(api_key="secret-sentinel"))

    assert reports["image.board.png"].status == "available"
    assert reports["image.board.jpeg"].status == "available"
    assert reports["provider.dashscope.vision"].status == "available"
    assert "v17" in reports["provider.dashscope.vision"].reason
    assert "secret-sentinel" not in repr(reports)


def test_offline_valid_but_unproven_dashscope_workflow_is_experimental() -> None:
    config = Config(
        provider="dashscope",
        model="qwen3.7-plus",
        dashscope=DashScopeSettings(
            region="cn-beijing",
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        ),
    )
    reports = _by_name(config)

    assert reports["image.board.png"].status == "experimental"
    assert reports["provider.dashscope.vision"].status == "experimental"
    assert "differs" in reports["provider.dashscope.vision"].reason


def test_injected_provider_is_experimental_and_not_dashscope() -> None:
    reports = _by_name(Config(provider=object()))

    assert reports["image.board.png"].status == "experimental"
    assert reports["provider.dashscope.vision"].status == "unavailable"


def test_explicit_providerless_config_is_unavailable() -> None:
    reports = _by_name(Config())

    assert reports["image.board.png"].status == "unavailable"
    assert reports["provider.dashscope.vision"].status == "unavailable"


def test_current_worker_is_experimental_and_later_phases_are_deferred() -> None:
    reports = _by_name()

    assert reports["worker.jsonl.v1alpha1"].status == "experimental"
    for name in EXPECTED_NAMES[6:]:
        assert reports[name].status == "deferred"


def test_get_capabilities_freshly_revalidates_exact_config() -> None:
    config = _proven_config()
    assert config.dashscope is not None
    object.__setattr__(config.dashscope, "region", "cn-hongkong")

    with pytest.raises(ConfigError, match="same DashScope region"):
        get_capabilities(config)


def test_get_capabilities_rejects_config_subclasses() -> None:
    class ConfigSubclass(Config):
        pass

    with pytest.raises(ConfigError, match="exact Config"):
        get_capabilities(ConfigSubclass())


def test_capability_query_loads_no_optional_packages_or_network_stack() -> None:
    source_root = Path(__file__).resolve().parents[1] / "src"
    probe = (
        "import sys; sys.path.insert(0,sys.argv[1]); "
        "import ocrllm; reports=ocrllm.get_capabilities(); assert len(reports)==19; "
        "loaded={name.split('.')[0] for name in sys.modules}; "
        "forbidden={'PIL','pypdfium2','openai','httpx','socket'}; "
        "assert not loaded & forbidden, loaded & forbidden"
    )
    environment = os.environ.copy()
    environment["DASHSCOPE_API_KEY"] = "secret-sentinel"

    completed = subprocess.run(
        [sys.executable, "-I", "-c", probe, str(source_root)],
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
        env=environment,
    )

    assert completed.returncode == 0, completed.stderr
    assert "secret-sentinel" not in completed.stdout + completed.stderr
