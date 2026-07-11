"""Tests for fixed DashScope sign-scout thinking modes."""

import pytest

from ocrllm.errors import ConfigError
from ocrllm.providers.dashscope.resolve_sign_scout_enable_thinking import (
    resolve_sign_scout_enable_thinking,
)


def test_qwen_vl_scout_disables_thinking():
    assert resolve_sign_scout_enable_thinking("qwen-vl-max") is False


def test_pinned_qwen37_scout_enables_thinking():
    assert resolve_sign_scout_enable_thinking("qwen3.7-plus-2026-05-26") is True


def test_unpinned_scout_has_no_thinking_contract():
    with pytest.raises(ConfigError, match="thinking-mode contract"):
        resolve_sign_scout_enable_thinking("qwen3.7-plus")
