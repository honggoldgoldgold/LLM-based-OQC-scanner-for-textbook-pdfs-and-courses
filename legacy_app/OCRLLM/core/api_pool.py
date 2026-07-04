"""
API 池 — 管理多个 API key，支持付费模式下的高并发。

付费模式: 使用所有空闲 API key 提高并行数量，各自独立识别。
免费模式: 仍使用单个 API key（当前行为不变）。
"""

from __future__ import annotations

import threading
import time
import logging
from threading import Event
from typing import Optional

from OCRLLM.config import AppConfig
from OCRLLM.core.provider_selection import uses_google_for_vision, visual_parallel_requests
from OCRLLM.core.providers.router import build_llm_client

logger = logging.getLogger(__name__)


class APISlot:
    """单个 API 槽位的状态。"""

    def __init__(self, key: str, client):
        self.key = key
        self.client = client
        self.active_requests: int = 0
        self.total_requests: int = 0
        self.error_count: int = 0
        self.last_used: float = 0.0
        self._lock = threading.Lock()

    def acquire(self) -> bool:
        """标记该槽位为活跃（递增活跃请求计数）。

        Returns:
            始终返回 True。
        """
        with self._lock:
            self.active_requests += 1
            self.total_requests += 1
            self.last_used = time.time()
            return True

    def release(self, error: bool = False):
        """释放该槽位（递减活跃请求计数）。

        Args:
            error: 本次请求是否出错。
        """
        with self._lock:
            self.active_requests = max(0, self.active_requests - 1)
            if error:
                self.error_count += 1

    @property
    def load(self) -> int:
        """当前活跃请求数（线程安全）。"""
        with self._lock:
            return self.active_requests


class APIPool:
    """线程安全的 API 池，支持多 key 负载均衡和并发上限。

    用法:
        pool = APIPool(cfg, api_keys=["sk-xxx", "sk-yyy"])

        # 获取最空闲的客户端（超过并发上限时阻塞等待）
        client = pool.acquire()
        try:
            result = client.chat_with_images(...)
        finally:
            pool.release(client)

        # 或使用上下文管理器
        with pool.get_client() as client:
            result = client.chat_with_images(...)
    """

    def __init__(self, cfg: AppConfig, api_keys: list[str] = None, paid_mode: bool = False):
        self._cfg = cfg
        self._paid_mode = paid_mode
        self._cond = threading.Condition(threading.Lock())
        self._cancel_event: Optional[Event] = None

        if paid_mode and api_keys and len(api_keys) > 1:
            self._slots = []
            for key in api_keys:
                key = key.strip()
                if not key:
                    continue
                if uses_google_for_vision(cfg):
                    # Google Gemini 限流按 project 而不是单个 API key 计算；
                    # 这里保留多 key 槽位接口，供后续接入项目级 API 池管理。
                    slot_cfg = cfg.with_updates(google_api={"api_key": key})
                else:
                    slot_cfg = cfg.with_updates(api={"api_key": key})
                client = build_llm_client(slot_cfg)
                self._slots.append(APISlot(key=key, client=client))
            logger.info("[API池] 付费模式: %d 个 API key", len(self._slots))
        else:
            # 免费模式或只有一个 key: 单客户端
            client = build_llm_client(cfg)
            slot_key = cfg.google_api.api_key if uses_google_for_vision(cfg) else cfg.api.api_key
            self._slots = [APISlot(key=slot_key, client=client)]
            logger.info("[API池] 免费/单 key 模式")

        # 并发上限: 每个 slot 最多 llm_parallel_requests 个并发
        self._max_per_slot = visual_parallel_requests(cfg)

    @property
    def pool_size(self) -> int:
        """API 池中的槽位数量。"""
        return len(self._slots)

    @property
    def max_parallel(self) -> int:
        """付费模式下可用的最大并行数。"""
        if self._paid_mode and len(self._slots) > 1:
            return self._max_per_slot * len(self._slots)
        return self._max_per_slot

    def acquire(self):
        """获取负载最低的客户端。若所有 slot 均达到并发上限则阻塞等待。

        Raises:
            CancelledError: 若在等待期间检测到取消事件。
        """
        from OCRLLM.core.task_runner import CancelledError

        with self._cond:
            while True:
                if self._cancel_event and self._cancel_event.is_set():
                    raise CancelledError("任务已取消")
                best = min(self._slots, key=lambda s: s.load)
                if best.load < self._max_per_slot:
                    best.acquire()
                    return best.client
                # 所有 slot 满载，等待释放通知
                self._cond.wait(timeout=1.0)

    def release(self, client, error: bool = False):
        """释放客户端并通知等待中的 acquire。"""
        with self._cond:
            for slot in self._slots:
                if slot.client is client:
                    slot.release(error)
                    self._cond.notify()
                    return

    def get_client(self) -> _PoolContext:
        """上下文管理器方式获取客户端。"""
        return _PoolContext(self)

    def get_stats(self) -> dict:
        """获取池状态统计。"""
        with self._cond:
            return {
                "pool_size": len(self._slots),
                "paid_mode": self._paid_mode,
                "slots": [
                    {
                        "key_suffix": s.key[-6:] if len(s.key) > 6 else "***",
                        "active": s.active_requests,
                        "total": s.total_requests,
                        "errors": s.error_count,
                    }
                    for s in self._slots
                ],
                "total_active": sum(s.active_requests for s in self._slots),
            }

    def get_single_client(self):
        """获取单个客户端（不做负载均衡，用于需要上下文连续的场景）。"""
        return self._slots[0].client

    def set_cancel_event(self, cancel_event: Optional[Event]):
        """为所有槽位客户端设置取消事件。

        Args:
            cancel_event: 线程取消事件，或 None 清除。
        """
        self._cancel_event = cancel_event
        for slot in self._slots:
            slot.client.set_cancel_event(cancel_event)


class _PoolContext:
    """API 池的上下文管理器。"""

    def __init__(self, pool: APIPool):
        self._pool = pool
        self._client = None

    def __enter__(self):
        self._client = self._pool.acquire()
        return self._client

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._client:
            self._pool.release(self._client, error=exc_type is not None)
        return False
