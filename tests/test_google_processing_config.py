import unittest

from OCRLLM.config import AppConfig
from OCRLLM.processors.pdf import PDFProcessor
from OCRLLM.processors.video import VideoProcessor


class GoogleProcessingConfigTests(unittest.TestCase):
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
