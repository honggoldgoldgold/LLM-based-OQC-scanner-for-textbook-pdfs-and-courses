from __future__ import annotations

import base64
import importlib
import json
from pathlib import Path

import pytest
from PIL import Image

from ocrllm.errors import Cancelled, InvalidSource
from ocrllm.providers.dashscope.provider_settings import DashScopeSettings


request_module = importlib.import_module(
    "ocrllm.providers.dashscope.build_dashscope_image_request"
)


def test_builds_ordered_mime_correct_openai_chat_request(tmp_path):
    png = _write_image(tmp_path / "first.png", size=(11, 12), color=(255, 0, 0))
    jpeg = _write_image(tmp_path / "second.jpg", size=(13, 11), color=(0, 0, 255))
    settings = _settings(enable_thinking=True, high_resolution=False)

    request = request_module.build_dashscope_image_request(
        (png, jpeg),
        prompt="Recognize in order.",
        model="qwen-test-model",
        settings=settings,
    )

    kwargs = request.kwargs
    assert kwargs["model"] == "qwen-test-model"
    assert kwargs["temperature"] == 0
    assert kwargs["max_completion_tokens"] == 16_384
    assert kwargs["extra_body"] == {
        "enable_thinking": True,
        "vl_high_resolution_images": False,
    }

    messages = kwargs["messages"]
    assert len(messages) == 1
    assert messages[0]["role"] == "user"
    content = messages[0]["content"]
    assert [item["type"] for item in content] == ["image_url", "image_url", "text"]

    first_url = content[0]["image_url"]["url"]
    second_url = content[1]["image_url"]["url"]
    assert first_url.startswith("data:image/png;base64,")
    assert second_url.startswith("data:image/jpeg;base64,")
    assert base64.b64decode(first_url.split(",", 1)[1]) == png.read_bytes()
    assert base64.b64decode(second_url.split(",", 1)[1]) == jpeg.read_bytes()
    assert content[2] == {"type": "text", "text": "Recognize in order."}
    assert request.serialized_byte_count == _wire_byte_count(kwargs)


def test_request_kwargs_returns_fresh_nested_containers(tmp_path):
    source = _write_image(tmp_path / "source.png")
    request = _build_request((source,))

    mutated = request.kwargs
    mutated["messages"][0]["content"][0]["image_url"]["url"] = "mutated"
    mutated["extra_body"]["enable_thinking"] = True

    fresh = request.kwargs
    assert fresh["messages"][0]["content"][0]["image_url"]["url"] != "mutated"
    assert fresh["extra_body"]["enable_thinking"] is False


def test_real_openai_sdk_serializes_the_measured_wire_body_exactly(
    tmp_path,
    monkeypatch,
):
    import httpx
    from openai import OpenAI

    source = _write_image(tmp_path / "sdk-wire.png")
    prompt = "Formula \u516c\u5f0f: x_1 \u2264 3"
    built = _build_request((source,), prompt=prompt)
    captured_bodies: list[bytes] = []

    def respond(request):
        captured_bodies.append(bytes(request.content))
        return httpx.Response(
            200,
            headers={"x-request-id": "req-sdk-wire"},
            json={
                "id": "chatcmpl-sdk-wire",
                "object": "chat.completion",
                "created": 1,
                "model": "qwen3.7-plus-2026-05-26",
                "choices": [
                    {
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": "# Recognized\n",
                            "refusal": None,
                        },
                        "finish_reason": "stop",
                        "logprobs": None,
                    }
                ],
                "usage": {
                    "prompt_tokens": 1,
                    "completion_tokens": 1,
                    "total_tokens": 2,
                },
            },
        )

    http_client = httpx.Client(transport=httpx.MockTransport(respond))
    client = OpenAI(
        api_key="test-only",
        base_url="https://example.test/v1",
        http_client=http_client,
        max_retries=0,
    )
    try:
        raw = client.chat.completions.with_raw_response.create(**built.kwargs)
        parsed = raw.parse()
    finally:
        client.close()

    assert parsed.choices[0].message.content == "# Recognized\n"
    assert len(captured_bodies) == 1
    assert len(captured_bodies[0]) == built.serialized_byte_count
    assert json.loads(captured_bodies[0])["messages"][0]["content"][-1] == {
        "type": "text",
        "text": prompt,
    }

    monkeypatch.setattr(
        request_module,
        "MAX_SERIALIZED_REQUEST_UTF8_BYTES",
        len(captured_bodies[0]),
    )
    assert _build_request((source,), prompt=prompt).serialized_byte_count == len(
        captured_bodies[0]
    )
    monkeypatch.setattr(
        request_module,
        "MAX_SERIALIZED_REQUEST_UTF8_BYTES",
        len(captured_bodies[0]) - 1,
    )
    with pytest.raises(InvalidSource) as raised:
        _build_request((source,), prompt=prompt)
    assert raised.value.code == "SOURCE_TOO_LARGE"


@pytest.mark.parametrize(
    ("cap_delta", "accepted"),
    [(1, True), (0, True), (-1, False)],
    ids=["one-below", "at", "one-above"],
)
def test_complete_data_url_byte_boundary(tmp_path, monkeypatch, cap_delta, accepted):
    source = _write_image(tmp_path / "boundary.png")
    actual_size = len(b"data:image/png;base64,") + len(
        base64.b64encode(source.read_bytes())
    )
    monkeypatch.setattr(
        request_module,
        "MAX_DATA_URL_UTF8_BYTES",
        actual_size + cap_delta,
    )

    if accepted:
        request = _build_request((source,))
        data_url = request.kwargs["messages"][0]["content"][0]["image_url"]["url"]
        assert len(data_url.encode("utf-8")) == actual_size
    else:
        with pytest.raises(InvalidSource) as raised:
            _build_request((source,))
        assert raised.value.code == "SOURCE_TOO_LARGE"


@pytest.mark.parametrize(
    ("size", "accepted"),
    [
        ((9, 11), False),
        ((10, 11), False),
        ((11, 11), True),
        ((11, 9), False),
        ((11, 10), False),
    ],
    ids=[
        "width-one-below",
        "width-at",
        "both-above",
        "height-one-below",
        "height-at",
    ],
)
def test_dimension_minimum_boundary(tmp_path, size, accepted):
    source = _write_image(tmp_path / f"{size[0]}x{size[1]}.png", size=size)

    if accepted:
        assert _build_request((source,)).serialized_byte_count > 0
    else:
        with pytest.raises(InvalidSource) as raised:
            _build_request((source,))
        assert raised.value.code == "SOURCE_INVALID"


@pytest.mark.parametrize(
    ("long_side", "accepted"),
    [(2_199, True), (2_200, True), (2_201, False)],
    ids=["one-below", "at", "one-above"],
)
def test_aspect_ratio_boundary(tmp_path, long_side, accepted):
    source = _write_image(tmp_path / f"ratio-{long_side}.png", size=(11, long_side))

    if accepted:
        assert _build_request((source,)).serialized_byte_count > 0
    else:
        with pytest.raises(InvalidSource) as raised:
            _build_request((source,))
        assert raised.value.code == "SOURCE_INVALID"


@pytest.mark.parametrize(
    ("long_side", "accepted"),
    [(7_679, True), (7_680, True), (7_681, False)],
    ids=["one-below", "at", "one-above"],
)
def test_long_side_boundary(tmp_path, long_side, accepted):
    source = _write_image(tmp_path / f"long-side-{long_side}.png", size=(39, long_side))

    if accepted:
        assert _build_request((source,)).serialized_byte_count > 0
    else:
        with pytest.raises(InvalidSource) as raised:
            _build_request((source,))
        assert raised.value.code == "SOURCE_TOO_LARGE"


@pytest.mark.parametrize(
    ("cap_delta", "accepted"),
    [(1, True), (0, True), (-1, False)],
    ids=["one-below", "at", "one-above"],
)
def test_high_resolution_pixel_boundary(tmp_path, monkeypatch, cap_delta, accepted):
    source = _write_image(tmp_path / "pixels.png", size=(11, 11))
    pixel_count = 121
    monkeypatch.setattr(
        request_module,
        "MAX_HIGH_RESOLUTION_PIXELS",
        pixel_count + cap_delta,
    )

    if accepted:
        assert _build_request((source,)).serialized_byte_count > 0
    else:
        with pytest.raises(InvalidSource) as raised:
            _build_request((source,))
        assert raised.value.code == "SOURCE_TOO_LARGE"


@pytest.mark.parametrize(
    ("cap_delta", "accepted"),
    [(1, True), (0, True), (-1, False)],
    ids=["one-below", "at", "one-above"],
)
def test_final_buffer_aggregate_pixel_boundary(
    tmp_path,
    monkeypatch,
    cap_delta,
    accepted,
):
    sources = (
        _write_image(tmp_path / "aggregate-first.png", size=(11, 11)),
        _write_image(tmp_path / "aggregate-second.png", size=(11, 11)),
    )
    aggregate_pixels = 242
    monkeypatch.setattr(
        request_module,
        "MAX_AGGREGATE_PIXELS",
        aggregate_pixels + cap_delta,
    )

    if accepted:
        assert _build_request(sources).serialized_byte_count > 0
    else:
        with pytest.raises(InvalidSource) as raised:
            _build_request(sources)
        assert raised.value.code == "SOURCE_TOO_LARGE"
        assert raised.value.details["aggregate_pixel_count"] == aggregate_pixels


def test_pixel_ceiling_is_not_applied_when_high_resolution_is_disabled(
    tmp_path,
    monkeypatch,
):
    source = _write_image(tmp_path / "standard-resolution.png", size=(11, 11))
    monkeypatch.setattr(request_module, "MAX_HIGH_RESOLUTION_PIXELS", 120)

    request = _build_request((source,), settings=_settings(high_resolution=False))

    assert request.serialized_byte_count > 0


@pytest.mark.parametrize(
    ("cap_delta", "accepted"),
    [(1, True), (0, True), (-1, False)],
    ids=["one-below", "at", "one-above"],
)
def test_compact_wire_request_byte_boundary(tmp_path, monkeypatch, cap_delta, accepted):
    source = _write_image(tmp_path / "request-size.png")
    measured = _build_request((source,), prompt="数式を正確に").serialized_byte_count
    monkeypatch.setattr(
        request_module,
        "MAX_SERIALIZED_REQUEST_UTF8_BYTES",
        measured + cap_delta,
    )

    if accepted:
        request = _build_request((source,), prompt="数式を正確に")
        assert request.serialized_byte_count == measured
    else:
        with pytest.raises(InvalidSource) as raised:
            _build_request((source,), prompt="数式を正確に")
        assert raised.value.code == "SOURCE_TOO_LARGE"
        assert raised.value.details["serialized_byte_count"] == measured


def test_request_repr_and_preflight_failure_do_not_expose_source_content(
    tmp_path,
    monkeypatch,
):
    path_secret = "SOURCE_PATH_SECRET_7d9e"
    prompt_secret = "PROMPT_SECRET_f31a"
    model_secret = "MODEL_SENTINEL_2b0c"
    source = _write_image(tmp_path / f"{path_secret}.png")
    request = _build_request(
        (source,),
        prompt=prompt_secret,
        model=model_secret,
    )
    encoded_secret = request.kwargs["messages"][0]["content"][0]["image_url"]["url"]

    safe_repr = repr(request)
    assert path_secret not in safe_repr
    assert prompt_secret not in safe_repr
    assert model_secret not in safe_repr
    assert encoded_secret not in safe_repr

    monkeypatch.setattr(request_module, "MAX_SERIALIZED_REQUEST_UTF8_BYTES", 1)
    with pytest.raises(InvalidSource) as raised:
        _build_request(
            (source,),
            prompt=prompt_secret,
            model=model_secret,
        )

    public_error = f"{raised.value!s} {raised.value!r} {dict(raised.value.details)!r}"
    assert path_secret not in public_error
    assert prompt_secret not in public_error
    assert model_secret not in public_error
    assert encoded_secret not in public_error


def test_missing_snapshot_is_sanitized_as_source_not_found(tmp_path):
    secret = "MISSING_PATH_SECRET_1bc9"

    with pytest.raises(InvalidSource) as raised:
        _build_request((tmp_path / f"{secret}.png",))

    assert raised.value.code == "SOURCE_NOT_FOUND"
    assert secret not in str(raised.value)
    assert raised.value.__cause__ is None


def test_snapshot_read_failure_is_sanitized_as_source_unreadable(
    tmp_path,
    monkeypatch,
):
    source = _write_image(tmp_path / "unreadable.png")
    error_secret = "OPERATING_SYSTEM_SECRET_693a"
    original_open = Path.open
    def deny_snapshot_read(path, *args, **kwargs):
        if path == source:
            raise PermissionError(error_secret)
        return original_open(path, *args, **kwargs)

    monkeypatch.setattr(Path, "open", deny_snapshot_read)

    with pytest.raises(InvalidSource) as raised:
        _build_request((source,))

    assert raised.value.code == "SOURCE_UNREADABLE"
    assert error_secret not in str(raised.value)
    assert raised.value.__cause__ is None


def test_snapshot_size_change_is_rejected(tmp_path, monkeypatch):
    source = _write_image(tmp_path / "changed.png")
    monkeypatch.setattr(
        request_module,
        "_read_snapshot_bytes",
        lambda _source, *, maximum_source_bytes: b"changed",
    )

    with pytest.raises(InvalidSource) as raised:
        _build_request((source,))

    assert raised.value.code == "SOURCE_INVALID"


def test_path_change_during_decode_cannot_change_the_captured_request_bytes(
    tmp_path,
    monkeypatch,
):
    source = _write_image(tmp_path / "same-size-change.png")
    original_bytes = source.read_bytes()
    replacement = bytes([original_bytes[0] ^ 0xFF]) + original_bytes[1:]
    assert len(replacement) == len(original_bytes)

    original_decode = request_module.decode_image_bytes

    def replace_snapshot_during_decode(image_bytes, *, suffix):
        source.write_bytes(replacement)
        return original_decode(image_bytes, suffix=suffix)

    monkeypatch.setattr(
        request_module,
        "decode_image_bytes",
        replace_snapshot_during_decode,
    )

    request = _build_request((source,))
    data_url = request.kwargs["messages"][0]["content"][0]["image_url"]["url"]

    assert base64.b64decode(data_url.split(",", 1)[1]) == original_bytes
    assert source.read_bytes() == replacement


def test_cancellation_during_group_preflight_stops_before_next_image(
    tmp_path,
    monkeypatch,
):
    from threading import Event

    sources = (
        _write_image(tmp_path / "cancel-first.png"),
        _write_image(tmp_path / "cancel-second.png"),
    )
    cancellation = Event()
    original_build_data_url = request_module._build_data_url
    processed: list[Path] = []

    def build_first_then_cancel(source_path, **kwargs):
        processed.append(source_path)
        result = original_build_data_url(source_path, **kwargs)
        cancellation.set()
        return result

    monkeypatch.setattr(request_module, "_build_data_url", build_first_then_cancel)

    with pytest.raises(Cancelled) as captured:
        request_module.build_dashscope_image_request(
            sources,
            prompt="Recognize.",
            model="qwen3.7-plus-2026-05-26",
            settings=_settings(),
            cancellation=cancellation,
        )

    assert captured.value.code == "CANCELLED"
    assert processed == [sources[0]]


def _build_request(
    image_paths,
    *,
    prompt="Recognize the board.",
    model="qwen3.7-plus-2026-05-26",
    settings=None,
):
    return request_module.build_dashscope_image_request(
        image_paths,
        prompt=prompt,
        model=model,
        settings=_settings() if settings is None else settings,
    )


def _settings(*, enable_thinking=False, high_resolution=True):
    return DashScopeSettings(
        region="ap-southeast-1",
        base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
        enable_thinking=enable_thinking,
        vl_high_resolution_images=high_resolution,
    )


def _write_image(path: Path, *, size=(11, 11), color=(32, 96, 160)) -> Path:
    image_format = "PNG" if path.suffix.casefold() == ".png" else "JPEG"
    Image.new("RGB", size, color=color).save(path, format=image_format)
    return path


def _wire_byte_count(kwargs) -> int:
    wire_body = dict(kwargs)
    extra_body = wire_body.pop("extra_body")
    wire_body.update(extra_body)
    return len(
        json.dumps(
            wire_body,
            ensure_ascii=False,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    )
