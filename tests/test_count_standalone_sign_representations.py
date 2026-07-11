"""Tests for source-equivalent standalone-sign representation counts."""

import pytest

from ocrllm.processors.count_standalone_sign_representations import (
    count_standalone_sign_representations,
)


@pytest.mark.parametrize(
    "markdown",
    (
        "TARGET RECALL: ≥ 95%",
        "TARGET RECALL: >= 95%",
        r"TARGET RECALL: $\ge 95\%$",
        r"TARGET RECALL: \(\geq 95\%\)",
        r"TARGET RECALL: $\geqslant 95\%$",
    ),
)
def test_count_treats_unicode_ascii_and_latex_greater_equal_as_equivalent(markdown):
    assert count_standalone_sign_representations(markdown, "≥") == 1
    assert count_standalone_sign_representations(markdown, ">=") == 1


def test_count_keeps_embedded_table_value_plus_out_of_standalone_plus_count():
    markdown = "| A-01 | +0.18 |\n+\n"

    assert count_standalone_sign_representations(markdown, "+") == 1


@pytest.mark.parametrize(("markdown", "sign"), ((None, "+"), ("text", "*")))
def test_count_rejects_invalid_inputs(markdown, sign):
    with pytest.raises(ValueError):
        count_standalone_sign_representations(markdown, sign)  # type: ignore[arg-type]
