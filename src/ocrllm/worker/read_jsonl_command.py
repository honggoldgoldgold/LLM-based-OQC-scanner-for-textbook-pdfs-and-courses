"""Read one bounded UTF-8 JSONL command from a binary stream."""

from __future__ import annotations

from typing import BinaryIO

from ocrllm.contracts.parse_jsonl_command import parse_jsonl_command
from ocrllm.contracts.worker_command import WorkerCommand
from ocrllm.errors import OCRLLMError


MAX_JSONL_COMMAND_BYTES = 1_048_576


def read_jsonl_command(stream: BinaryIO) -> WorkerCommand | None:
    """Read one newline-terminated record, returning None only at clean EOF."""

    raw_line = stream.readline(MAX_JSONL_COMMAND_BYTES + 1)
    if raw_line == b"":
        return None
    if len(raw_line) > MAX_JSONL_COMMAND_BYTES or not raw_line.endswith(b"\n"):
        if not raw_line.endswith(b"\n"):
            _drain_rejected_record(stream)
        raise _command_invalid("Worker command record is too large or incomplete.")
    try:
        line = raw_line.decode("utf-8", errors="strict")
    except UnicodeDecodeError:
        raise _command_invalid("Worker command is not valid UTF-8.") from None
    return parse_jsonl_command(line)


def _drain_rejected_record(stream: BinaryIO) -> None:
    while True:
        remainder = stream.readline(MAX_JSONL_COMMAND_BYTES + 1)
        if remainder == b"" or remainder.endswith(b"\n"):
            return


def _command_invalid(message: str) -> OCRLLMError:
    return OCRLLMError(message, code="COMMAND_INVALID")
