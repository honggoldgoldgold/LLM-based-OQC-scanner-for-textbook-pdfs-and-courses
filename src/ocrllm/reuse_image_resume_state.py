"""Validate and reconstruct one completed image processor output."""

from __future__ import annotations

import hashlib

from .errors import ResumeStateError
from .image_request_identity import ImageRequestIdentity
from .image_resume_state import ImageResumeState
from .processor_output import ProcessorOutput


def reuse_image_resume_state(
    state: ImageResumeState,
    identity: ImageRequestIdentity,
) -> ProcessorOutput:
    """Return stored output only when source, request, and processor all match."""
    if (
        state.request_fingerprint != identity.request_fingerprint
        or state.processor_name != identity.processor_name
        or state.processor_version != identity.processor_version
        or state.sources != identity.sources
    ):
        raise ResumeStateError(
            "The image resume state belongs to a different request.",
            code="RESUME_STATE_MISMATCH",
        ) from None
    markdown_sha256 = hashlib.sha256(state.markdown.encode("utf-8")).hexdigest()
    if markdown_sha256 != state.final_markdown_sha256:
        raise ResumeStateError(
            "The completed result in image resume state is corrupt.",
            code="RESUME_STATE_INVALID",
        ) from None
    return ProcessorOutput(
        media_type="image",
        markdown=state.markdown,
        profile=state.profile,
        status=state.status,
        hotwords=state.hotwords,
        warnings=state.warnings,
        metadata=state.metadata,
    )
