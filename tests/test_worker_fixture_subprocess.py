from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ENTRYPOINT = Path(__file__).parent / "worker_fixture_entrypoint.py"
CAPABILITY_ID = "11111111-1111-4111-8111-111111111111"
RECOGNITION_ID = "22222222-2222-4222-8222-222222222222"
SOURCE_URI = (
    "file:///C:/Very%20Long%20Course%20Folder/"
    "%E8%AF%BE%E7%A8%8B%20%F0%9F%93%9A/board.png"
)


def _encode(record: dict[str, object]) -> str:
    return json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n"


def _recognize() -> dict[str, object]:
    return {
        "protocol_version": "ocrllm.v1alpha1",
        "command": "recognize",
        "request_id": RECOGNITION_ID,
        "sources": [{"media_type": "image", "uri": SOURCE_URI}],
        "provider": "dashscope",
        "model": None,
        "input_languages": ["zh-Hans", "en"],
        "output_language": "zh-Hans",
        "profile": "board",
        "options": {},
    }


def test_fixture_entrypoint_round_trips_protocol_over_real_os_pipes() -> None:
    stdin = (
        "not-json\n"
        + _encode(
            {
                "protocol_version": "ocrllm.v1alpha1",
                "command": "capabilities",
                "request_id": CAPABILITY_ID,
            }
        )
        + _encode(_recognize())
    )

    completed = subprocess.run(
        [sys.executable, "-I", str(ENTRYPOINT)],
        input=stdin,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
        timeout=30,
    )

    assert completed.returncode == 0, completed.stderr
    assert completed.stderr == ""
    lines = completed.stdout.splitlines()
    events = [json.loads(line) for line in lines]
    assert len(lines) == len(events) == 4
    assert [event["event"] for event in events] == [
        "error",
        "capabilities",
        "accepted",
        "result",
    ]
    assert events[0]["request_id"] is None
    assert events[0]["code"] == "COMMAND_INVALID"
    assert events[1]["request_id"] == CAPABILITY_ID
    assert len(events[1]["capabilities"]) == 19
    assert events[2]["request_id"] == RECOGNITION_ID
    assert events[3]["result"]["metadata"]["source_uris"] == [SOURCE_URI]
    assert all(line.startswith("{") and line.endswith("}") for line in lines)


def test_fixture_entrypoint_uses_fallback_version_and_recovers_valid_id() -> None:
    stdin = _encode(
        {
            "protocol_version": "ocrllm.v9",
            "command": "capabilities",
            "request_id": CAPABILITY_ID,
        }
    )

    completed = subprocess.run(
        [sys.executable, "-I", str(ENTRYPOINT)],
        input=stdin,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
        timeout=30,
    )

    assert completed.returncode == 0, completed.stderr
    event = json.loads(completed.stdout)
    assert event["protocol_version"] == "ocrllm.v1alpha1"
    assert event["request_id"] == CAPABILITY_ID
    assert event["code"] == "PROTOCOL_UNSUPPORTED"
