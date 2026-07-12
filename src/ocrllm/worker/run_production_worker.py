"""Compose the production JSONL worker from explicit stream boundaries."""

from __future__ import annotations

from functools import partial
from typing import BinaryIO, TextIO

from .isolated_worker_job_manager import IsolatedWorkerJobManager
from .report_worker_internal_error import report_worker_internal_error
from .run_image_recognition_job import run_image_recognition_job
from .run_worker_control_loop import run_worker_control_loop


def run_production_worker(
    *,
    input_stream: BinaryIO,
    output_stream: BinaryIO,
    error_stream: TextIO,
) -> None:
    """Run stdin/stdout JSONL with one isolated unified image job at a time."""

    internal_error_reporter = partial(
        report_worker_internal_error,
        stream=error_stream,
    )
    job_manager = IsolatedWorkerJobManager(
        run_image_recognition_job,
        internal_error_reporter=internal_error_reporter,
    )
    run_worker_control_loop(
        input_stream=input_stream,
        output_stream=output_stream,
        job_manager=job_manager,
        internal_error_reporter=internal_error_reporter,
    )
