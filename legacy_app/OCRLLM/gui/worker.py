"""
后台任务 Worker — 通过 ProgressReporter + Qt 信号桥接。

线程安全架构:
  - 不使用 QThread.terminate()（危险，可能死锁/损坏数据）
  - 通过 ProgressReporter 的协作式取消: cancel() 设置标志，
    处理器在下一次 reporter.progress() 时检测并抛出 CancelledError。
"""

from __future__ import annotations

import logging
import traceback
from typing import Callable, Optional

from PyQt5.QtCore import QObject, QThread, QTimer, pyqtSignal

from OCRLLM.core.task_runner import ProgressReporter, CancelledError
from OCRLLM.core.progress_tracker import ProgressTracker

logger = logging.getLogger(__name__)


class GuiWorker(QObject):
    """
    线程安全的后台任务执行器。

    用法:
        worker = GuiWorker()
        worker.progress.connect(on_progress)
        worker.content.connect(on_content)
        worker.finished_ok.connect(on_done)
        worker.finished_err.connect(on_error)
        worker.start(my_task_function)

    task_function 签名:
        def my_task(reporter: ProgressReporter) -> str:
            reporter.progress(1, 10, "步骤1...")
            reporter.content("识别结果", "标签")
            return "完成信息"
    """

    progress = pyqtSignal(int, int, str)
    content = pyqtSignal(str, str)
    log = pyqtSignal(str)
    finished_ok = pyqtSignal(str)
    finished_err = pyqtSignal(str)
    done = pyqtSignal()
    # 进度追踪信号: 友好文字 + 百分比 + 阶段快照
    progress_detail = pyqtSignal(str, float, dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._thread: Optional[QThread] = None
        self._reporter: Optional[ProgressReporter] = None
        self._tracker: Optional[ProgressTracker] = None
        self._poll_timer: Optional[QTimer] = None

    @property
    def is_running(self) -> bool:
        """后台任务线程是否正在运行。"""
        return self._thread is not None and self._thread.isRunning()

    @property
    def tracker(self) -> Optional[ProgressTracker]:
        """当前进度追踪器实例。"""
        return self._tracker

    def start(self, task_func: Callable[[ProgressReporter], str], tracker: ProgressTracker = None):
        """启动后台任务线程。

        Args:
            task_func: 任务函数，签名为 ``(ProgressReporter) -> str``。
            tracker: 进度追踪器实例，为 None 则自动创建。
        """
        if self.is_running:
            return

        reporter = ProgressReporter(
            on_progress=self._emit_progress,
            on_content=self._emit_content,
        )
        self._reporter = reporter
        self._tracker = tracker or ProgressTracker()

        self._thread = _WorkerThread(task_func, reporter)
        self._thread.result_ok.connect(self._on_ok)
        self._thread.result_err.connect(self._on_err)
        self._thread.finished.connect(self._on_finished)
        self._thread.start()

        # 轮询共享状态代价很低，1 秒刷新能显著改善长任务的进度观感。
        self._poll_timer = QTimer(self)
        self._poll_timer.timeout.connect(self._poll_progress)
        self._poll_timer.start(1000)

    def cancel(self):
        """协作式取消: 设置标志并等待线程自然退出。"""
        self.request_cancel()
        if self._thread and self._thread.isRunning():
            self._thread.wait(15000)

    def request_cancel(self):
        """仅请求取消，不阻塞当前线程等待完成。"""
        if self._reporter:
            self._reporter.cancel()

    def _emit_progress(self, current: int, total: int, msg: str):
        self.progress.emit(current, total, msg)

    def _emit_content(self, text: str, label: str):
        self.content.emit(text, label)

    def _on_ok(self, msg: str):
        self.finished_ok.emit(msg)

    def _on_err(self, msg: str):
        self.finished_err.emit(msg)

    def _on_finished(self):
        if self._poll_timer:
            self._poll_timer.stop()
            self._poll_timer = None
        self._thread = None
        self._reporter = None
        self.done.emit()

    def _poll_progress(self):
        """定时轮询进度追踪器，发送人类友好的进度消息。"""
        if not self._tracker:
            return
        try:
            snap = self._tracker.get_snapshot()
            msg = self._tracker.get_friendly_message()
            pct = snap.get("overall_percent", 0.0)
            if msg:
                self.progress_detail.emit(msg, pct, snap)
        except Exception:
            pass


class _WorkerThread(QThread):
    """内部线程 — 仅运行 task_func，不触碰 sys.stdout。"""
    result_ok = pyqtSignal(str)
    result_err = pyqtSignal(str)

    def __init__(self, task_func, reporter: ProgressReporter):
        super().__init__()
        self._task_func = task_func
        self._reporter = reporter

    def run(self):
        try:
            msg = self._task_func(self._reporter) or "完成"
            self.result_ok.emit(msg)
        except CancelledError:
            self.result_err.emit("任务已取消")
        except Exception as e:
            tb = traceback.format_exc()
            self.result_err.emit(f"{e}\n\n{tb}")
