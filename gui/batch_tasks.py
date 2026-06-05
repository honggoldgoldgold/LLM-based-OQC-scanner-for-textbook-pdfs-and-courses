"""GUI 多文件批处理辅助。"""

from __future__ import annotations

from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from dataclasses import dataclass
import logging
import os
from typing import Callable

from ..config import AppConfig
from ..core.task_runner import CancelledError, ProgressReporter
from ..core.utils import resolve_workers

logger = logging.getLogger(__name__)

_AUTO_WORKER_HARD_CAP = 8


@dataclass(frozen=True, slots=True)
class BatchFileTask:
    """单个文件批处理任务描述。"""

    source_path: str
    display_name: str
    run: Callable[[AppConfig, ProgressReporter], str]


def run_batch_tasks(
    *,
    task_kind: str,
    task_label: str,
    cfg: AppConfig,
    reporter: ProgressReporter,
    tasks: list[BatchFileTask],
) -> str:
    """执行一组相互独立的文件任务。"""
    if not tasks:
        return f"没有可处理的{task_label}文件"

    worker_count = _resolve_batch_workers(task_kind, cfg, len(tasks))
    shared_cfg = _shared_batch_cfg(cfg, task_kind, worker_count)
    reporter.progress(0, len(tasks), f"批量{task_label}: 共 {len(tasks)} 个文件，最多并行 {worker_count} 个任务")

    successes: list[tuple[str, str]] = []
    failures: list[tuple[str, str]] = []
    done = 0

    def _run_one(task: BatchFileTask) -> tuple[str, str]:
        child = _fork_reporter(reporter, task.display_name)
        logger.info("[BATCH] 开始%s: %s", task_label, task.source_path)
        result = task.run(shared_cfg, child)
        logger.info("[BATCH] 完成%s: %s -> %s", task_label, task.source_path, result)
        return task.display_name, result

    executor = ThreadPoolExecutor(max_workers=worker_count, thread_name_prefix=f"batch-{task_kind}")
    future_map = {}
    try:
        for task in tasks:
            reporter.check_cancelled()
            future = executor.submit(_run_one, task)
            future_map[future] = task

        while future_map:
            reporter.check_cancelled()
            finished, _ = wait(set(future_map), timeout=0.2, return_when=FIRST_COMPLETED)
            if not finished:
                continue

            for future in finished:
                task = future_map.pop(future)
                done += 1
                try:
                    name, result = future.result()
                    successes.append((name, result))
                    reporter.progress(done, len(tasks), f"批量{task_label}: 已完成 {done}/{len(tasks)} · {name}")
                except CancelledError:
                    raise
                except Exception as e:
                    logger.exception("[BATCH] %s 失败: %s", task.source_path, e)
                    failures.append((task.display_name, str(e)))
                    reporter.progress(done, len(tasks), f"批量{task_label}: 失败 {done}/{len(tasks)} · {task.display_name}")
    finally:
        for future in future_map:
            future.cancel()
        executor.shutdown(wait=False, cancel_futures=True)

    return _build_summary(task_label, successes, failures)


def _resolve_batch_workers(task_kind: str, cfg: AppConfig, task_count: int) -> int:
    if task_kind == "pdf":
        llm_budget = max(1, cfg.concurrency.llm_parallel_requests // 4)
        render_budget = max(1, _effective_worker_budget(cfg.concurrency.pdf_render_workers))
        budget = min(llm_budget, render_budget, 2)
    elif task_kind == "video":
        llm_budget = max(1, cfg.concurrency.llm_parallel_requests // 3)
        resize_budget = max(1, _effective_worker_budget(cfg.concurrency.video_resize_workers))
        budget = min(llm_budget, resize_budget, 2)
    elif task_kind == "board":
        budget = max(1, cfg.concurrency.llm_parallel_requests)
    elif task_kind == "audio":
        budget = max(1, cfg.concurrency.audio_asr_parallel_requests)
    else:
        budget = 1
    return resolve_workers(max(1, budget), task_count, hard_cap=_AUTO_WORKER_HARD_CAP)


def _shared_batch_cfg(cfg: AppConfig, task_kind: str, worker_count: int) -> AppConfig:
    updates: dict[str, dict] = {"concurrency": {}}
    concurrency = updates["concurrency"]

    if task_kind in {"pdf", "video", "board"}:
        concurrency["llm_parallel_requests"] = max(1, cfg.concurrency.llm_parallel_requests // worker_count)
    if task_kind == "pdf":
        concurrency["pdf_render_workers"] = max(
            1,
            _effective_worker_budget(cfg.concurrency.pdf_render_workers) // worker_count,
        )
    if task_kind == "video":
        concurrency["video_resize_workers"] = max(
            1,
            _effective_worker_budget(cfg.concurrency.video_resize_workers) // worker_count,
        )
    if task_kind == "audio":
        concurrency["audio_asr_parallel_requests"] = max(1, cfg.concurrency.audio_asr_parallel_requests // worker_count)
        concurrency["audio_split_workers"] = max(
            1,
            _effective_worker_budget(cfg.concurrency.audio_split_workers) // worker_count,
        )

    if not concurrency:
        return cfg
    return cfg.with_updates(**updates)


def _fork_reporter(parent: ProgressReporter, label_prefix: str) -> ProgressReporter:
    def _on_content(text: str, label: str):
        if parent.on_content:
            merged = f"{label_prefix} · {label}" if label else label_prefix
            parent.on_content(text, merged)

    child = ProgressReporter(on_content=_on_content)
    child._cancelled = parent.cancel_event
    return child


def _effective_worker_budget(configured: int, hard_cap: int = _AUTO_WORKER_HARD_CAP) -> int:
    if configured and configured > 0:
        return max(1, configured)
    return max(1, min(os.cpu_count() or 4, hard_cap))


def _build_summary(task_label: str, successes: list[tuple[str, str]], failures: list[tuple[str, str]]) -> str:
    lines = [f"批量{task_label}完成: 成功 {len(successes)}, 失败 {len(failures)}"]
    if successes:
        lines.append("成功文件:")
        lines.extend(f"- {name}" for name, _ in successes[:10])
        if len(successes) > 10:
            lines.append(f"- 其余 {len(successes) - 10} 个文件略")
    if failures:
        lines.append("失败文件:")
        lines.extend(f"- {name}: {message.splitlines()[0]}" for name, message in failures[:10])
        if len(failures) > 10:
            lines.append(f"- 其余 {len(failures) - 10} 个失败文件略")

    if failures and not successes:
        raise RuntimeError("\n".join(lines))
    return "\n".join(lines)