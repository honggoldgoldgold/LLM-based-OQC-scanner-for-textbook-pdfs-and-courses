"""Write one protocol-only UTF-8 JSONL event to a binary stream."""

from __future__ import annotations

import json
from typing import BinaryIO

from ocrllm.contracts.serialize_worker_event import serialize_worker_event
from ocrllm.contracts.worker_event import WorkerEvent


def write_jsonl_event(event: WorkerEvent, *, stream: BinaryIO) -> None:
    """Write exactly one compact JSON record and flush it before returning."""

    payload = (
        json.dumps(
            serialize_worker_event(event),
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")
    offset = 0
    while offset < len(payload):
        written = stream.write(payload[offset:])
        if not isinstance(written, int) or written <= 0:
            raise OSError("worker stdout did not accept the complete event")
        offset += written
    stream.flush()
