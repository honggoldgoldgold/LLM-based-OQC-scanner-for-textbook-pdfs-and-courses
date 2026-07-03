import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from OCRLLM.core import model_catalog


class BailianModelDiscoveryTests(unittest.TestCase):
    def test_refresh_bailian_models_fetches_classifies_and_caches_real_model_ids(self):
        fake_models = SimpleNamespace(data=[
            SimpleNamespace(id="qwen3-vl-plus"),
            SimpleNamespace(id="qwen-vl-ocr-latest"),
            SimpleNamespace(id="qwen3-asr-flash-filetrans-2025-11-17"),
            SimpleNamespace(id="qwen3-asr-flash-2026-02-10"),
            SimpleNamespace(id="paraformer-v2"),
            SimpleNamespace(id="qwen-plus"),
        ])

        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(Path, "home", return_value=Path(tmp)):
                with patch("OCRLLM.core.model_catalog.OpenAI") as openai_cls:
                    openai_cls.return_value.models.list.return_value = fake_models

                    summary = model_catalog.refresh_bailian_models(
                        "https://dashscope.aliyuncs.com/compatible-mode/v1",
                        "sk-test",
                    )

                self.assertEqual(summary.raw_count, 6)
                self.assertIn("qwen3-vl-plus", [m.name for m in summary.vision])
                self.assertIn("qwen-vl-ocr-latest", [m.name for m in summary.vision])
                self.assertIn("qwen3-asr-flash-filetrans-2025-11-17", [m.name for m in summary.audio])
                self.assertIn("qwen3-asr-flash-2026-02-10", [m.name for m in summary.audio])
                self.assertIn("paraformer-v2", [m.name for m in summary.audio])

                cached_names = [m.name for m in model_catalog.load_bailian_audio_models()]
                self.assertIn("qwen3-asr-flash-filetrans-2025-11-17", cached_names)
                self.assertTrue((Path(tmp) / ".OCRLLM" / "bailian_models.json").exists())


if __name__ == "__main__":
    unittest.main()
