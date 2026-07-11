"""Tests for deterministic two-scout standalone-sign restoration."""

import pytest

from ocrllm.processors.restore_quorum_standalone_signs import (
    RestoredStandaloneSigns,
    restore_quorum_standalone_signs,
)


SCOUT_ONE = """foreign gene

+

I:V
Transformation
+
Validation
"""
SCOUT_TWO = """Ligase join
+
I:V 3:1 Ratio
Transformation.
+
Validation
"""


def test_quorum_restores_one_missing_sign_without_copying_scout_prose():
    base = "foreign gene\nI:V 3:1 Ratio\nTransformation.\n+\nValidation\n"

    result = restore_quorum_standalone_signs(base, SCOUT_ONE, SCOUT_TWO)

    assert result == RestoredStandaloneSigns(
        markdown=(
            "foreign gene\n+\nI:V 3:1 Ratio\nTransformation.\n+\nValidation\n"
        ),
        restored_count=1,
    )
    assert "Ligase join" not in result.markdown


def test_quorum_counts_inline_isolated_sign_and_leaves_correct_base_byte_identical():
    base = "foreign gene\n+\nI:V 3:1 Ratio\nTransformation.\n+ Validation\n"

    result = restore_quorum_standalone_signs(base, SCOUT_ONE, SCOUT_TWO)

    assert result == RestoredStandaloneSigns(markdown=base, restored_count=0)


def test_nonquorum_sign_is_not_restored():
    base = "foreign gene\nI:V 3:1 Ratio\n"
    first = "foreign gene\n+\nI:V\n"
    second = "foreign gene\nI:V\n"

    result = restore_quorum_standalone_signs(base, first, second)

    assert result == RestoredStandaloneSigns(markdown=base, restored_count=0)


def test_unmatched_quorum_anchors_cannot_inject_a_sign():
    base = "unrelated base\n"

    result = restore_quorum_standalone_signs(base, SCOUT_ONE, SCOUT_TWO)

    assert result == RestoredStandaloneSigns(markdown=base, restored_count=0)


@pytest.mark.parametrize(
    ("base", "first", "second"),
    (("", "a", "b"), ("a", "", "b"), ("a", "b", None)),
)
def test_restore_rejects_empty_or_nonexact_inputs(base, first, second):
    with pytest.raises(ValueError, match="must be nonempty plain text"):
        restore_quorum_standalone_signs(base, first, second)  # type: ignore[arg-type]
