"""Launch the production OCRLLM JSONL worker."""

from __future__ import annotations

import multiprocessing
import sys

from .run_production_worker import run_production_worker


def main() -> int:
    """Bind the production worker to standard streams and run until EOF."""

    multiprocessing.freeze_support()
    run_production_worker(
        input_stream=sys.stdin.buffer,
        output_stream=sys.stdout.buffer,
        error_stream=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
