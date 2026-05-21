"""
STAv2 ↔ OCRLLM 桥接插件（接口定义）。

此文件定义了 STAv2 侧的 OCRLLM 集成接口。
当前阶段仅作为接口文档和参考实现，不修改 STAv2 代码。

集成方式: STAv2 通过 HTTP 调用 OCRLLM FastAPI 服务（端口 8100）。

STAv2 侧需要:
1. 在 src/plugins/ 新建 ocrllm_bridge.py（实现如下 OcrllmBridgePlugin）
2. 在 src/app_container.py 的 _load_runtime_plugins() 中注册
3. 在 src/core/job_worker.py 新增 ocrllm_process job type
"""

from __future__ import annotations

import logging
import os
from typing import Any, Optional

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# OCRLLM API 客户端（供 STAv2 调用）
# ---------------------------------------------------------------------------

OCRLLM_API_BASE = os.environ.get("OCRLLM_API_URL", "http://localhost:8100")

MEDIA_EXTENSIONS = {
    ".pdf", ".mp4", ".avi", ".mkv", ".mov", ".flv", ".wmv",
    ".mp3", ".m4a", ".wav", ".aac", ".flac",
}


class OcrllmApiClient:
    """OCRLLM HTTP API 客户端。

    STAv2 的 JobWorker 或 Plugin 通过此客户端调用 OCRLLM 服务。

    用法::

        client = OcrllmApiClient()
        task_id = client.submit("pdf", "/path/to/file.pdf")
        status = client.get_status(task_id)
        result = client.get_result(task_id)
    """

    def __init__(self, base_url: str = OCRLLM_API_BASE):
        self.base_url = base_url.rstrip("/")

    def health(self) -> dict:
        import requests
        resp = requests.get(f"{self.base_url}/api/health", timeout=5)
        resp.raise_for_status()
        return resp.json()

    def submit(
        self,
        task_type: str,
        source: str,
        output_dir: str = "",
        config_overrides: dict = None,
    ) -> str:
        """提交处理任务，返回 task_id。"""
        import requests
        payload = {
            "type": task_type,
            "source": source,
            "output_dir": output_dir,
            "config_overrides": config_overrides or {},
        }
        resp = requests.post(
            f"{self.base_url}/api/ocrllm/process",
            json=payload,
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()["task_id"]

    def get_status(self, task_id: str) -> dict:
        """查询任务状态。"""
        import requests
        resp = requests.get(
            f"{self.base_url}/api/ocrllm/status/{task_id}",
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()

    def get_result(self, task_id: str) -> dict:
        """获取任务结果。"""
        import requests
        resp = requests.get(
            f"{self.base_url}/api/ocrllm/result/{task_id}",
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()

    def cancel(self, task_id: str) -> dict:
        """取消任务。"""
        import requests
        resp = requests.post(
            f"{self.base_url}/api/ocrllm/cancel/{task_id}",
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()

    def is_available(self) -> bool:
        """检查 OCRLLM 服务是否可用。"""
        try:
            self.health()
            return True
        except Exception:
            return False


# ---------------------------------------------------------------------------
# STAv2 Plugin 接口定义（参考实现）
# ---------------------------------------------------------------------------


class OcrllmBridgePlugin:
    """STAv2 OCRLLM 桥接插件。

    集成到 STAv2 的 PluginManager:

        # src/app_container.py
        from src.plugins.ocrllm_bridge import OcrllmBridgePlugin as _OcrllmBridge

        def _load_runtime_plugins(self):
            ...
            self.plugin_manager.load_plugin(_OcrllmBridge, name="OCRLLM Bridge")

    事件流:
        FILE_CREATED → 检测是否为媒体文件 → 提交 OCRLLM Job → 轮询完成 → 写 proxy.md

    注意: 此类继承自 STAv2 的 BasePlugin，此处仅定义接口结构。
    实际部署时需要放在 STAv2/STA/src/plugins/ocrllm_bridge.py。
    """

    def __init__(self, name: str, event_bus: Any, db_manager: Any):
        self.name = name
        self.bus = event_bus
        self.db = db_manager
        self.client = OcrllmApiClient()
        self._pending_tasks: dict[str, dict] = {}  # task_id → {file_id, source_path, ...}

    def start(self):
        """订阅文件创建事件。"""
        self.bus.subscribe("FILE_CREATED", self._on_file_created)
        self.bus.subscribe("FILE_UPDATED", self._on_file_updated)
        logger.info("OCRLLM Bridge Plugin started")

    def stop(self):
        """清理资源。"""
        logger.info("OCRLLM Bridge Plugin stopped")

    def _on_file_created(self, payload: dict):
        """处理新文件事件。"""
        path = payload.get("absolute_path", "")
        if not self._is_processable(path):
            return

        if not self.client.is_available():
            logger.warning("OCRLLM 服务不可用，跳过自动处理: %s", path)
            return

        self._submit_processing(payload)

    def _on_file_updated(self, payload: dict):
        """处理文件更新事件（通常不需要重新处理）。"""
        pass

    def _is_processable(self, path: str) -> bool:
        """检查文件是否需要 OCRLLM 处理。"""
        ext = os.path.splitext(path)[1].lower()
        return ext in MEDIA_EXTENSIONS

    def _determine_task_type(self, path: str) -> str:
        """根据文件扩展名确定处理类型。"""
        ext = os.path.splitext(path)[1].lower()
        if ext == ".pdf":
            return "pdf"
        elif ext in (".mp4", ".avi", ".mkv", ".mov", ".flv", ".wmv"):
            return "video"
        elif ext in (".mp3", ".m4a", ".wav", ".aac", ".flac"):
            return "audio"
        return "auto"

    def _submit_processing(self, payload: dict):
        """提交文件处理任务。"""
        path = payload["absolute_path"]
        file_id = payload.get("file_id", "")
        task_type = self._determine_task_type(path)

        # 输出到同目录，proxy 文件名
        output_dir = os.path.dirname(path)

        try:
            task_id = self.client.submit(task_type, path, output_dir)
            self._pending_tasks[task_id] = {
                "file_id": file_id,
                "source_path": path,
                "task_type": task_type,
            }
            logger.info("OCRLLM 任务已提交: %s → %s (%s)", task_id, path, task_type)
        except Exception as exc:
            logger.error("OCRLLM 任务提交失败: %s — %s", path, exc)


# ---------------------------------------------------------------------------
# STAv2 Job Type 定义（参考）
# ---------------------------------------------------------------------------

# 在 STAv2 的 job_worker.py 中新增:
#
# elif job_type == "ocrllm_process":
#     scope = parse_scope_key(scope_key)
#     # scope_key 格式: "file_uid:xxx|type:pdf|source:/path/to/file.pdf"
#     client = OcrllmApiClient()
#     task_id = client.submit(
#         scope["type"],
#         scope["source"],
#         output_dir=scope.get("output_dir", ""),
#     )
#     # 轮询直到完成
#     import time
#     for _ in range(3600):  # 最多等 1 小时
#         status = client.get_status(task_id)
#         if status["status"] in ("completed", "failed", "cancelled"):
#             break
#         time.sleep(2)
#     result = client.get_result(task_id)
#     if result["status"] == "completed":
#         return {"output_path": result["output_path"]}
#     raise RuntimeError(result.get("error", "OCRLLM task failed"))


# ---------------------------------------------------------------------------
# EventBus 事件定义（OCRLLM 侧发布）
# ---------------------------------------------------------------------------

OCRLLM_EVENTS = {
    "OCRLLM_TASK_SUBMITTED": "OCRLLM 任务已提交",
    "OCRLLM_TASK_PROGRESS": "OCRLLM 任务进度更新",
    "OCRLLM_TASK_COMPLETED": "OCRLLM 任务完成",
    "OCRLLM_TASK_FAILED": "OCRLLM 任务失败",
}

# STAv2 EventBus 事件 payload 格式:
#
# OCRLLM_TASK_SUBMITTED:
#   {task_id, task_type, source_path, file_uid}
#
# OCRLLM_TASK_PROGRESS:
#   {task_id, percent, message}
#
# OCRLLM_TASK_COMPLETED:
#   {task_id, output_path, file_uid}
#
# OCRLLM_TASK_FAILED:
#   {task_id, error, file_uid}
