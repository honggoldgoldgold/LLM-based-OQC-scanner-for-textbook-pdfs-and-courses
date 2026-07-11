from dataclasses import FrozenInstanceError, replace

import pytest

from tests.quality.build_scorer_expectations import build_scorer_expectations
from tests.quality.load_fixture_manifest import load_fixture_manifest
from tests.quality.score_recognition_result import score_recognition_result


def _fixture_markdown(manifest, fixture_id):
    fixture = next(item for item in manifest.fixtures if item.id == fixture_id)
    lines = [unit.text for unit in fixture.content_units]
    lines.extend(
        f"{formula.label}: ${formula.accepted_latex[0]}$"
        for formula in fixture.formulas
    )
    if fixture.table is not None:
        table = fixture.table
        headers = [header.accepted[0] for header in table.headers]
        cells = {(cell.row, cell.column): cell for cell in table.cells}
        lines.extend(
            (
                "| " + " | ".join(headers) + " |",
                "| " + " | ".join("---" for _ in headers) + " |",
            )
        )
        lines.extend(
            "| "
            + " | ".join(
                cells[(row, column)].accepted[0]
                for column in range(table.column_count)
            )
            + " |"
            for row in range(table.row_count)
        )
    return "\n".join(lines)


def _dispatch_markdown(manifest, dispatch):
    return "\n".join(
        _fixture_markdown(manifest, fixture_id)
        for fixture_id in dispatch.fixture_ids
    )


def test_perfect_single_and_ordered_dispatches_return_immutable_passing_reports():
    manifest = load_fixture_manifest()
    single = manifest.live_dispatch_order[0]
    ordered = manifest.live_dispatch_order[5]

    single_report = score_recognition_result(
        manifest,
        single,
        _dispatch_markdown(manifest, single),
    )
    ordered_report = score_recognition_result(
        manifest,
        ordered,
        _dispatch_markdown(manifest, ordered),
    )

    assert single_report.target == single.fixture_ids[0]
    assert single_report.profile == "printed_slide"
    assert single_report.dispatch_sequence == 0
    assert single_report.fixture_ids == single.fixture_ids
    assert single_report.failures == ()
    assert single_report.passes
    assert ordered_report.target == ordered.ordered_request_id
    assert ordered_report.profile == "ordered_request"
    assert ordered_report.failures == ()
    assert ordered_report.passes
    with pytest.raises(FrozenInstanceError):
        single_report.profile = "changed"  # type: ignore[misc]


def test_omitted_handwriting_critical_value_fails_while_ratios_still_pass():
    manifest = load_fixture_manifest()
    dispatch = manifest.live_dispatch_order[2]
    recognized = "\n".join(
        unit.text
        for fixture in manifest.fixtures
        if fixture.id == dispatch.fixture_ids[0]
        for unit in fixture.content_units
        if unit.text != "MCS"
    )

    report = score_recognition_result(manifest, dispatch, recognized)

    assert report.text_score.recall.numerator == 24
    assert report.text_score.recall.denominator == 25
    assert report.text_score.critical_accuracy.numerator == (
        report.text_score.critical_accuracy.denominator
    )
    assert all(
        item.metrics.recall.numerator * 100
        >= item.metrics.recall.denominator * 85
        for item in report.language_text_scores
    )
    assert report.critical_slot_score is not None
    assert report.critical_slot_score.accuracy.numerator == 8
    assert report.critical_slot_score.accuracy.denominator == 9
    assert report.failures == ("critical_slot_accuracy_below_one",)
    assert not report.passes


def test_ordered_request_missing_formula_and_extra_f99_fail_end_to_end():
    manifest = load_fixture_manifest()
    dispatch = manifest.live_dispatch_order[5]
    perfect = _dispatch_markdown(manifest, dispatch)
    formula = next(
        formula
        for fixture in manifest.fixtures
        if fixture.id == "formula-integrity-board"
        for formula in fixture.formulas
        if formula.label == "F01"
    )
    formula_line = f"{formula.label}: ${formula.accepted_latex[0]}$"

    missing = score_recognition_result(
        manifest,
        dispatch,
        perfect.replace(formula_line + "\n", ""),
    )
    extra = score_recognition_result(
        manifest,
        dispatch,
        perfect + "\nF99: $z=999$",
    )

    assert missing.formula_score is not None
    assert missing.formula_score.missing_labels == ("F01",)
    assert "formula_critical_accuracy_below_one" in missing.failures
    assert not missing.passes
    assert extra.formula_score is not None
    assert extra.formula_score.unexpected_labels == ("F99",)
    assert "formula_unexpected_labels" in extra.failures
    assert "formula_unexpected_atoms" in extra.failures
    assert not extra.passes


def test_wrong_or_detached_dispatch_record_is_rejected():
    manifest = load_fixture_manifest()
    dispatch = manifest.live_dispatch_order[0]
    markdown = _dispatch_markdown(manifest, dispatch)

    with pytest.raises(ValueError, match="exact manifest record"):
        score_recognition_result(manifest, replace(dispatch), markdown)
    with pytest.raises(ValueError, match="exact manifest record"):
        score_recognition_result(
            manifest,
            replace(dispatch, fixture_ids=("handwritten-whiteboard",)),
            markdown,
        )
    with pytest.raises(TypeError, match="exact Phase1FixtureManifest"):
        score_recognition_result(object(), dispatch, markdown)  # type: ignore[arg-type]


def test_manifest_dataclass_cannot_delete_checksum_slot_while_retaining_raw_hash():
    manifest = load_fixture_manifest()
    dispatch = manifest.live_dispatch_order[0]
    fixture_id = dispatch.fixture_ids[0]
    fixture = next(item for item in manifest.fixtures if item.id == fixture_id)
    assert len(fixture.critical_slots) == 9
    assert fixture.critical_slots[-1].id == "checksum"
    weakened_fixture = replace(
        fixture,
        critical_slots=fixture.critical_slots[:-1],
    )
    weakened_manifest = replace(
        manifest,
        fixtures=tuple(
            weakened_fixture if item.id == fixture_id else item
            for item in manifest.fixtures
        ),
    )
    assert weakened_manifest.raw_sha256 == manifest.raw_sha256
    assert len(weakened_fixture.critical_slots) == 8
    corrupted = _dispatch_markdown(weakened_manifest, dispatch).replace(
        "CHECKSUM: CN-7319",
        "CHECKSUM: XX-7319",
        1,
    )

    with pytest.raises(ValueError, match="freshly strict-loaded canonical manifest"):
        score_recognition_result(weakened_manifest, dispatch, corrupted)


def test_table_dispatch_scores_coordinates_and_reports_a_missing_table_channel():
    manifest = load_fixture_manifest()
    dispatch = manifest.live_dispatch_order[4]
    perfect = _dispatch_markdown(manifest, dispatch)

    passing = score_recognition_result(manifest, dispatch, perfect)
    corrupted = score_recognition_result(
        manifest,
        dispatch,
        perfect.replace("12.57", "12.58", 1),
    )
    fixture = next(item for item in manifest.fixtures if item.id == dispatch.fixture_ids[0])
    missing = score_recognition_result(
        manifest,
        dispatch,
        "\n".join(unit.text for unit in fixture.content_units),
    )

    assert passing.table_score is not None
    assert passing.table_score.data_cell_accuracy.numerator == (
        passing.table_score.data_cell_accuracy.denominator
    )
    assert passing.passes
    assert corrupted.table_score is not None
    assert "table_critical_accuracy_below_one" in corrupted.failures
    assert not corrupted.passes
    assert missing.table_score is None
    assert "table_score_required" in missing.failures
    assert not missing.passes


def test_report_score_cardinalities_equal_manifest_driven_expectations():
    manifest = load_fixture_manifest()
    expectations = build_scorer_expectations(manifest)
    fixture_expectations = {item.fixture_id: item for item in expectations.fixtures}
    ordered_expectations = {
        item.request_id: item for item in expectations.ordered_requests
    }
    fixture_records = {item.id: item for item in manifest.fixtures}

    for dispatch in manifest.live_dispatch_order:
        report = score_recognition_result(
            manifest,
            dispatch,
            _dispatch_markdown(manifest, dispatch),
        )
        if dispatch.kind == "single":
            expected = fixture_expectations[dispatch.fixture_ids[0]]
            languages = fixture_records[dispatch.fixture_ids[0]].languages
        else:
            expected = ordered_expectations[dispatch.ordered_request_id]
            languages = tuple(
                dict.fromkeys(
                    language
                    for fixture_id in dispatch.fixture_ids
                    for language in fixture_records[fixture_id].languages
                )
            )

        assert report.text_score.recall.denominator == sum(
            unit.count for unit in expected.text
        )
        assert tuple(item.language for item in report.language_text_scores) == languages
        for language_score in report.language_text_scores:
            token_kind = {"en-US": "word", "zh-CN": "han"}[language_score.language]
            assert language_score.metrics.recall.denominator == sum(
                unit.count for unit in expected.text if unit.kind == token_kind
            )
        if expected.critical_slots:
            assert report.critical_slot_score is not None
            assert report.critical_slot_score.accuracy.denominator == sum(
                slot.count for slot in expected.critical_slots
            )
        else:
            assert report.critical_slot_score is None
        if expected.formulas:
            assert report.formula_score is not None
            assert report.formula_score.signature_accuracy.denominator == len(
                expected.formulas
            )
        else:
            assert report.formula_score is None
        if expected.table is not None:
            assert report.table_score is not None
            assert report.table_score.header_accuracy.denominator == len(
                expected.table.header
            )
            assert report.table_score.data_cell_accuracy.denominator == (
                len(expected.table.header) * len(expected.table.rows)
            )
        else:
            assert report.table_score is None
        if dispatch.kind == "ordered":
            assert report.ordered_anchor_score is not None
            assert report.ordered_anchor_score.presence.denominator == len(
                expected.anchors
            )
        else:
            assert report.ordered_anchor_score is None
        assert report.passes
