"""Tests for allowlisted record extraction from untrusted scout responses."""

import pytest

from ocrllm.processors.extract_supported_standalone_sign_events import (
    extract_supported_standalone_sign_events,
)
from ocrllm.processors.parse_standalone_sign_ledger import StandaloneSignEvent


def test_extractor_keeps_exact_supported_rows_and_discards_other_punctuation():
    response = (
        "+ | foreign gene | I:V\n"
        "/ | R-DNA | Replasmid\n"
        ": | Nuclease | Cut\n"
        "+ | Transformation | Validation\n"
        "+ | foreign gene | I:V"
    )

    assert extract_supported_standalone_sign_events(response) == (
        StandaloneSignEvent("+", "foreigngene", "iv"),
        StandaloneSignEvent("+", "transformation", "validation"),
    )


def test_extractor_preserves_exact_none_as_valid_empty_evidence():
    assert extract_supported_standalone_sign_events("NONE") == ()


@pytest.mark.parametrize(
    "response",
    ("/ | R-DNA | Replasmid", "heading only", "", None),
)
def test_extractor_rejects_responses_without_any_supported_exact_record(response):
    with pytest.raises(ValueError, match="standalone-sign response"):
        extract_supported_standalone_sign_events(response)  # type: ignore[arg-type]
