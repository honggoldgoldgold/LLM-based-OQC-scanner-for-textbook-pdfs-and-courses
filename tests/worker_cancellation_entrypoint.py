"""Launch the real control loop with a blocking child-plus-grandchild fixture."""

from __future__ import annotations

import sys
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "src"))
sys.path.insert(0, str(REPOSITORY_ROOT / "tests"))

from ocrllm.worker import (  # noqa: E402
    IsolatedWorkerJobManager,
    report_worker_internal_error,
    run_worker_control_loop,
)
from worker_job_fixtures import block_with_grandchild  # noqa: E402


def main() -> int:
    reporter = lambda error: report_worker_internal_error(  # noqa: E731
        error,
        stream=sys.stderr,
    )
    run_worker_control_loop(
        input_stream=sys.stdin.buffer,
        output_stream=sys.stdout.buffer,
        job_manager=IsolatedWorkerJobManager(
            block_with_grandchild,
            internal_error_reporter=reporter,
        ),
        internal_error_reporter=reporter,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
