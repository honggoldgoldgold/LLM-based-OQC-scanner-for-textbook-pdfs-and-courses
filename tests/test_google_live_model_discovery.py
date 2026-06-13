import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from OCRLLM.core import model_catalog


@unittest.skipUnless(
    os.environ.get("OCRLLM_RUN_LIVE_GOOGLE_TESTS") == "1"
    and (os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")),
    "set OCRLLM_RUN_LIVE_GOOGLE_TESTS=1 and GOOGLE_API_KEY/GEMINI_API_KEY to run live Google model discovery",
)
class GoogleLiveModelDiscoveryTests(unittest.TestCase):
    def test_live_google_model_discovery_returns_generate_content_candidates(self):
        api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY") or ""
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(Path, "home", return_value=Path(tmp)):
                summary = model_catalog.refresh_google_models(api_key, timeout=20.0)

                self.assertGreater(summary.raw_count, 0)
                self.assertTrue(summary.raw_model_ids)
                self.assertTrue(summary.vision)
                self.assertTrue(summary.audio)
                self.assertTrue((Path(tmp) / ".OCRLLM" / "google_models.json").exists())


if __name__ == "__main__":
    unittest.main()
