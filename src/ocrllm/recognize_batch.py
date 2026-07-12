"""Recognize independent requests in caller order."""

from __future__ import annotations

from collections.abc import Iterable, Iterator, Sequence
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import TYPE_CHECKING

from .config import Config
from .recognize import recognize
from .providers.provider_request_start_gate import (
    ProviderRequestStartGate,
    activate_provider_request_start_gate,
)
from .validate_config import validate_config

if TYPE_CHECKING:
    from .result import RecognitionResult


def recognize_batch(
    sources: Iterable[str | Path | Sequence[str | Path]],
    *,
    config: Config | None = None,
) -> list[RecognitionResult]:
    """Return ordered independent results with bounded fail-fast execution."""
    cfg = validate_config(config)
    gate = ProviderRequestStartGate(
        cfg.execution.provider_request_start_interval_seconds
    )
    if cfg.execution.max_parallel_requests == 1:
        with activate_provider_request_start_gate(gate):
            return [recognize(source, config=cfg) for source in sources]

    source_iterator = iter(sources)
    results: list[RecognitionResult | None] = []
    with ThreadPoolExecutor(
        max_workers=cfg.execution.max_parallel_requests,
        thread_name_prefix="ocrllm-recognition",
    ) as executor:
        future_indexes: dict[Future[RecognitionResult], int] = {}
        try:
            for _ in range(cfg.execution.max_parallel_requests):
                if not _submit_next_batch_item(
                    source_iterator,
                    executor=executor,
                    config=cfg,
                    gate=gate,
                    results=results,
                    future_indexes=future_indexes,
                ):
                    break

            while future_indexes:
                future = next(as_completed(tuple(future_indexes)))
                result_index = future_indexes.pop(future)
                results[result_index] = future.result()
                _submit_next_batch_item(
                    source_iterator,
                    executor=executor,
                    config=cfg,
                    gate=gate,
                    results=results,
                    future_indexes=future_indexes,
                )
        except BaseException:
            gate.abort()
            for future in future_indexes:
                future.cancel()
            raise

    if any(result is None for result in results):  # pragma: no cover - defensive.
        raise AssertionError("recognize_batch() completed without every result")
    return [result for result in results if result is not None]


def _submit_next_batch_item(
    source_iterator: Iterator[str | Path | Sequence[str | Path]],
    *,
    executor: ThreadPoolExecutor,
    config: Config,
    gate: ProviderRequestStartGate,
    results: list[RecognitionResult | None],
    future_indexes: dict[Future[RecognitionResult], int],
) -> bool:
    """Submit at most one source so queued work never exceeds the worker bound."""
    try:
        source = next(source_iterator)
    except StopIteration:
        return False

    result_index = len(results)
    results.append(None)
    future = executor.submit(
        _recognize_batch_item,
        source,
        config=config,
        gate=gate,
    )
    future_indexes[future] = result_index
    return True


def _recognize_batch_item(
    source: str | Path | Sequence[str | Path],
    *,
    config: Config,
    gate: ProviderRequestStartGate,
) -> RecognitionResult:
    """Run one batch item with the operation-wide provider start gate."""
    with activate_provider_request_start_gate(gate):
        return recognize(source, config=config)
