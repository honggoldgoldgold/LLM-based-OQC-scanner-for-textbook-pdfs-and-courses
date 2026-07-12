"""Strictly parse one bounded image resume JSON document."""

from __future__ import annotations

import json

from .contracts.source_fingerprint import SourceFingerprint
from .errors import ResumeStateError
from .image_resume_state import ImageResumeState


_ROOT_KEYS = frozenset(
    {
        "state_version",
        "request_fingerprint",
        "processor_name",
        "processor_version",
        "sources",
        "result",
        "final_markdown_sha256",
    }
)
_SOURCE_KEYS = frozenset({"uri", "byte_size", "sha256"})
_RESULT_KEYS = frozenset(
    {"markdown", "media_type", "profile", "status", "hotwords", "warnings", "metadata"}
)


class _DuplicateKey(ValueError):
    pass


def parse_image_resume_state(raw: bytes) -> ImageResumeState:
    """Reject duplicate keys, schema drift, and invalid completed results."""
    try:
        document = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=_unique_object,
            parse_constant=_reject_constant,
        )
        if type(document) is not dict or frozenset(document) != _ROOT_KEYS:
            raise ValueError
        source_documents = document["sources"]
        result = document["result"]
        if type(source_documents) is not list or not source_documents:
            raise ValueError
        if type(result) is not dict or frozenset(result) != _RESULT_KEYS:
            raise ValueError
        sources = []
        for source in source_documents:
            if type(source) is not dict or frozenset(source) != _SOURCE_KEYS:
                raise ValueError
            sources.append(
                SourceFingerprint(
                    uri=source["uri"],
                    byte_size=source["byte_size"],
                    sha256=source["sha256"],
                )
            )
        hotwords = result["hotwords"]
        warnings = result["warnings"]
        if type(hotwords) is not list or type(warnings) is not list:
            raise ValueError
        return ImageResumeState(
            state_version=document["state_version"],
            request_fingerprint=document["request_fingerprint"],
            processor_name=document["processor_name"],
            processor_version=document["processor_version"],
            sources=tuple(sources),
            markdown=result["markdown"],
            media_type=result["media_type"],
            profile=result["profile"],
            status=result["status"],
            hotwords=tuple(hotwords),
            warnings=tuple(warnings),
            metadata=result["metadata"],
            final_markdown_sha256=document["final_markdown_sha256"],
        )
    except ResumeStateError:
        raise
    except Exception:
        raise ResumeStateError(
            "The image resume state is corrupt or has an unsupported schema.",
            code="RESUME_STATE_INVALID",
        ) from None


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise _DuplicateKey
        result[key] = value
    return result


def _reject_constant(_value: str) -> object:
    raise ValueError
