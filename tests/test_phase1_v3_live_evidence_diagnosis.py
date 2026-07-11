"""Prove v3 isolates v2 presentation failures from handwriting quality."""

import json
from pathlib import Path

from tests.quality.load_fixture_manifest import load_fixture_manifest
from tests.quality.score_recognition_result import score_recognition_result


EVIDENCE_PATH = (
    Path(__file__).parent.parent
    / "evidence"
    / "phase1"
    / "phase1-quality-v2-2026-07-11-cn-beijing.json"
)


def test_v2_outputs_pass_v3_presentation_but_keep_handwriting_failures():
    evidence = json.loads(EVIDENCE_PATH.read_text(encoding="utf-8"))
    manifest = load_fixture_manifest()
    expected_passes = (True, True, False, True, True, True)
    handwriting_failures = (
        "text_recall_below_threshold",
        "content_precision_below_threshold",
        "text_critical_accuracy_below_one",
        "text_unexpected_critical_units",
        "language_text_recall_below_threshold:en-US",
        "language_content_precision_below_threshold:en-US",
        "critical_slot_accuracy_below_one",
    )

    smoke = score_recognition_result(
        manifest,
        manifest.live_dispatch_order[0],
        evidence["smoke"]["markdown"],
    )
    assert smoke.passes
    for run in evidence["full_runs"]:
        reports = tuple(
            score_recognition_result(
                manifest,
                manifest.live_dispatch_order[sequence],
                dispatch["markdown"],
            )
            for sequence, dispatch in enumerate(run["dispatches"])
        )
        assert tuple(report.passes for report in reports) == expected_passes
        assert reports[2].failures == handwriting_failures
