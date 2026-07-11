"""Tests for deterministic two-scout standalone-sign restoration."""

import pytest

from ocrllm.processors.restore_quorum_standalone_signs import (
    RestoredStandaloneSigns,
    restore_quorum_standalone_signs,
)


SCOUT_ONE = "+ | foreign gene | I:V\n+ | Transformation | Validation"
SCOUT_TWO = "+ | Ligase join | I:V 3:1 Ratio\n+ | Transformation. | Validation"
SCOUT_THREE = "+ | foreign gene | I:V 3:1 Ratio\n+ | Transformation. | Validation"


def test_quorum_restores_one_missing_sign_without_copying_scout_prose():
    base = "foreign gene\nI:V 3:1 Ratio\nTransformation.\n+\nValidation\n"

    result = restore_quorum_standalone_signs(base, (SCOUT_ONE, SCOUT_TWO))

    assert result == RestoredStandaloneSigns(
        markdown=(
            "foreign gene\n+\nI:V 3:1 Ratio\nTransformation.\n+\nValidation\n"
        ),
        restored_count=1,
    )
    assert "Ligase join" not in result.markdown


def test_quorum_counts_inline_isolated_sign_and_leaves_correct_base_byte_identical():
    base = "foreign gene\n+\nI:V 3:1 Ratio\nTransformation.\n+ Validation\n"

    result = restore_quorum_standalone_signs(base, (SCOUT_ONE, SCOUT_TWO))

    assert result == RestoredStandaloneSigns(markdown=base, restored_count=0)


def test_nonquorum_sign_is_not_restored():
    base = "foreign gene\nI:V 3:1 Ratio\n"
    first = "+ | foreign gene | I:V"
    second = "- | Validation | Selection"

    result = restore_quorum_standalone_signs(base, (first, second))

    assert result == RestoredStandaloneSigns(markdown=base, restored_count=0)


def test_unmatched_quorum_anchors_cannot_inject_a_sign():
    base = "unrelated base\n"

    result = restore_quorum_standalone_signs(base, (SCOUT_ONE, SCOUT_TWO))

    assert result == RestoredStandaloneSigns(markdown=base, restored_count=0)


@pytest.mark.parametrize(
    ("base", "scouts"),
    (
        ("", ("a", "b")),
        ("a", ("", "b")),
        ("a", ("b", None)),
        ("a", ["b", "c"]),
        ("a", ("only-one",)),
    ),
)
def test_restore_rejects_empty_or_nonexact_inputs(base, scouts):
    with pytest.raises(ValueError, match="must"):
        restore_quorum_standalone_signs(base, scouts)  # type: ignore[arg-type]


def test_two_of_three_quorum_restores_when_one_scout_omits_the_sign():
    base = "foreign gene\nI:V 3:1 Ratio\nTransformation.\n+\nValidation\n"
    missing = "- | Validation | Selection"

    result = restore_quorum_standalone_signs(
        base,
        (missing, SCOUT_TWO, SCOUT_THREE),
        minimum_agreement=2,
    )

    assert result.restored_count == 1
    assert result.markdown.count("\n+\n") == 2


def test_markdown_thematic_breaks_are_rejected_as_invalid_ledger_signs():
    base = "first source\nsecond source\n"
    scout = "--- | first source | second source"

    with pytest.raises(ValueError, match="unsupported sign"):
        restore_quorum_standalone_signs(
            base,
            (scout, scout, scout),
            minimum_agreement=2,
        )


@pytest.mark.parametrize("minimum", (True, 0, 1, 4, "2"))
def test_restore_rejects_invalid_minimum_agreement(minimum):
    with pytest.raises(ValueError, match="minimum_agreement"):
        restore_quorum_standalone_signs(
            "base",
            (SCOUT_ONE, SCOUT_TWO, SCOUT_THREE),
            minimum_agreement=minimum,  # type: ignore[arg-type]
        )
