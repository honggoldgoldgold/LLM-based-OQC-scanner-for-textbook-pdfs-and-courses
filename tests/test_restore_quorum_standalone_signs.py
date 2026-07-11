"""Tests for deterministic multi-scout standalone-sign restoration."""

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
        abstained_scout_count=0,
    )
    assert "Ligase join" not in result.markdown


def test_quorum_counts_inline_isolated_sign_and_leaves_correct_base_byte_identical():
    base = "foreign gene\n+\nI:V 3:1 Ratio\nTransformation.\n+ Validation\n"

    result = restore_quorum_standalone_signs(base, (SCOUT_ONE, SCOUT_TWO))

    assert result == RestoredStandaloneSigns(
        markdown=base,
        restored_count=0,
        abstained_scout_count=0,
    )


def test_nonquorum_sign_is_not_restored():
    base = "foreign gene\nI:V 3:1 Ratio\n"
    first = "+ | foreign gene | I:V"
    second = "- | Validation | Selection"

    result = restore_quorum_standalone_signs(base, (first, second))

    assert result == RestoredStandaloneSigns(
        markdown=base,
        restored_count=0,
        abstained_scout_count=0,
    )


def test_unmatched_quorum_anchors_cannot_inject_a_sign():
    base = "unrelated base\n"

    result = restore_quorum_standalone_signs(base, (SCOUT_ONE, SCOUT_TWO))

    assert result == RestoredStandaloneSigns(
        markdown=base,
        restored_count=0,
        abstained_scout_count=0,
    )


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


def test_two_valid_scouts_restore_while_one_malformed_scout_abstains():
    base = "foreign gene\nI:V 3:1 Ratio\n"

    result = restore_quorum_standalone_signs(
        base,
        (SCOUT_ONE, SCOUT_THREE, "# invalid scout prose"),
        minimum_agreement=2,
    )

    assert result.markdown == "foreign gene\n+\nI:V 3:1 Ratio\n"
    assert result.restored_count == 1
    assert result.abstained_scout_count == 1


def test_invalid_thematic_break_ledgers_abstain_without_mutating_the_primary():
    base = "first source\nsecond source\n"
    scout = "--- | first source | second source"

    result = restore_quorum_standalone_signs(
        base,
        (scout, scout, scout),
        minimum_agreement=2,
    )

    assert result == RestoredStandaloneSigns(
        markdown=base,
        restored_count=0,
        abstained_scout_count=3,
    )


def test_exact_none_is_valid_empty_evidence_not_an_abstention():
    base = "first source\nsecond source\n"

    result = restore_quorum_standalone_signs(
        base,
        ("NONE", "NONE", "NONE"),
        minimum_agreement=2,
    )

    assert result.abstained_scout_count == 0
    assert result.markdown == base


def test_existing_different_sign_blocks_conflicting_restoration_at_same_anchors():
    base = "- Selection\n- Screening\n"
    false_plus = "+ | Selection | Screening"

    result = restore_quorum_standalone_signs(
        base,
        (false_plus, false_plus, "NONE"),
        minimum_agreement=2,
    )

    assert result == RestoredStandaloneSigns(
        markdown=base,
        restored_count=0,
        abstained_scout_count=0,
    )


def test_latex_equivalent_relation_blocks_duplicate_unicode_restoration():
    base = "TARGET RECALL: $\\ge 95\\%$\nOUTPUT\nLATENCY P95: 180 ms\n"
    duplicate = "≥ | OUTPUT | LATENCY P95"

    result = restore_quorum_standalone_signs(
        base,
        (duplicate, duplicate, "NONE"),
        minimum_agreement=2,
    )

    assert result == RestoredStandaloneSigns(
        markdown=base,
        restored_count=0,
        abstained_scout_count=0,
    )


def test_sign_restoration_cannot_split_gfm_pipe_table_rows():
    base = (
        "| Run | Drift |\n"
        "| --- | --- |\n"
        "| A-01 | +0.18 |\n"
        "| A-02 | -0.07 |\n"
    )
    row_sign = "+ | A-01 | A-02"

    result = restore_quorum_standalone_signs(
        base,
        (row_sign, row_sign, row_sign),
        minimum_agreement=2,
    )

    assert result == RestoredStandaloneSigns(
        markdown=base,
        restored_count=0,
        abstained_scout_count=0,
    )


@pytest.mark.parametrize("minimum", (True, 0, 1, 4, "2"))
def test_restore_rejects_invalid_minimum_agreement(minimum):
    with pytest.raises(ValueError, match="minimum_agreement"):
        restore_quorum_standalone_signs(
            "base",
            (SCOUT_ONE, SCOUT_TWO, SCOUT_THREE),
            minimum_agreement=minimum,  # type: ignore[arg-type]
        )
