import os
import sys
import tempfile
import threading
import time
from types import SimpleNamespace

PROJECT_PARENT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_PARENT not in sys.path:
    sys.path.insert(0, PROJECT_PARENT)

from OCRLLM.api import server
from OCRLLM.config import AppConfig


def test_apply_output_override_treats_directory_as_directory_for_file_processors() -> None:
    with tempfile.TemporaryDirectory(prefix="ocrllm_api_output_") as td:
        cfg = AppConfig()
        spec = SimpleNamespace(output_target="file")

        next_cfg, kwargs = server._apply_output_override(cfg, spec, td)

        assert kwargs == {}
        assert os.path.abspath(td) == next_cfg.paths.output_dir


def test_assign_task_result_keeps_markdown_artifacts() -> None:
    task = server.TaskState(task_id="task-artifacts", task_type="video", source="demo.mp4")

    server._assign_task_result(
        task,
        {
            "board_md": "C:/tmp/board.md",
            "transcript_md": "C:/tmp/transcript.md",
            "output_dir": "C:/tmp/video",
            "frames": [{"id": 1}, {"id": 2}],
            "hotwords": ["matrix"],
        },
    )

    assert task.output_path == "C:/tmp/board.md"
    assert task.result_payload["transcript_md"] == "C:/tmp/transcript.md"
    assert task.result_payload["frames_count"] == 2


def test_execute_task_marks_running_cancel_as_cancelled() -> None:
    task_id = "task-cancel-running"
    task = server.TaskState(task_id=task_id, task_type="pdf", source="demo.pdf")
    server._register_task(task)

    original_execute_local = server._execute_local_task
    try:
        def _fake_execute_local(task_obj, source, task_type, cfg, req):
            while not task_obj.reporter.is_cancelled:
                time.sleep(0.01)
            task_obj.reporter.check_cancelled()

        server._execute_local_task = _fake_execute_local
        worker = threading.Thread(
            target=server._execute_task,
            args=(task_id, server.ProcessRequest(type="pdf", source="demo.pdf")),
            daemon=True,
        )
        worker.start()

        deadline = time.time() + 2
        while time.time() < deadline:
            with task.lock:
                if task.status == server.TaskStatus.RUNNING:
                    break
            time.sleep(0.01)

        response = server.cancel_task(task_id)
        worker.join(timeout=2)

        assert response.status == "cancelled"
        assert not worker.is_alive()
        with task.lock:
            assert task.status == server.TaskStatus.CANCELLED
            assert "CancelledError" not in task.error
            assert task.finished_at > 0
    finally:
        server._execute_local_task = original_execute_local
        with server._tasks_lock:
            server._tasks.pop(task_id, None)


def test_get_task_result_combines_board_and_transcript_content() -> None:
    with tempfile.TemporaryDirectory(prefix="ocrllm_api_result_") as td:
        board_md = os.path.join(td, "board.md")
        transcript_md = os.path.join(td, "transcript.md")
        with open(board_md, "w", encoding="utf-8") as file_handle:
            file_handle.write("Board content")
        with open(transcript_md, "w", encoding="utf-8") as file_handle:
            file_handle.write("Transcript content")

        task_id = "task-result-content"
        task = server.TaskState(task_id=task_id, task_type="video", source="demo.mp4")
        with task.lock:
            task.status = server.TaskStatus.COMPLETED
            task.output_path = board_md
            task.result_payload = {
                "board_md": board_md,
                "transcript_md": transcript_md,
            }
        server._register_task(task)

        try:
            response = server.get_task_result(task_id)
            assert response.status == "completed"
            assert "Board content" in response.content
            assert "Transcript content" in response.content
            assert response.artifacts["transcript_md"] == transcript_md
        finally:
            with server._tasks_lock:
                server._tasks.pop(task_id, None)


if __name__ == "__main__":
    test_apply_output_override_treats_directory_as_directory_for_file_processors()
    test_assign_task_result_keeps_markdown_artifacts()
    test_execute_task_marks_running_cancel_as_cancelled()
    test_get_task_result_combines_board_and_transcript_content()
    print("PASS: API server guards")
