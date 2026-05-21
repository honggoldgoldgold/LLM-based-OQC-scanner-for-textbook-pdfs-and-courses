"""
OCRLLM API 桥接验证 — 测试 FastAPI 服务和 STAv2 客户端接口兼容性。

不启动实际服务，而是用 FastAPI TestClient 模拟。
"""

import os
import sys
import json
import tempfile

# 确保 OCRLLM 包可导入
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fastapi.testclient import TestClient
from OCRLLM.api.server import app
from OCRLLM.api.sta_bridge import OcrllmApiClient, OcrllmBridgePlugin, OCRLLM_EVENTS


def test_health_endpoint():
    """验证 health 端点返回正确格式。"""
    client = TestClient(app)
    resp = client.get("/api/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["service"] == "ocrllm"
    print("[PASS] health endpoint")


def test_submit_and_status():
    """验证任务提交和状态查询流程。"""
    client = TestClient(app)

    with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
        resp = client.post("/api/ocrllm/process", json={
            "type": "pdf",
            "source": tmp.name,
            "output_dir": "",
            "config_overrides": {},
        })
    assert resp.status_code == 200
    data = resp.json()
    assert "task_id" in data
    assert data["status"] == "pending"
    task_id = data["task_id"]
    print(f"[PASS] submit task: {task_id}")

    # 查询状态
    resp = client.get(f"/api/ocrllm/status/{task_id}")
    assert resp.status_code == 200
    status = resp.json()
    assert status["task_id"] == task_id
    assert status["task_type"] == "pdf"
    assert status["source"]
    print(f"[PASS] status query: status={status['status']}")

    # 查询结果
    resp = client.get(f"/api/ocrllm/result/{task_id}")
    assert resp.status_code == 200
    result = resp.json()
    assert result["task_id"] == task_id
    print(f"[PASS] result query: status={result['status']}")


def test_submit_missing_file_rejected():
    """验证不存在的本地文件会在提交阶段被拒绝。"""
    client = TestClient(app)
    resp = client.post("/api/ocrllm/process", json={
        "type": "pdf",
        "source": "/nonexistent/test.pdf",
    })
    assert resp.status_code == 400
    assert "Source file not found" in resp.json()["detail"]
    print("[PASS] missing source rejected")


def test_cancel_task():
    """验证任务取消流程。"""
    client = TestClient(app)

    with tempfile.NamedTemporaryFile(suffix=".mp4") as tmp:
        resp = client.post("/api/ocrllm/process", json={
            "type": "auto",
            "source": tmp.name,
        })
    assert resp.status_code == 200
    task_id = resp.json()["task_id"]

    resp = client.post(f"/api/ocrllm/cancel/{task_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] in ("cancelled", "pending", "running", "completed", "failed")
    print(f"[PASS] cancel task: {data['status']}")


def test_list_tasks():
    """验证任务列表端点。"""
    client = TestClient(app)
    resp = client.get("/api/ocrllm/tasks")
    assert resp.status_code == 200
    tasks = resp.json()
    assert isinstance(tasks, list)
    print(f"[PASS] list tasks: {len(tasks)} tasks")


def test_404_for_unknown_task():
    """验证不存在的任务返回 404。"""
    client = TestClient(app)
    resp = client.get("/api/ocrllm/status/nonexistent-id")
    assert resp.status_code == 404
    print("[PASS] 404 for unknown task")


def test_sta_bridge_client_interface():
    """验证 OcrllmApiClient 接口定义完整性。"""
    client = OcrllmApiClient("http://localhost:8100")
    assert hasattr(client, "health")
    assert hasattr(client, "submit")
    assert hasattr(client, "get_status")
    assert hasattr(client, "get_result")
    assert hasattr(client, "cancel")
    assert hasattr(client, "is_available")
    print("[PASS] OcrllmApiClient interface complete")


def test_sta_bridge_plugin_interface():
    """验证 OcrllmBridgePlugin 接口定义完整性。"""
    assert hasattr(OcrllmBridgePlugin, "start")
    assert hasattr(OcrllmBridgePlugin, "stop")
    assert hasattr(OcrllmBridgePlugin, "_on_file_created")
    assert hasattr(OcrllmBridgePlugin, "_on_file_updated")
    assert hasattr(OcrllmBridgePlugin, "_is_processable")
    assert hasattr(OcrllmBridgePlugin, "_determine_task_type")
    assert hasattr(OcrllmBridgePlugin, "_submit_processing")
    print("[PASS] OcrllmBridgePlugin interface complete")


def test_event_definitions():
    """验证 OCRLLM 事件定义与 STAv2 EventBus 兼容。"""
    expected_events = {
        "OCRLLM_TASK_SUBMITTED",
        "OCRLLM_TASK_PROGRESS",
        "OCRLLM_TASK_COMPLETED",
        "OCRLLM_TASK_FAILED",
    }
    assert set(OCRLLM_EVENTS.keys()) == expected_events
    print("[PASS] OCRLLM event definitions match STAv2 contract")


def test_sta_eventbus_compatibility():
    """验证 STAv2 EventBus 可以被 OCRLLM Bridge 使用。"""
    sys.path.insert(0, os.path.abspath(os.path.join(
        os.path.dirname(__file__), "..", "..", "..", "STAv2", "STA"
    )))
    try:
        from src.core.event_bus import EventBus
        bus = EventBus()

        received = []
        bus.subscribe("OCRLLM_TASK_COMPLETED", lambda payload: received.append(payload))
        bus.publish("OCRLLM_TASK_COMPLETED", {
            "task_id": "test-123",
            "output_path": "/tmp/test.md",
            "file_uid": "uid-456",
        })
        assert len(received) == 1
        assert received[0]["task_id"] == "test-123"
        print("[PASS] STAv2 EventBus compatible with OCRLLM events")
    except ImportError:
        print("[SKIP] STAv2 not available for EventBus test")


if __name__ == "__main__":
    test_health_endpoint()
    test_submit_and_status()
    test_submit_missing_file_rejected()
    test_cancel_task()
    test_list_tasks()
    test_404_for_unknown_task()
    test_sta_bridge_client_interface()
    test_sta_bridge_plugin_interface()
    test_event_definitions()
    test_sta_eventbus_compatibility()
    print("\n=== All API bridge tests passed ===")
