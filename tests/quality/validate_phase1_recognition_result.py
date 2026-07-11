"""Validate one live RecognitionResult against its exact dispatch contract."""

from __future__ import annotations

from ocrllm import RecognitionResult

from tests.quality.build_phase1_dispatch_plan import Phase1DispatchPlanEntry
from tests.quality.fixture_manifest import EvidenceContract


def validate_phase1_recognition_result(
    result: RecognitionResult,
    *,
    plan_entry: Phase1DispatchPlanEntry,
    contract: EvidenceContract,
    provider_region: str,
) -> None:
    """Reject incomplete output or any missing, extra, or divergent metadata."""

    if type(result) is not RecognitionResult:
        raise TypeError("result must be an exact RecognitionResult")
    if type(plan_entry) is not Phase1DispatchPlanEntry:
        raise TypeError("plan_entry must be an exact Phase1DispatchPlanEntry")
    if type(contract) is not EvidenceContract:
        raise TypeError("contract must be an exact EvidenceContract")
    if type(provider_region) is not str or not provider_region:
        raise TypeError("provider_region must be nonempty text")
    if (
        result.source_type != contract.source_type
        or result.profile != contract.profile
        or result.status != "complete"
        or result.output_path is not None
        or result.assets
        or result.hotwords
        or result.warnings
    ):
        raise ValueError("recognition result differs from the frozen success contract")

    expected_metadata = {
        "image_count": len(plan_entry.fixture_ids),
        "model": contract.model,
        "prompt_version": contract.prompt_version,
        "provider_call_count": (
            contract.draft_candidates
            + contract.review_passes
            + contract.standalone_sign_scout_count
        ),
        "draft_candidates": contract.draft_candidates,
        "review_passes": contract.review_passes,
        "standalone_sign_scout_model": contract.standalone_sign_scout_model,
        "standalone_sign_scout_count": contract.standalone_sign_scout_count,
        "standalone_sign_scout_enable_thinking": (
            contract.standalone_sign_scout_enable_thinking
        ),
        "standalone_signs_restored": result.metadata.get(
            "standalone_signs_restored"
        ),
        "standalone_sign_scout_abstention_count": result.metadata.get(
            "standalone_sign_scout_abstention_count"
        ),
        "provider": contract.provider,
        "profile": contract.profile,
        "provider_region": provider_region,
        "enable_thinking": contract.enable_thinking,
        "vl_high_resolution_images": contract.vl_high_resolution_images,
    }
    restored_count = expected_metadata["standalone_signs_restored"]
    if type(restored_count) is not int or restored_count < 0:
        raise ValueError("recognition result has an invalid restored-sign count")
    abstention_count = expected_metadata["standalone_sign_scout_abstention_count"]
    if (
        type(abstention_count) is not int
        or not 0 <= abstention_count <= contract.standalone_sign_scout_count
    ):
        raise ValueError("recognition result has an invalid scout-abstention count")
    if dict(result.metadata) != expected_metadata:
        raise ValueError(
            "recognition result metadata differs from the frozen request contract"
        )
