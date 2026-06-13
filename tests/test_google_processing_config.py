import unittest
from unittest.mock import patch

from OCRLLM.config import AppConfig
from OCRLLM.processors.pdf import PDFProcessor
from OCRLLM.processors.video import VideoProcessor


class GoogleProcessingConfigTests(unittest.TestCase):
    def test_from_env_loads_google_runtime_controls_for_cli(self):
        with patch.dict("os.environ", {
            "OCRLLM_GOOGLE_MODE_ENABLED": "1",
            "GOOGLE_API_KEY": "AIza-test",
            "OCRLLM_GOOGLE_PARALLEL_REQUESTS": "3",
            "OCRLLM_GOOGLE_REQUEST_STAGGER_SECONDS": "66.5",
            "OCRLLM_GOOGLE_VISION_BATCH_SIZE": "4",
            "OCRLLM_GOOGLE_VIDEO_FRAME_BATCH_SIZE": "5",
        }, clear=True):
            cfg = AppConfig.from_env()

        self.assertTrue(cfg.google_api.enabled)
        self.assertEqual(cfg.google_api.parallel_requests, 3)
        self.assertEqual(cfg.google_api.request_stagger_seconds, 66.5)
        self.assertEqual(cfg.google_api.vision_batch_size, 4)
        self.assertEqual(cfg.google_api.video_frame_batch_size, 5)

    def test_pdf_uses_google_independent_batch_parallel_and_stagger_config(self):
        cfg = AppConfig().with_updates(
            google_api={
                "enabled": True,
                "vision_batch_size": 23,
                "parallel_requests": 17,
                "request_stagger_seconds": 31.5,
            },
            processing={"batch_size": 3},
            concurrency={"llm_parallel_requests": 2, "llm_request_stagger_seconds": 0.1},
        )
        processor = PDFProcessor.__new__(PDFProcessor)
        processor.cfg = cfg

        self.assertEqual(processor._llm_batch_size(), 23)
        self.assertEqual(processor._llm_parallel_requests(), 17)
        self.assertEqual(processor._llm_request_stagger_seconds(), 31.5)

    def test_video_uses_google_independent_frame_batch_parallel_and_stagger_config(self):
        cfg = AppConfig().with_updates(
            google_api={
                "enabled": True,
                "video_frame_batch_size": 24,
                "parallel_requests": 18,
                "request_stagger_seconds": 32.5,
            },
            video={"batch_size": 4},
            concurrency={"llm_parallel_requests": 2, "llm_request_stagger_seconds": 0.1},
        )
        processor = VideoProcessor.__new__(VideoProcessor)
        processor.cfg = cfg

        self.assertEqual(processor._phase4_batch_size(), 24)
        self.assertEqual(processor._llm_parallel_requests(), 18)
        self.assertEqual(processor._llm_request_stagger_seconds(), 32.5)


if __name__ == "__main__":
    unittest.main()
