"""Launch the real control loop with a deterministic test-only job manager."""

from __future__ import annotations

import sys
from collections.abc import Callable
from pathlib import Path


SOURCE_ROOT = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SOURCE_ROOT))

from ocrllm.contracts import (  # noqa: E402
    AcceptedEvent,
    CancelCommand,
    ImageRecognitionRequest,
    ResultEvent,
    WorkerEvent,
    WorkerRecognitionResult,
)
from ocrllm.errors import OCRLLMError  # noqa: E402
from ocrllm.worker import run_worker_control_loop  # noqa: E402


class FixtureJobManager:
    """Produce deterministic accepted/result events without provider work."""

    def start(
        self,
        command: ImageRecognitionRequest,
        *,
        emit: Callable[[WorkerEvent], None],
    ) -> None:
        emit(AcceptedEvent(request_id=command.request_id))
        source_uris = [source.uri for source in command.sources]
        emit(
            ResultEvent(
                request_id=command.request_id,
                result=WorkerRecognitionResult(
                    markdown="# Fixture recognition\n",
                    source_type="image",
                    profile="board",
                    metadata={"source_uris": source_uris, "mode": "fixture"},
                ),
            )
        )

    def cancel(
        self,
        command: CancelCommand,
        *,
        emit: Callable[[WorkerEvent], None],
    ) -> None:
        raise OCRLLMError(
            "The requested worker job is not active.",
            code="REQUEST_NOT_ACTIVE",
        )

    def close(self) -> None:
        return None


def main() -> int:
    run_worker_control_loop(
        input_stream=sys.stdin.buffer,
        output_stream=sys.stdout.buffer,
        job_manager=FixtureJobManager(),
        internal_error_reporter=lambda _: print(
            "worker fixture internal error",
            file=sys.stderr,
            flush=True,
        ),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
