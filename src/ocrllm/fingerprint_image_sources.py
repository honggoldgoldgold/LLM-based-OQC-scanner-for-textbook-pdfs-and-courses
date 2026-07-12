"""Hash the exact validated image bytes used by a resumable request."""

from __future__ import annotations

import hashlib
from collections.abc import Sequence
from pathlib import Path

from .contracts.source_fingerprint import SourceFingerprint
from .errors import InvalidSource, OutputError


_CHUNK_BYTES = 1024 * 1024


def fingerprint_image_sources(
    source_paths: Sequence[Path],
    snapshot_paths: Sequence[Path],
) -> tuple[SourceFingerprint, ...]:
    """Return ordered original URIs with hashes of their validated snapshots."""
    if len(source_paths) != len(snapshot_paths) or not source_paths:
        raise ValueError("source and snapshot groups must be nonempty and aligned")
    fingerprints = []
    for source_path, snapshot_path in zip(source_paths, snapshot_paths, strict=True):
        try:
            digest = hashlib.sha256()
            byte_size = 0
            with snapshot_path.open("rb") as stream:
                while chunk := stream.read(_CHUNK_BYTES):
                    digest.update(chunk)
                    byte_size += len(chunk)
            source_uri = source_path.resolve(strict=True).as_uri()
        except FileNotFoundError:
            raise InvalidSource(
                "A recognition source disappeared before resume identity was built.",
                code="SOURCE_NOT_FOUND",
            ) from None
        except (OSError, ValueError):
            raise OutputError(
                "Validated image bytes could not be fingerprinted for resume.",
                code="OUTPUT_WRITE_FAILED",
            ) from None
        fingerprints.append(
            SourceFingerprint(
                uri=source_uri,
                byte_size=byte_size,
                sha256=digest.hexdigest(),
            )
        )
    return tuple(fingerprints)
