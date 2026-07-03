"""
进度报告 & 协作取消 — 用于 GUI 和 CLI 的任务生命周期管理。
"""

from __future__ import annotations

import logging
import threading
import time
from typing import Callable, Optional

logger = logging.getLogger(__name__)


class CancelledError(Exception):
    """任务被用户取消。"""


class ProgressReporter:
    """线程安全的进度报告器，支持协作式取消。

    处理器在每次 progress() / check_cancelled() 时检查取消标志，
    若检测到取消则抛出 CancelledError，沿调用栈自然退出。
    """

    def __init__(
        self,
        on_progress: Optional[Callable[[int, int, str], None]] = None,
        on_content: Optional[Callable[[str, str], None]] = None,
        on_log: Optional[Callable[[str], None]] = None,
    ):
        self.on_progress = on_progress
        self.on_content = on_content
        self.on_log = on_log
        self._cancelled = threading.Event()

    def cancel(self):
        """请求取消（线程安全）。"""
        self._cancelled.set()

    @property
    def is_cancelled(self) -> bool:
        """取消标志是否已设置。"""
        return self._cancelled.is_set()

    @property
    def cancel_event(self) -> threading.Event:
        """底层 threading.Event 对象，供需要直接等待的场景使用。"""
        return self._cancelled

    def check_cancelled(self):
        """若已请求取消，抛出 CancelledError。"""
        if self._cancelled.is_set():
            raise CancelledError("任务已取消")

    def wait(self, seconds: float, poll_interval: float = 0.2):
        """可取消的等待，用于替代长时间 sleep。"""
        if seconds <= 0:
            return
        deadline = time.monotonic() + seconds
        while True:
            self.check_cancelled()
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                return
            self._cancelled.wait(min(poll_interval, remaining))

    def progress(self, current: int, total: int, msg: str):
        """报告进度并检查取消。

        Args:
            current: 当前步数。
            total: 总步数。
            msg: 进度描述文本。

        Raises:
            CancelledError: 若取消标志已设置。
        """
        self.check_cancelled()
        logger.info("(%d/%d) %s", current, total, msg)
        if self.on_progress:
            self.on_progress(current, total, msg)

    def content(self, text: str, label: str = ""):
        """报告处理结果内容。

        Args:
            text: 内容文本。
            label: 内容标签/标题。
        """
        if self.on_content:
            self.on_content(text, label)

    def log(self, msg: str):
        """发送日志消息。

        Args:
            msg: 日志消息文本。
        """
        logger.info(msg)
        if self.on_log:
            self.on_log(msg)
