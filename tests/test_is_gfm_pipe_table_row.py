"""Tests for conservative GFM pipe-table row protection."""

import pytest

from ocrllm.processors.is_gfm_pipe_table_row import is_gfm_pipe_table_row


@pytest.mark.parametrize(
    "line",
    (
        "| Run | Value |",
        "  | :--- | ---: |  ",
        "| A-01 | +0.18 |",
    ),
)
def test_outer_pipe_rows_are_protected(line):
    assert is_gfm_pipe_table_row(line) is True


@pytest.mark.parametrize("line", ("plain text", "A | B", "| incomplete", ""))
def test_non_rows_are_not_protected(line):
    assert is_gfm_pipe_table_row(line) is False


def test_nontext_row_is_rejected():
    with pytest.raises(ValueError, match="plain text"):
        is_gfm_pipe_table_row(None)  # type: ignore[arg-type]
