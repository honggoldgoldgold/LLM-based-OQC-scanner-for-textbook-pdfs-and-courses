"""
OCRLLM FastAPI service.

The API exposes OCRLLM processing as bounded asynchronous background tasks for
external systems such as STAv2.
"""

from __future__ import annotations

import logging
import os
import time
import traceback
import uuid
from concurrent.futures import Future, ThreadPoolExecutor
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from threading import Lock
from typing import Any, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from OCRLLM.config import AppConfig
from OCRLLM.core.progress_tracker import ProgressTracker
from OCRLLM.core.task_runner import CancelledError, ProgressReporter

logger = logging.getLogger(__name__)


@asynccontextmanager
async def _lifespan(application: FastAPI):
    yield
    _executor.shutdown(wait=True, cancel_futures=True)
    logger.info("[API] Executor shutdown complete.")


app = FastAPI(
    title="OCRLLM Processing API",
    description="OCR/LLM processing service for STA and other callers.",
    version="1.1.0",
    lifespan=_lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_MAX_CONCURRENT_TASKS = max(1, int(os.environ.get("OCRLLM_MAX_CONCURRENT_TASKS", "3")))
_TASK_RETENTION_SECONDS = max(60, int(os.environ.get("OCRLLM_TASK_RETENTION_SECONDS", "86400")))
_TASK_MAX_HISTORY = max(10, int(os.environ.get("OCRLLM_TASK_MAX_HISTORY", "500")))
_MAX_INLINE_RESULT_BYTES = 5 * 1024 * 1024
_MAX_TOTAL_LLM_REQUESTS = max(
    _MAX_CONCURRENT_TASKS,
    int(os.environ.get("OCRLLM_MAX_TOTAL_LLM_REQUESTS", str(_MAX_CONCURRENT_TASKS * 4))),
)
_MAX_TOTAL_AUDIO_ASR_REQUESTS = max(
    _MAX_CONCURRENT_TASKS,
    int(os.environ.get("OCRLLM_MAX_TOTAL_AUDIO_ASR_REQUESTS", str(_MAX_CONCURRENT_TASKS * 2))),
)

_executor = ThreadPoolExecutor(max_workers=_MAX_CONCURRENT_TASKS, thread_name_prefix="ocrllm-task")
_cfg: AppConfig | None = None
_cfg_lock = Lock()


def _get_cfg() -> AppConfig:
    global _cfg
    if _cfg is None:
        with _cfg_lock:
            if _cfg is None:
                _cfg = AppConfig.from_env()
    return _cfg


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class TaskState:
    task_id: str
    task_type: str
    source: str
    status: TaskStatus = TaskStatus.PENDING
    progress_percent: float = 0.0
    progress_message: str = ""
    output_path: str = ""
    error: str = ""
    created_at: float = field(default_factory=time.time)
    started_at: float = 0.0
    finished_at: float = 0.0
    reporter: ProgressReporter = field(default_factory=ProgressReporter, repr=False)
    tracker: ProgressTracker = field(default_factory=ProgressTracker, repr=False)
    future: Optional[Future] = field(default=None, repr=False)
    result_payload: dict[str, Any] = field(default_factory=dict, repr=False)
    cancel_requested: bool = False
    lock: Lock = field(default_factory=Lock, repr=False)


_tasks: dict[str, TaskState] = {}
_tasks_lock = Lock()


def _sanitize_result_payload(result: Any) -> dict[str, Any]:
    if not isinstance(result, dict):
        return {}
    payload: dict[str, Any] = {}
    for key in ("board_md", "transcript_md", "audio_path", "output_dir", "frames_dir", "output_path"):
        value = result.get(key)
        if value:
            payload[key] = value
    hotwords = result.get("hotwords")
    if isinstance(hotwords, list):
        payload["hotwords"] = hotwords[:200]
    frames = result.get("frames")
    if isinstance(frames, list):
        payload["frames_count"] = len(frames)
    return payload


def _choose_primary_output(result: Any) -> str:
    if isinstance(result, str):
        return result
    if not isinstance(result, dict):
        return ""
    for key in ("board_md", "transcript_md", "output_path", "output_dir"):
        value = result.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def _register_task(task: TaskState) -> None:
    with _tasks_lock:
        _prune_tasks_locked()
        _tasks[task.task_id] = task


def _get_task(task_id: str) -> Optional[TaskState]:
    with _tasks_lock:
        return _tasks.get(task_id)


def _prune_tasks_locked(now: Optional[float] = None) -> None:
    now = now or time.time()
    expired: list[str] = []
    for task_id, task in _tasks.items():
        with task.lock:
            terminal = task.status in {TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED}
            age_anchor = task.finished_at or task.created_at
        if terminal and (now - age_anchor) > _TASK_RETENTION_SECONDS:
            expired.append(task_id)
    for task_id in expired:
        _tasks.pop(task_id, None)

    if len(_tasks) <= _TASK_MAX_HISTORY:
        return

    terminal_tasks = []
    for task_id, task in _tasks.items():
        with task.lock:
            if task.status in {TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED}:
                terminal_tasks.append((task.finished_at or task.created_at, task_id))
    terminal_tasks.sort()
    overflow = len(_tasks) - _TASK_MAX_HISTORY
    for _, task_id in terminal_tasks[:overflow]:
        _tasks.pop(task_id, None)


def _apply_server_concurrency_limits(cfg: AppConfig) -> AppConfig:
    cpu_budget_per_task = max(1, (os.cpu_count() or 4) // _MAX_CONCURRENT_TASKS)
    llm_budget_per_task = max(1, _MAX_TOTAL_LLM_REQUESTS // _MAX_CONCURRENT_TASKS)
    audio_budget_per_task = max(1, _MAX_TOTAL_AUDIO_ASR_REQUESTS // _MAX_CONCURRENT_TASKS)

    def _bounded(value: Any, limit: int) -> int:
        try:
            parsed = int(value)
        except Exception:
            parsed = 0
        if parsed <= 0:
            return limit
        return min(parsed, limit)

    return cfg.with_updates(
        concurrency={
            "pdf_render_workers": _bounded(cfg.concurrency.pdf_render_workers, cpu_budget_per_task),
            "llm_parallel_requests": _bounded(cfg.concurrency.llm_parallel_requests, llm_budget_per_task),
            "video_resize_workers": _bounded(cfg.concurrency.video_resize_workers, cpu_budget_per_task),
            "audio_split_workers": _bounded(cfg.concurrency.audio_split_workers, cpu_budget_per_task),
            "audio_asr_parallel_requests": _bounded(cfg.concurrency.audio_asr_parallel_requests, audio_budget_per_task),
        }
    )


def _looks_like_directory_path(path_text: str) -> bool:
    if not path_text:
        return False
    normalized = os.path.abspath(path_text)
    if os.path.isdir(normalized):
        return True
    basename = os.path.basename(normalized.rstrip("\\/"))
    return "." not in basename


def _apply_output_override(cfg: AppConfig, spec, requested_output: str) -> tuple[AppConfig, dict[str, Any]]:
    if not requested_output:
        return cfg, {}

    normalized = os.path.abspath(requested_output)
    if spec.output_target == "directory":
        return cfg, {"output_dir": normalized}

    if _looks_like_directory_path(normalized):
        return cfg.with_updates(paths={"output_dir": normalized}), {}

    return cfg, {"output_path": normalized}


def _read_text_if_small(path_text: str) -> str:
    if not path_text:
        return ""
    path = Path(path_text)
    if not path.is_file():
        return ""
    try:
        if path.stat().st_size > _MAX_INLINE_RESULT_BYTES:
            return ""
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def _collect_result_content(task: TaskState) -> str:
    paths: list[str] = []
    if task.output_path:
        paths.append(task.output_path)
    for key in ("board_md", "transcript_md", "output_path"):
        artifact_path = str(task.result_payload.get(key) or "").strip()
        if artifact_path and artifact_path not in paths:
            paths.append(artifact_path)

    parts = []
    for path_text in paths:
        text = _read_text_if_small(path_text)
        if text.strip():
            parts.append(text.strip())
    if not parts:
        return ""
    return "\n\n".join(parts) + "\n"


class ProcessRequest(BaseModel):
    type: str = "auto"
    source: str
    output_dir: str = ""
    config_overrides: dict[str, Any] = Field(default_factory=dict)


class TaskResponse(BaseModel):
    task_id: str
    status: str
    message: str = ""


class TaskStatusResponse(BaseModel):
    task_id: str
    task_type: str
    source: str
    status: str
    progress_percent: float
    progress_message: str
    output_path: str
    error: str
    created_at: float
    started_at: float
    finished_at: float


class TaskResultResponse(BaseModel):
    task_id: str
    status: str
    output_path: str
    content: str = ""
    error: str = ""
    artifacts: dict[str, Any] = Field(default_factory=dict)


def _assign_task_result(task: TaskState, result: Any) -> None:
    with task.lock:
        task.output_path = _choose_primary_output(result)
        task.result_payload = _sanitize_result_payload(result)


def _execute_social_task(task: TaskState, url: str, cfg: AppConfig, req: ProcessRequest):
    from OCRLLM.processors.social.platform_router import VideoCategory, classify_video

    route = classify_video(url, cfg)
    with task.lock:
        task.task_type = f"social_{route.category.value}"

    if req.type == "social_long" or route.category == VideoCategory.LONG:
        from OCRLLM.processors.social.long_video import SocialLongVideoProcessor

        proc = SocialLongVideoProcessor(cfg=cfg, reporter=task.reporter, tracker=task.tracker)
        result = proc.process(url, output_dir=req.output_dir or None)
    else:
        from OCRLLM.processors.social.downloader import download_media
        from OCRLLM.processors.social.short_video import ShortVideoProcessor

        download_dir = req.output_dir or os.path.join(cfg.paths.output_dir, "social_short_video")
        os.makedirs(download_dir, exist_ok=True)
        download_result = download_media(url, download_dir, cfg)

        proc = ShortVideoProcessor(cfg=cfg, reporter=task.reporter, tracker=task.tracker)
        result = proc.process(
            download_result.video_path,
            output_dir=download_dir,
            title=download_result.title,
        )

    _assign_task_result(task, result)


def _execute_local_task(task: TaskState, source: str, task_type: str, cfg: AppConfig, req: ProcessRequest):
    from OCRLLM.processors.registry import get_default_registry

    registry = get_default_registry()
    spec = registry.get(task_type)
    proc_cls = spec.load_processor_class()
    effective_cfg, kwargs = _apply_output_override(cfg, spec, req.output_dir)
    proc = proc_cls(cfg=effective_cfg, reporter=task.reporter, tracker=task.tracker)
    result = proc.process(source, **kwargs)
    _assign_task_result(task, result)


def _execute_auto_task(task: TaskState, source: str, cfg: AppConfig, req: ProcessRequest):
    from OCRLLM.processors.routing import route_input_paths

    routed = route_input_paths(source)
    with task.lock:
        task.task_type = routed.spec.key

    effective_cfg, kwargs = _apply_output_override(cfg, routed.spec, req.output_dir)
    proc_cls = routed.spec.load_processor_class()
    proc = proc_cls(cfg=effective_cfg, reporter=task.reporter, tracker=task.tracker)
    result = proc.process(routed.paths[0] if routed.is_single_file else list(routed.paths), **kwargs)
    _assign_task_result(task, result)


def _mark_cancelled(task: TaskState, message: str = "任务已取消") -> None:
    with task.lock:
        task.status = TaskStatus.CANCELLED
        task.progress_message = message
        if task.finished_at <= 0:
            task.finished_at = time.time()


def _execute_task(task_id: str, req: ProcessRequest):
    task = _get_task(task_id)
    if not task:
        return

    with task.lock:
        if task.cancel_requested:
            task.status = TaskStatus.CANCELLED
            task.finished_at = time.time()
            task.progress_message = "任务已取消"
            return
        task.status = TaskStatus.RUNNING
        task.started_at = time.time()
        task.error = ""
        task.progress_message = ""

    try:
        cfg = _get_cfg()
        if req.config_overrides:
            cfg = cfg.with_updates(**req.config_overrides)
        cfg = _apply_server_concurrency_limits(cfg)

        source = req.source
        task_type = req.type

        if task_type in ("social_long", "social_short") or (
            task_type == "auto" and source.startswith(("http://", "https://"))
        ):
            _execute_social_task(task, source, cfg, req)
        elif task_type in ("pdf", "video", "audio", "board", "pptx", "ppt", "docx", "doc", "html"):
            _execute_local_task(task, source, task_type, cfg, req)
        elif task_type == "auto":
            _execute_auto_task(task, source, cfg, req)
        else:
            raise ValueError(f"Unknown task type: {task_type}")

        if task.cancel_requested or task.reporter.is_cancelled:
            raise CancelledError("任务已取消")

        with task.lock:
            task.status = TaskStatus.COMPLETED
            task.finished_at = time.time()
            task.progress_message = "处理完成"
        logger.info("Task completed: %s -> %s", task_id, task.output_path)
    except CancelledError:
        _mark_cancelled(task)
        logger.info("Task cancelled: %s", task_id)
    except Exception as exc:
        with task.lock:
            task.status = TaskStatus.FAILED
            task.error = f"{type(exc).__name__}: {exc}\n{traceback.format_exc()}"
            task.finished_at = time.time()
        logger.error("Task failed: %s - %s", task_id, exc)


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "ocrllm"}


@app.post("/api/ocrllm/process", response_model=TaskResponse)
def submit_task(req: ProcessRequest):
    # --- H5: upfront validation ---
    source = req.source.strip()
    task_type = req.type.strip().lower()
    _KNOWN_TYPES = {"auto", "pdf", "video", "audio", "board",
                    "pptx", "ppt", "docx", "doc", "html",
                    "social_long", "social_short"}
    if task_type not in _KNOWN_TYPES:
        raise HTTPException(status_code=400, detail=f"Unknown task type: {task_type}")
    if not source.startswith(("http://", "https://")):
        if not os.path.exists(source):
            raise HTTPException(status_code=400, detail=f"Source file not found: {source}")

    task_id = str(uuid.uuid4())
    task = TaskState(task_id=task_id, task_type=task_type, source=source)
    _register_task(task)

    future = _executor.submit(_execute_task, task_id, req)
    with task.lock:
        task.future = future

    return TaskResponse(
        task_id=task_id,
        status=TaskStatus.PENDING.value,
        message=f"Task submitted: {req.type} -> {req.source}",
    )


@app.get("/api/ocrllm/status/{task_id}", response_model=TaskStatusResponse)
def get_task_status(task_id: str):
    task = _get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task not found: {task_id}")

    snapshot = task.tracker.get_snapshot()
    with task.lock:
        percent = float(snapshot.get("overall_percent", 0.0)) if snapshot else task.progress_percent
        if task.status == TaskStatus.COMPLETED and percent <= 0:
            percent = 100.0
        status = task.status.value
        progress_message = snapshot.get("status_message", "") if snapshot else ""
        if not progress_message:
            progress_message = task.progress_message
        return TaskStatusResponse(
            task_id=task.task_id,
            task_type=task.task_type,
            source=task.source,
            status=status,
            progress_percent=percent,
            progress_message=progress_message,
            output_path=task.output_path,
            error=task.error,
            created_at=task.created_at,
            started_at=task.started_at,
            finished_at=task.finished_at,
        )


@app.get("/api/ocrllm/result/{task_id}", response_model=TaskResultResponse)
def get_task_result(task_id: str):
    task = _get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task not found: {task_id}")

    with task.lock:
        status = task.status.value
        output_path = task.output_path
        error = task.error
        artifacts = dict(task.result_payload)

    content = _collect_result_content(task) if status == TaskStatus.COMPLETED.value else ""
    return TaskResultResponse(
        task_id=task.task_id,
        status=status,
        output_path=output_path,
        content=content,
        error=error,
        artifacts=artifacts,
    )


@app.post("/api/ocrllm/cancel/{task_id}", response_model=TaskResponse)
def cancel_task(task_id: str):
    task = _get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task not found: {task_id}")

    with task.lock:
        if task.status in {TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED}:
            return TaskResponse(task_id=task_id, status=task.status.value, message="Task already finished")
        task.cancel_requested = True
        task.reporter.cancel()
        future = task.future

    if future and future.cancel():
        _mark_cancelled(task)

    return TaskResponse(task_id=task_id, status=TaskStatus.CANCELLED.value, message="Cancel signal sent")


@app.get("/api/ocrllm/tasks")
def list_tasks(status: Optional[str] = None, limit: int = 50):
    with _tasks_lock:
        _prune_tasks_locked()
        tasks = list(_tasks.values())

    if status:
        filtered = []
        for task in tasks:
            with task.lock:
                if task.status.value == status:
                    filtered.append(task)
        tasks = filtered

    tasks.sort(key=lambda task: task.created_at, reverse=True)
    tasks = tasks[: max(1, min(limit, 500))]

    result = []
    for task in tasks:
        with task.lock:
            result.append(
                {
                    "task_id": task.task_id,
                    "task_type": task.task_type,
                    "source": task.source,
                    "status": task.status.value,
                    "created_at": task.created_at,
                    "output_path": task.output_path,
                }
            )
    return result
