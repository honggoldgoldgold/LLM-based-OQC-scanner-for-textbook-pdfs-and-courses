"""Tests for the dependency-free board prompt contract."""

from ocrllm.profiles.build_board_prompt import (
    BOARD_PROMPT_VERSION,
    build_board_prompt,
)


def test_board_v7_declares_verified_transcription_without_fixture_specific_labels():
    prompt = build_board_prompt(("en-US", "zh-CN"), None)

    assert BOARD_PROMPT_VERSION == "board.v15"
    assert "LABEL: $formula$" in prompt
    assert "do not put labeled formulas in tables" in prompt
    assert "do not invent labels" in prompt
    assert "Unicode signs for relations embedded in prose" in prompt
    assert "use exactly ≤ and ≥" in prompt
    assert "Preserve handwritten spelling and capitalization exactly" in prompt
    assert "do not normalize or autocorrect it" in prompt
    assert "faint but visible diagram labels" in prompt
    assert "instead of silently omitting it" in prompt
    assert "internal region-by-region verification pass" in prompt
    assert "Count repeated standalone marks as separate visible occurrences" in prompt
    assert "do not infer new marks" in prompt
    assert "Do not interpret repeated hatch marks" in prompt
    assert "spatially distinct from drawing strokes" in prompt
    assert "F01" not in prompt
    assert "Expected input languages: en-US, zh-CN." in prompt
