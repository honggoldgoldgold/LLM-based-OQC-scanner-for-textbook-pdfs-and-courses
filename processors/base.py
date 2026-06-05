"""
处理器基类 — 定义统一接口和进度报告。
"""

from __future__ import annotations

from concurrent.futures import FIRST_COMPLETED, wait
import logging
from typing import Optional

from OCRLLM.config import AppConfig
from OCRLLM.core.document_model import SourceType, UnifiedDocument
from OCRLLM.core.llm_client import LLMClient
from OCRLLM.core.task_runner import ProgressReporter
from OCRLLM.core.progress_tracker import ProgressTracker
from OCRLLM.core.checkpoint import CheckpointManager
from OCRLLM.core.api_pool import APIPool

logger = logging.getLogger(__name__)


class BaseProcessor:
    """所有处理器的基类。通过构造函数注入依赖。"""

    processor_key = "base"
    display_name = "基础处理器"
    supported_extensions: tuple[str, ...] = ()
    source_type = SourceType.UNKNOWN
    requires_llm = True

    def __init__(
        self,
        cfg: Optional[AppConfig] = None,
        llm: Optional[LLMClient] = None,
        reporter: Optional[ProgressReporter] = None,
        tracker: Optional[ProgressTracker] = None,
        api_pool: Optional[APIPool] = None,
    ):
        self.cfg = cfg or AppConfig()
        self.reporter = reporter or ProgressReporter()
        self.tracker = tracker or ProgressTracker()
        self.checkpoint_mgr = CheckpointManager(self.cfg.paths.output_dir)

        if not self.requires_llm:
            self.api_pool = None
            self.llm = llm
            return

        # API 池：如有提供则使用，否则根据 paid_mode 自动创建
        if api_pool:
            self.api_pool = api_pool
            self.llm = llm or api_pool.get_single_client()
        elif self.cfg.api.paid_mode and self.cfg.api.api_keys:
            self.api_pool = APIPool(self.cfg, self.cfg.api.api_keys, paid_mode=True)
            self.llm = llm or self.api_pool.get_single_client()
        else:
            self.api_pool = APIPool(self.cfg)
            self.llm = llm or self.api_pool.get_single_client()

        self.api_pool.set_cancel_event(self.reporter.cancel_event)
        if self.llm:
            self.llm.set_cancel_event(self.reporter.cancel_event)

    def _report(self, current: int, total: int, msg: str):
        self.reporter.progress(current, total, msg)

    def _report_content(self, text: str, label: str = ""):
        self.reporter.content(text, label)

    def _check_cancelled(self):
        self.reporter.check_cancelled()

    def _sleep(self, seconds: float):
        self.reporter.wait(seconds)

    def _iter_completed_futures(self, futures: set, poll_interval: float = 0.25):
        pending = set(futures)
        while pending:
            self._check_cancelled()
            done, pending = wait(
                pending,
                timeout=poll_interval,
                return_when=FIRST_COMPLETED,
            )
            if not done:
                continue
            for future in done:
                yield future

    @staticmethod
    def _cancel_futures(futures):
        for future in futures:
            future.cancel()

    @classmethod
    def describe_processor(cls) -> dict:
        """返回处理器的元信息字典。

        Returns:
            包含 key、display_name、supported_extensions、source_type 的字典。
        """
        return {
            "key": cls.processor_key,
            "display_name": cls.display_name,
            "supported_extensions": cls.supported_extensions,
            "source_type": cls.source_type.value if isinstance(cls.source_type, SourceType) else str(cls.source_type),
        }

    def process_to_document(self, source_path: str, **kwargs) -> UnifiedDocument:
        """将源文件处理为统一文档模型（子类实现）。

        Args:
            source_path: 源文件路径。
            **kwargs: 处理器特定参数。

        Returns:
            UnifiedDocument 实例。

        Raises:
            NotImplementedError: 子类未实现时抛出。
        """
        raise NotImplementedError(f"{self.__class__.__name__}.process_to_document 尚未实现")
