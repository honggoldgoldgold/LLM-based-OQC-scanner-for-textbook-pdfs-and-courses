import os
import sys
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

PROJECT_PARENT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_PARENT not in sys.path:
    sys.path.insert(0, PROJECT_PARENT)

from PIL import Image

from OCRLLM.config import AppConfig, APIConfig, VisionAPIConfig
from OCRLLM.core.llm_client import LLMClient


class VisionProviderConfigTests(unittest.TestCase):
    def test_from_env_keeps_dashscope_base_url_and_adds_optional_vision_provider(self):
        with patch.dict(os.environ, {
            "DASHSCOPE_API_KEY": "dash-key",
            "DASHSCOPE_BASE_URL": "https://dash.example/v1",
            "OCRLLM_VISION_API_KEY": "vision-key",
            "OCRLLM_VISION_BASE_URL": "https://vision.example/v1",
            "OCRLLM_VISION_WIRE_API": "responses",
            "OCRLLM_VISION_MODEL": "oasis-vision-model",
        }, clear=True):
            cfg = AppConfig.from_env()

        self.assertEqual(cfg.api.api_key, "dash-key")
        self.assertEqual(cfg.api.base_url, "https://dash.example/v1")
        self.assertTrue(cfg.vision_api.enabled)
        self.assertEqual(cfg.vision_api.api_key, "vision-key")
        self.assertEqual(cfg.vision_api.base_url, "https://vision.example/v1")
        self.assertEqual(cfg.vision_api.wire_api, "responses")
        self.assertEqual(cfg.models.vision_model, "oasis-vision-model")

    def test_responses_payload_carries_image_and_requested_provider_options(self):
        cfg = AppConfig(
            api=APIConfig(api_key="dash-key"),
            vision_api=VisionAPIConfig(
                enabled=True,
                api_key="vision-key",
                base_url="https://vision.example/v1",
                wire_api="responses",
                model_reasoning_effort="high",
                network_access=True,
                disable_response_storage=True,
            ),
        )
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            image_path = tmp.name
        try:
            Image.new("RGB", (8, 8), "white").save(image_path)
            client = LLMClient(cfg)
            payload = client._responses_payload("gpt-5.5", "scan", [image_path])
        finally:
            try:
                os.unlink(image_path)
            except OSError:
                pass

        self.assertEqual(payload["model"], "gpt-5.5")
        self.assertEqual(payload["reasoning"], {"effort": "high"})
        self.assertEqual(payload["tools"], [{"type": "web_search_preview"}])
        self.assertFalse(payload["store"])
        content = payload["input"][0]["content"]
        self.assertEqual(content[0], {"type": "input_text", "text": "scan"})
        self.assertEqual(content[1]["type"], "input_image")
        self.assertTrue(content[1]["image_url"].startswith("data:image/png;base64,"))

    def test_enabled_vision_provider_uses_responses_client_without_free_tier_chain(self):
        cfg = AppConfig(
            api=APIConfig(api_key="dash-key"),
            vision_api=VisionAPIConfig(
                enabled=True,
                api_key="vision-key",
                base_url="https://vision.example/v1",
                wire_api="responses",
            ),
        )
        client = LLMClient(cfg)
        client.vision_client.responses.create = MagicMock(return_value=SimpleNamespace(output_text="OCRLLM TEST 12345"))
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            image_path = tmp.name
        try:
            Image.new("RGB", (8, 8), "white").save(image_path)
            result = client.chat_with_images("read", [image_path], model="gpt-5.5", max_retries=1)
        finally:
            try:
                os.unlink(image_path)
            except OSError:
                pass

        self.assertEqual(result, "OCRLLM TEST 12345")
        client.vision_client.responses.create.assert_called_once()

    def test_enabled_external_vision_provider_chat_omits_dashscope_extra_body(self):
        cfg = AppConfig(
            api=APIConfig(api_key="dash-key"),
            vision_api=VisionAPIConfig(
                enabled=True,
                api_key="vision-key",
                base_url="https://vision.example/v1",
                wire_api="chat",
            ),
        )
        client = LLMClient(cfg)
        client.vision_client.chat.completions.create = MagicMock(return_value=["OCRLLM TEST 12345"])
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            image_path = tmp.name
        try:
            Image.new("RGB", (8, 8), "white").save(image_path)
            result = client.chat_with_images("read", [image_path], model="gpt-vision", max_retries=1)
        finally:
            try:
                os.unlink(image_path)
            except OSError:
                pass

        self.assertEqual(result, "OCRLLM TEST 12345")
        kwargs = client.vision_client.chat.completions.create.call_args.kwargs
        self.assertNotIn("extra_body", kwargs)

    def test_vision_provider_can_initialize_without_dashscope_key(self):
        cfg = AppConfig(
            api=APIConfig(api_key=""),
            vision_api=VisionAPIConfig(
                enabled=True,
                api_key="vision-key",
                base_url="https://vision.example/v1",
                wire_api="chat",
            ),
        )
        client = LLMClient(cfg)
        client.vision_client.chat.completions.create = MagicMock(return_value=["OCRLLM TEST 12345"])
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            image_path = tmp.name
        try:
            Image.new("RGB", (8, 8), "white").save(image_path)
            result = client.chat_with_images("read", [image_path], model="gpt-vision", max_retries=1)
        finally:
            try:
                os.unlink(image_path)
            except OSError:
                pass

        self.assertEqual(result, "OCRLLM TEST 12345")

    def test_responses_parser_accepts_dict_shape(self):
        response = {
            "output": [{
                "content": [
                    {"text": "OCRLLM"},
                    {"text": " TEST"},
                ],
            }],
        }

        self.assertEqual(LLMClient._extract_responses_text(response), "OCRLLM TEST")

    def test_openai_compatible_stream_parser_accepts_text_and_dict_chunks(self):
        chunks = [
            "OCR",
            {"choices": [{"delta": {"content": "LLM"}}]},
            SimpleNamespace(choices=[SimpleNamespace(delta=SimpleNamespace(content=" TEST"))]),
        ]

        self.assertEqual(LLMClient._collect_stream(chunks), "OCRLLM TEST")

    def test_openai_compatible_message_parser_accepts_string_and_dict_responses(self):
        self.assertEqual(LLMClient._extract_message_text(" OCRLLM TEST "), "OCRLLM TEST")

        completion = {
            "choices": [{
                "message": {
                    "content": [
                        {"text": "OCRLLM"},
                        {"text": " TEST"},
                    ],
                },
            }],
        }

        self.assertEqual(LLMClient._extract_message_text(completion), "OCRLLM TEST")


if __name__ == "__main__":
    unittest.main()
