"""Tests for the strict standalone-sign ledger prompt."""

from ocrllm.profiles.build_board_sign_scout_prompt import (
    build_board_sign_scout_prompt,
)


def test_sign_scout_prompt_requires_only_bounded_plain_text_records():
    prompt = build_board_sign_scout_prompt()

    assert "SIGN | BEFORE | AFTER" in prompt
    assert "at most five words each" in prompt
    assert "Do not transcribe other content" in prompt
    assert "Do not output headings, bullets, fences" in prompt
    assert "Markdown separators" in prompt
