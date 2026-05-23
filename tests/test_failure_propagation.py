import os
import tempfile
import unittest

from PIL import Image

from OCRLLM.config import AppConfig, APIConfig
from OCRLLM.core.progress_tracker import ProgressTracker
from OCRLLM.core.task_runner import ProgressReporter
from OCRLLM.processors.board import BoardProcessor
from OCRLLM.processors.pdf import PDFProcessor
from OCRLLM.processors.video import VideoProcessor


class _FailingLLM:
    def set_cancel_event(self, *_args):
        pass

    def chat_with_images(self, *_args, **_kwargs):
        raise RuntimeError("provider rejected model")

    def chat_with_images_contextual(self, *_args, **_kwargs):
        raise RuntimeError("provider rejected model")

    def chat_text(self, *_args, **_kwargs):
        raise RuntimeError("provider rejected model")


class _SingleClientPool:
    pool_size = 1

    def set_cancel_event(self, *_args):
        pass

    def get_single_client(self):
        return _FailingLLM()


def _cfg(tmp: str) -> AppConfig:
    return AppConfig(
        api=APIConfig(api_key="dummy-key"),
    ).with_updates(
        paths={"output_dir": tmp, "temp_dir": tmp},
        concurrency={"llm_parallel_requests": 1, "llm_request_stagger_seconds": 0},
        processing={"batch_size": 1},
        video={"batch_size": 1},
    )


class VisionFailurePropagationTests(unittest.TestCase):
    def test_board_raises_when_every_batch_only_writes_error_placeholders(self):
        with tempfile.TemporaryDirectory() as tmp:
            image_path = os.path.join(tmp, "board.png")
            output_path = os.path.join(tmp, "board.md")
            Image.new("RGB", (8, 8), "white").save(image_path)
            proc = BoardProcessor(cfg=_cfg(tmp), llm=_FailingLLM(), api_pool=_SingleClientPool())

            with self.assertRaisesRegex(RuntimeError, "全部.*失败"):
                proc.process([image_path], output_path=output_path, skip_preprocess=True)

            with open(output_path, encoding="utf-8") as f:
                self.assertIn("识别失败", f.read())

    def test_pdf_raises_when_every_llm_batch_only_writes_error_placeholders(self):
        with tempfile.TemporaryDirectory() as tmp:
            pdf_path = os.path.join(tmp, "book.pdf")
            output_path = os.path.join(tmp, "book.md")
            import fitz

            doc = fitz.open()
            doc.new_page(width=64, height=64)
            doc.save(pdf_path)
            doc.close()

            proc = PDFProcessor(cfg=_cfg(tmp), llm=_FailingLLM(), api_pool=_SingleClientPool())

            with self.assertRaisesRegex(RuntimeError, "全部.*失败"):
                proc.process(pdf_path, need_formula=True, output_path=output_path)

            with open(output_path, encoding="utf-8") as f:
                self.assertIn("识别失败", f.read())

    def test_video_phase4_raises_when_every_batch_only_writes_error_placeholders(self):
        with tempfile.TemporaryDirectory() as tmp:
            frame_path = os.path.join(tmp, "board_001_010s.jpg")
            Image.new("RGB", (8, 8), "white").save(frame_path)
            proc = VideoProcessor(
                cfg=_cfg(tmp),
                llm=_FailingLLM(),
                reporter=ProgressReporter(),
                tracker=ProgressTracker(),
                api_pool=_SingleClientPool(),
            )

            with self.assertRaisesRegex(RuntimeError, "全部.*失败"):
                proc._phase4_llm(
                    [{"path": frame_path, "timestamp": 10.0, "frame_idx": 1}],
                    [frame_path],
                    tmp,
                    "lecture",
                )

            board_md = os.path.join(tmp, "lecture_板书识别.md")
            with open(board_md, encoding="utf-8") as f:
                self.assertIn("批次 1 失败", f.read())


if __name__ == "__main__":
    unittest.main()
