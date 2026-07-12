from __future__ import annotations

import io
import json
import os
import subprocess
import sys
import threading
from pathlib import Path

from ocrllm.worker import report_worker_internal_error


SOURCE_ROOT = Path(__file__).resolve().parents[1] / "src"
CAPABILITY_ID = "11111111-1111-4111-8111-111111111111"
RECOGNITION_ID = "22222222-2222-4222-8222-222222222222"


def _encode(record: dict[str, object]) -> str:
    return json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n"


def _worker_environment() -> dict[str, str]:
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(SOURCE_ROOT)
    environment.pop("DASHSCOPE_API_KEY", None)
    return environment


def test_module_entrypoint_serves_capabilities_without_credentials_or_network(
    tmp_path,
) -> None:
    command = {
        "protocol_version": "ocrllm.v1alpha1",
        "command": "capabilities",
        "request_id": CAPABILITY_ID,
    }

    completed = subprocess.run(
        [sys.executable, "-m", "ocrllm.worker"],
        cwd=tmp_path,
        env=_worker_environment(),
        input=_encode(command),
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
        timeout=30,
    )

    assert completed.returncode == 0, completed.stderr
    assert completed.stderr == ""
    lines = completed.stdout.splitlines()
    assert len(lines) == 1
    event = json.loads(lines[0])
    assert event["protocol_version"] == "ocrllm.v1alpha1"
    assert event["event"] == "capabilities"
    assert event["request_id"] == CAPABILITY_ID
    assert len(event["capabilities"]) == 20
    assert all("secret" not in line.lower() for line in lines)


def test_internal_error_reporter_writes_type_without_exception_message() -> None:
    stream = io.StringIO()

    report_worker_internal_error(RuntimeError("secret-sentinel"), stream=stream)

    diagnostic = stream.getvalue()
    assert diagnostic == "worker internal error type: builtins.RuntimeError\n"
    assert "secret-sentinel" not in diagnostic


def test_module_entrypoint_runs_isolated_image_job_without_provider_call(
    tmp_path,
) -> None:
    missing_source = (tmp_path / "课程 📚" / "missing board.png").resolve()
    command = {
        "protocol_version": "ocrllm.v1alpha1",
        "command": "recognize",
        "request_id": RECOGNITION_ID,
        "sources": [{"media_type": "image", "uri": missing_source.as_uri()}],
        "provider": "dashscope",
        "model": None,
        "input_languages": ["zh-Hans", "en"],
        "output_language": "zh-Hans",
        "profile": "board",
        "options": {},
    }
    process = subprocess.Popen(
        [sys.executable, "-m", "ocrllm.worker"],
        cwd=tmp_path,
        env=_worker_environment(),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    )
    events: list[dict[str, object]] = []

    def read_until_terminal() -> None:
        assert process.stdout is not None
        for line in process.stdout:
            event = json.loads(line)
            events.append(event)
            if event["event"] in {"result", "error"}:
                return

    reader = threading.Thread(target=read_until_terminal, daemon=True)
    try:
        assert process.stdin is not None
        process.stdin.write(_encode(command))
        process.stdin.flush()
        reader.start()
        reader.join(timeout=30)
        assert not reader.is_alive(), "worker did not emit a terminal event"
    finally:
        if process.stdin is not None and not process.stdin.closed:
            process.stdin.close()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=10)

    assert process.returncode == 0
    assert process.stderr is not None
    assert process.stderr.read() == ""
    assert [event["event"] for event in events] == [
        "accepted",
        "progress",
        "error",
    ]
    assert events[0]["request_id"] == RECOGNITION_ID
    assert events[1]["completed"] == 0
    assert events[1]["total"] == 1
    assert events[2]["code"] == "SOURCE_NOT_FOUND"
    assert events[2]["retryable"] is False
