import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

from OCRLLM.core import model_catalog


class GoogleModelDiscoveryTests(unittest.TestCase):
    def test_refresh_google_models_fetches_classifies_prioritizes_and_caches_real_models(self):
        fake_client = SimpleNamespace(
            models=SimpleNamespace(
                list=Mock(return_value=[
                    SimpleNamespace(
                        name="models/gemini-3.5-flash",
                        display_name="Gemini 3.5 Flash",
                        description="Multimodal flash model with audio and video understanding.",
                        supported_generation_methods=["generateContent"],
                        input_token_limit=1_000_000,
                    ),
                    SimpleNamespace(
                        name="models/gemini-2.5-flash-image-preview",
                        display_name="Gemini 2.5 Flash Image Preview",
                        description="Preview image model.",
                        supported_generation_methods=["generateContent"],
                        input_token_limit=128_000,
                    ),
                    SimpleNamespace(
                        name="models/gemini-2.0-pro-exp",
                        display_name="Gemini 2.0 Pro Experimental",
                        description="Experimental multimodal pro model.",
                        supported_generation_methods=["generateContent"],
                        input_token_limit=1_000_000,
                    ),
                    SimpleNamespace(
                        name="models/gemini-1.5-pro",
                        display_name="Gemini 1.5 Pro",
                        description="General Gemini model.",
                        supported_generation_methods=["generateContent"],
                        input_token_limit=1_000_000,
                    ),
                    SimpleNamespace(
                        name="models/text-embedding-004",
                        display_name="Text Embedding",
                        description="Embedding model.",
                        supported_generation_methods=["embedContent"],
                    ),
                ])
            )
        )

        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(Path, "home", return_value=Path(tmp)):
                summary = model_catalog.refresh_google_models(
                    "AIza-test",
                    client_factory=lambda api_key, timeout: fake_client,
                    timeout=7.0,
                )

                fake_client.models.list.assert_called_once()
                self.assertEqual(summary.raw_count, 5)
                self.assertEqual(
                    [m.name for m in summary.vision],
                    [
                        "gemini-2.5-flash-image-preview",
                        "gemini-2.0-pro-exp",
                        "gemini-3.5-flash",
                        "gemini-1.5-pro",
                    ],
                )
                self.assertEqual(
                    [m.name for m in summary.audio],
                    ["gemini-3.5-flash", "gemini-2.0-pro-exp"],
                )
                self.assertTrue((Path(tmp) / ".OCRLLM" / "google_models.json").exists())

                cached_audio = [m.name for m in model_catalog.load_google_audio_models()]
                self.assertEqual(cached_audio, ["gemini-3.5-flash", "gemini-2.0-pro-exp"])

    def test_google_sdk_client_receives_model_fetch_timeout(self):
        with patch("google.genai.Client") as client_cls:
            model_catalog._build_google_client("AIza-test", timeout=7.5)

        kwargs = client_cls.call_args.kwargs
        self.assertEqual(kwargs["api_key"], "AIza-test")
        self.assertEqual(kwargs["http_options"].timeout, 7500)

    def test_google_free_chains_keep_vision_and_audio_priorities_separate(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(Path, "home", return_value=Path(tmp)):
                model_catalog._save_google_models_raw({
                    "vision": [
                        {
                            "name": "gemini-2.5-flash-image-preview",
                            "label": "image preview",
                            "kind": "image_preview",
                            "free_quota": True,
                        },
                        {
                            "name": "gemini-3.5-flash",
                            "label": "audio capable",
                            "kind": "audio_long",
                            "free_quota": True,
                        },
                    ],
                    "audio": [
                        {
                            "name": "gemini-3.5-flash",
                            "label": "audio capable",
                            "kind": "audio_long",
                            "free_quota": True,
                        },
                    ],
                })

                self.assertEqual(
                    model_catalog.google_free_vision_chain(),
                    ["gemini-2.5-flash-image-preview", "gemini-3.5-flash"],
                )
                self.assertEqual(model_catalog.google_free_audio_chain(), ["gemini-3.5-flash"])


if __name__ == "__main__":
    unittest.main()
