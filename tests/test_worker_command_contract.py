from __future__ import annotations

import json
from dataclasses import FrozenInstanceError
from pathlib import Path
from types import MappingProxyType

import pytest

from ocrllm.contracts import (
    CancelCommand,
    CapabilitiesCommand,
    ImageRecognitionRequest,
    SourceDescriptor,
    parse_jsonl_command,
    parse_worker_command,
    serialize_worker_command,
)
from ocrllm.errors import ConfigError, OCRLLMError


FIXTURE = Path(__file__).parent / "fixtures" / "worker" / "v1alpha1_commands.jsonl"
REQUEST_ID = "22222222-2222-4222-8222-222222222222"
SOURCE_URI = "file:///C:/Course%20Data/%E8%AE%B2%E4%B9%89%F0%9F%93%9D.png"


def _recognize_command(**overrides: object) -> dict[str, object]:
    command: dict[str, object] = {
        "protocol_version": "ocrllm.v1alpha1",
        "command": "recognize",
        "request_id": REQUEST_ID,
        "sources": [{"media_type": "image", "uri": SOURCE_URI}],
        "provider": "dashscope",
        "model": "qwen3.7-plus-2026-05-26",
        "input_languages": ["zh-Hans", "en"],
        "output_language": "zh-Hans",
        "profile": "board",
        "options": {},
    }
    command.update(overrides)
    return command


def test_frozen_command_fixture_covers_all_three_commands() -> None:
    lines = FIXTURE.read_text(encoding="utf-8").splitlines()
    commands = [parse_jsonl_command(line) for line in lines]

    assert [type(command) for command in commands] == [
        CapabilitiesCommand,
        ImageRecognitionRequest,
        CancelCommand,
    ]
    assert [command.command for command in commands] == [
        "capabilities",
        "recognize",
        "cancel",
    ]
    assert serialize_worker_command(commands[1]) == json.loads(lines[1])


def test_recognize_defaults_are_explicit_and_immutable() -> None:
    raw = _recognize_command(options={})
    command = parse_worker_command(raw)

    assert isinstance(command, ImageRecognitionRequest)
    assert command.options == {
        "output_directory_uri": None,
        "overwrite": False,
        "timeout_seconds": 120,
    }
    assert isinstance(command.options, MappingProxyType)
    with pytest.raises(TypeError):
        command.options["overwrite"] = True  # type: ignore[index]
    with pytest.raises(FrozenInstanceError):
        command.profile = "board"  # type: ignore[misc]


def test_constructor_copies_sources_languages_and_options() -> None:
    sources = [SourceDescriptor(media_type="image", uri=SOURCE_URI)]
    languages = ["zh-Hans"]
    options = {"overwrite": False}
    command = ImageRecognitionRequest(
        request_id=REQUEST_ID,
        sources=tuple(sources),
        provider="dashscope",
        model=None,
        input_languages=tuple(languages),
        options=options,
    )

    sources.clear()
    languages.clear()
    options["overwrite"] = True

    assert len(command.sources) == 1
    assert command.input_languages == ("zh-Hans",)
    assert command.options["overwrite"] is False


def test_serialization_returns_fresh_mutable_json_values() -> None:
    command = parse_worker_command(_recognize_command())
    serialized = serialize_worker_command(command)
    serialized_options = serialized["options"]
    assert isinstance(serialized_options, dict)
    serialized_options["overwrite"] = True

    assert isinstance(command, ImageRecognitionRequest)
    assert command.options["overwrite"] is False


@pytest.mark.parametrize(
    "line",
    [
        "",
        "[]",
        "{} {}",
        '{"protocol_version":"ocrllm.v1alpha1","command":"capabilities",'
        '"command":"cancel","request_id":"11111111-1111-4111-8111-111111111111"}',
        '{"protocol_version":"ocrllm.v1alpha1","command":"recognize",'
        '"request_id":"22222222-2222-4222-8222-222222222222","sources":[],"provider":"dashscope",'
        '"model":null,"input_languages":[],"output_language":null,"profile":"board",'
        '"options":{"timeout_seconds":NaN}}',
    ],
)
def test_invalid_json_records_fail_as_command_invalid(line: str) -> None:
    with pytest.raises(OCRLLMError) as caught:
        parse_jsonl_command(line)

    assert caught.value.code == "COMMAND_INVALID"


def test_unsupported_protocol_has_distinct_stable_code() -> None:
    raw = {
        "protocol_version": "ocrllm.v9-secret-sentinel",
        "command": "capabilities",
        "request_id": "11111111-1111-4111-8111-111111111111",
    }
    with pytest.raises(OCRLLMError) as caught:
        parse_worker_command(raw)

    assert caught.value.code == "PROTOCOL_UNSUPPORTED"
    assert "secret-sentinel" not in str(caught.value)


@pytest.mark.parametrize(
    "raw",
    [
        {"protocol_version": "ocrllm.v1alpha1", "command": "capabilities"},
        {
            "protocol_version": "ocrllm.v1alpha1",
            "command": "capabilities",
            "request_id": "11111111-1111-4111-8111-111111111111",
            "extra": True,
        },
        {
            "protocol_version": "ocrllm.v1alpha1",
            "command": "unknown",
            "request_id": "11111111-1111-4111-8111-111111111111",
        },
        {
            "protocol_version": "ocrllm.v1alpha1",
            "command": "cancel",
            "request_id": "{22222222-2222-4222-8222-222222222222}",
        },
    ],
)
def test_invalid_command_envelopes_fail_closed(raw: object) -> None:
    with pytest.raises(OCRLLMError) as caught:
        parse_worker_command(raw)
    assert caught.value.code == "COMMAND_INVALID"


@pytest.mark.parametrize(
    ("overrides", "message"),
    [
        ({"sources": []}, "sources"),
        ({"sources": [{"media_type": "pdf", "uri": SOURCE_URI}]}, "images"),
        (
            {"sources": [{"media_type": "image", "uri": "https://example.test/a.png"}]},
            "configuration",
        ),
        (
            {"sources": [{"media_type": "image", "uri": "file:///C:/bad path/a.png"}]},
            "configuration",
        ),
        (
            {"sources": [{"media_type": "image", "uri": "file:///C:/bad%ZZ/a.png"}]},
            "configuration",
        ),
        (
            {"sources": [{"media_type": "image", "uri": "file://host:bad/a.png"}]},
            "configuration",
        ),
        ({"provider": "google"}, "provider"),
        ({"model": ""}, "model"),
        ({"input_languages": ["zh_Hans"]}, "languages"),
        ({"output_language": 3}, "languages"),
        ({"profile": "handwriting"}, "profile"),
        ({"options": {"api_key": "secret-sentinel"}}, "unknown"),
        ({"options": {"overwrite": 1}}, "overwrite"),
        ({"options": {"timeout_seconds": True}}, "timeout_seconds"),
        ({"options": {"timeout_seconds": 0}}, "timeout_seconds"),
        ({"options": {"timeout_seconds": 601}}, "timeout_seconds"),
        ({"options": {"output_directory_uri": "out"}}, "output_directory_uri"),
    ],
)
def test_invalid_recognition_configuration_is_typed_and_redacted(
    overrides: dict[str, object],
    message: str,
) -> None:
    with pytest.raises(ConfigError, match=message) as caught:
        parse_worker_command(_recognize_command(**overrides))

    assert caught.value.code == "CONFIG_INVALID"
    assert "secret-sentinel" not in str(caught.value)


def test_recognize_rejects_unknown_envelope_fields_before_configuration() -> None:
    raw = _recognize_command(api_key="secret-sentinel")
    with pytest.raises(OCRLLMError) as caught:
        parse_worker_command(raw)

    assert caught.value.code == "COMMAND_INVALID"
    assert "secret-sentinel" not in str(caught.value)


def test_source_and_output_uris_accept_unicode_emoji_spaces_and_unc() -> None:
    raw = _recognize_command(
        sources=[
            {
                "media_type": "image",
                "uri": "file://server/share/%E8%AF%BE%E7%A8%8B%20%F0%9F%93%9A/board.png",
            }
        ],
        options={"output_directory_uri": "file:///D:/Long%20Path/%E8%BE%93%E5%87%BA"},
    )
    command = parse_worker_command(raw)

    assert isinstance(command, ImageRecognitionRequest)
    assert command.sources[0].uri.startswith("file://server/share/")
    assert command.options["output_directory_uri"].startswith("file:///D:/")
