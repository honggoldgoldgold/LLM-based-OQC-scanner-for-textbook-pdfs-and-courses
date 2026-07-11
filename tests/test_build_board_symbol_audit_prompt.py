"""Tests for the complete-board silent symbol-audit prompt."""

import pytest

from ocrllm.profiles.build_board_symbol_audit_prompt import (
    build_board_symbol_audit_prompt,
)


def test_symbol_audit_prompt_keeps_full_transcription_and_rejects_texture():
    prompt = build_board_symbol_audit_prompt("Transcribe every source image.")

    assert prompt.startswith("Transcribe every source image.")
    assert "silently inventory every text-bearing region" in prompt
    assert "standalone visible sign or operator" in prompt
    assert "Preserve exact case, identifiers" in prompt
    assert "hatch, fill, shading, and texture strokes" in prompt
    assert prompt.endswith("Return only complete Markdown.")


@pytest.mark.parametrize("value", ("", "  ", None, b"prompt"))
def test_symbol_audit_prompt_rejects_nonempty_nonexact_text(value):
    with pytest.raises(ValueError, match="base_prompt"):
        build_board_symbol_audit_prompt(value)  # type: ignore[arg-type]
