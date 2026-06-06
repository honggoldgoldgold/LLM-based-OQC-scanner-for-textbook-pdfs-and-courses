import os
import tempfile
import unittest

import fitz
from PIL import Image

from OCRLLM.config import APIConfig, AppConfig
from OCRLLM.core.checkpoint import Checkpoint
from OCRLLM.core.progress_tracker import ProgressTracker
from OCRLLM.core.response_validator import validate_ocr_response
from OCRLLM.core.task_runner import ProgressReporter
from OCRLLM.processors.board import BoardProcessor
from OCRLLM.processors.pdf import PDFProcessor
from OCRLLM.processors.video import VideoProcessor


API_ERROR_JSON = '{"error": {"message": "用户额度不足", "code": "insufficient_user_quota"}}'


class _SingleClientPool:
    pool_size = 1

    def set_cancel_event(self, *_args):
        pass

    def get_single_client(self):
        return _JsonErrorLLM()


class _JsonErrorLLM:
    def set_cancel_event(self, *_args):
        pass

    def chat_with_images(self, *_args, **_kwargs):
        return API_ERROR_JSON

    def chat_with_images_contextual(self, *_args, **_kwargs):
        return API_ERROR_JSON

    def chat_text(self, *_args, **_kwargs):
        return ""


class _PromptAwarePDFLLM(_JsonErrorLLM):
    def chat_with_images(self, prompt, *_args, **_kwargs):
        if "1-1" in prompt:
            return "<!-- meta:page number=1 -->\n\n# Page 1\n\n真实内容足够长，可以作为有效识别结果。"
        return API_ERROR_JSON


class _PromptAwarePool(_SingleClientPool):
    def __init__(self, llm):
        self._llm = llm

    def get_single_client(self):
        return self._llm


class _MixedVideoLLM(_JsonErrorLLM):
    def __init__(self):
        self.calls = 0

    def chat_with_images(self, *_args, **_kwargs):
        self.calls += 1
        if self.calls == 1:
            return "<!-- meta:frame id=board_001_010s time=0:10 -->\n\n真实板书内容足够长。"
        return API_ERROR_JSON


class _SlotWriter:
    def __init__(self):
        self.slots = {}

    def write_slot(self, index, text):
        self.slots[index] = text


class _RecordingCheckpointManager:
    def __init__(self):
        self.saved_indices = []

    def save_incremental(self, checkpoint, index, result=""):
        checkpoint.mark_completed(index)
        self.saved_indices.append(index)


def _cfg(tmp: str) -> AppConfig:
    return AppConfig(api=APIConfig(api_key="dummy-key")).with_updates(
        paths={"output_dir": tmp, "temp_dir": tmp},
        concurrency={"llm_parallel_requests": 1, "llm_request_stagger_seconds": 0},
        processing={"batch_size": 1},
        video={"batch_size": 1},
    )


class ResponseValidatorTests(unittest.TestCase):
    def test_rejects_api_json_error_blob(self):
        ok, reason = validate_ocr_response(API_ERROR_JSON)

        self.assertFalse(ok)
        self.assertIn("insufficient_user_quota", reason)

    def test_rejects_html_error_page(self):
        ok, reason = validate_ocr_response("<!DOCTYPE html><html><body>403 Forbidden</body></html>")

        self.assertFalse(ok)
        self.assertIn("HTML", reason)

    def test_rejects_short_text_after_ignoring_comments(self):
        ok, reason = validate_ocr_response("<!-- provider note -->\nOK", min_chars=20)

        self.assertFalse(ok)
        self.assertIn("too short", reason)

    def test_allows_short_structural_empty_page_or_frame(self):
        for text in (
            "<!-- meta:page number=3 -->",
            "<!-- meta:frame id=board_001_010s time=0:10 -->",
        ):
            ok, reason = validate_ocr_response(text, min_chars=20)
            self.assertTrue(ok, reason)

    def test_config_exposes_response_validation_section(self):
        cfg = AppConfig()

        self.assertTrue(cfg.response_validation.enabled)
        self.assertEqual(cfg.response_validation.min_chars, 20)
        self.assertFalse(
            cfg.with_updates(response_validation={"enabled": False}).response_validation.enabled
        )


class ProcessorResponseValidationTests(unittest.TestCase):
    def test_board_rejects_json_error_response_instead_of_writing_it_as_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            image_path = os.path.join(tmp, "board.png")
            output_path = os.path.join(tmp, "board.md")
            Image.new("RGB", (8, 8), "white").save(image_path)
            proc = BoardProcessor(cfg=_cfg(tmp), llm=_JsonErrorLLM(), api_pool=_SingleClientPool())

            with self.assertRaisesRegex(RuntimeError, "全部.*失败"):
                proc.process([image_path], output_path=output_path, skip_preprocess=True)

            with open(output_path, encoding="utf-8") as f:
                content = f.read()
            self.assertIn("识别失败", content)
            self.assertNotIn('"error"', content)

    def test_pdf_rejected_response_does_not_mark_batch_checkpoint_complete(self):
        with tempfile.TemporaryDirectory() as tmp:
            proc = PDFProcessor(cfg=_cfg(tmp), llm=_JsonErrorLLM(), api_pool=_SingleClientPool())
            proc.checkpoint_mgr = _RecordingCheckpointManager()
            checkpoint = Checkpoint("pdf", "book.pdf", os.path.join(tmp, "book.md"), 1)
            writer = _SlotWriter()

            _, _, result, success = proc._process_llm_batch_tracked(
                0,
                ["page1.png"],
                0,
                "pages {page_range}",
                writer,
                checkpoint,
            )

            self.assertFalse(success)
            self.assertEqual(proc.checkpoint_mgr.saved_indices, [])
            self.assertEqual(checkpoint.completed_indices, set())
            self.assertIn("识别失败", result)
            self.assertNotIn('"error"', writer.slots[0])

    def test_pdf_partial_validation_failure_keeps_checkpoint_for_resume(self):
        with tempfile.TemporaryDirectory() as tmp:
            pdf_path = os.path.join(tmp, "book.pdf")
            output_path = os.path.join(tmp, "book.md")
            doc = fitz.open()
            doc.new_page(width=64, height=64)
            doc.new_page(width=64, height=64)
            doc.save(pdf_path)
            doc.close()

            llm = _PromptAwarePDFLLM()
            proc = PDFProcessor(cfg=_cfg(tmp), llm=llm, api_pool=_PromptAwarePool(llm))

            with self.assertRaisesRegex(RuntimeError, "部分.*失败"):
                proc.process(pdf_path, need_formula=True, output_path=output_path)

            checkpoint = proc.checkpoint_mgr.load("pdf", pdf_path)
            self.assertIsNotNone(checkpoint)
            self.assertEqual(checkpoint.completed_indices, {0})
            with open(output_path, encoding="utf-8") as f:
                content = f.read()
            self.assertIn("识别失败", content)
            self.assertNotIn('"error"', content)

    def test_video_rejected_batch_writes_placeholder_and_reports_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            proc = VideoProcessor(
                cfg=_cfg(tmp),
                llm=_JsonErrorLLM(),
                reporter=ProgressReporter(),
                tracker=ProgressTracker(),
                api_pool=_SingleClientPool(),
            )
            writer = _SlotWriter()
            frame = {"path": os.path.join(tmp, "board_001_010s.jpg"), "timestamp": 10.0, "frame_idx": 1}

            _, result_text, _, success = proc._phase4_batch_one(
                0,
                [(frame, frame["path"])],
                1,
                "{image_names} {extra_instruction}",
                writer,
            )

            self.assertFalse(success)
            self.assertIn("批次 1 失败", result_text)
            self.assertNotIn('"error"', writer.slots[0])

    def test_video_partial_validation_failure_stops_phase4_before_checkpoint_can_complete(self):
        with tempfile.TemporaryDirectory() as tmp:
            frame1 = os.path.join(tmp, "board_001_010s.jpg")
            frame2 = os.path.join(tmp, "board_002_020s.jpg")
            Image.new("RGB", (8, 8), "white").save(frame1)
            Image.new("RGB", (8, 8), "white").save(frame2)
            llm = _MixedVideoLLM()
            proc = VideoProcessor(
                cfg=_cfg(tmp),
                llm=llm,
                reporter=ProgressReporter(),
                tracker=ProgressTracker(),
                api_pool=_PromptAwarePool(llm),
            )

            with self.assertRaisesRegex(RuntimeError, "部分.*失败"):
                proc._phase4_llm(
                    [
                        {"path": frame1, "timestamp": 10.0, "frame_idx": 1},
                        {"path": frame2, "timestamp": 20.0, "frame_idx": 2},
                    ],
                    [frame1, frame2],
                    tmp,
                    "lecture",
                )

            with open(os.path.join(tmp, "lecture_板书识别.md"), encoding="utf-8") as f:
                content = f.read()
            self.assertIn("真实板书内容", content)
            self.assertIn("批次 2 失败", content)
            self.assertNotIn('"error"', content)


if __name__ == "__main__":
    unittest.main()
