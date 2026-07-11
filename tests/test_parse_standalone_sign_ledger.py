"""Tests for strict parsing of untrusted standalone-sign ledgers."""

import pytest

from ocrllm.processors.parse_standalone_sign_ledger import (
    StandaloneSignEvent,
    parse_standalone_sign_ledger,
)


def test_parser_returns_exact_signs_and_normalized_neighbor_anchors():
    ledger = "+ | foreign gene | I:V\n- | NONE | Selection"

    assert parse_standalone_sign_ledger(ledger) == (
        StandaloneSignEvent("+", "foreigngene", "iv"),
        StandaloneSignEvent("-", "", "selection"),
    )


@pytest.mark.parametrize(
    "ledger",
    (
        "# Signs\n+ | foreign gene | I:V",
        "```\n+ | foreign gene | I:V\n```",
        "--- | foreign gene | I:V",
        "+|foreign gene|I:V",
        "+ | one two three four five six | I:V",
        "+ | NONE | NONE",
        "+ | --- | I:V",
        "* | foreign gene | I:V",
    ),
)
def test_parser_rejects_extra_prose_unsafe_signs_and_invalid_neighbors(ledger):
    with pytest.raises(ValueError, match="standalone-sign ledger"):
        parse_standalone_sign_ledger(ledger)


@pytest.mark.parametrize("ledger", ("", "  ", None, b"ledger"))
def test_parser_rejects_empty_or_nonexact_input(ledger):
    with pytest.raises(ValueError, match="nonempty plain text"):
        parse_standalone_sign_ledger(ledger)  # type: ignore[arg-type]
