import logging
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from OCRLLM.config import AppConfig
from OCRLLM.core.utils import setup_logging
from OCRLLM.core.llm_client import LLMClient, dashscope_local_file_uri
from OCRLLM.processors.audio import (
    ASRLowContentError,
    ASRNoValidFragmentError,
    AudioProcessor,
    _TLS12HttpAdapter,
    build_fallback_audio_windows,
)


class AudioWaitResultTests(unittest.TestCase):
    def tearDown(self):
        root = logging.getLogger()
        for handler in list(root.handlers):
            if getattr(handler, "_ocrllm_persistent_log", False):
                root.removeHandler(handler)
                handler.close()

    def test_tls_adapter_forces_minimum_tls12(self):
        context = _TLS12HttpAdapter._build_context()

        self.assertEqual(context.minimum_version.name, "TLSv1_2")

    def test_wait_result_raises_on_unknown_status(self):
        processor = AudioProcessor.__new__(AudioProcessor)
        processor._check_cancelled = lambda: None
        processor._sleep = lambda _: None
        processor._report = lambda current, total, msg: None
        processor._poll_headers = lambda: {}
        processor._http_session = Mock()
        processor.cfg = AppConfig()

        response = Mock(status_code=200)
        response.json.return_value = {"output": {"task_status": "UNKNOWN"}}
        processor._http_session.get.return_value = response

        with self.assertRaises(RuntimeError) as ctx:
            processor._wait_result("task-id", poll_interval=1.0, max_wait=5.0)

        self.assertIn("UNKNOWN", str(ctx.exception))

    def test_wait_result_rejects_succeeded_task_with_failed_subtask(self):
        processor = AudioProcessor.__new__(AudioProcessor)
        processor._check_cancelled = lambda: None
        processor._sleep = lambda _: None
        processor._report = lambda current, total, msg: None
        processor._poll_headers = lambda: {}
        processor._http_session = Mock()
        processor.cfg = AppConfig()

        response = Mock(status_code=200)
        response.json.return_value = {
            "output": {
                "task_status": "SUCCEEDED",
                "results": [{
                    "file_url": "https://example.com/bad.mp3",
                    "subtask_status": "FAILED",
                    "code": "InvalidFile.DownloadFailed",
                    "message": "The audio file cannot be downloaded.",
                }],
                "task_metrics": {"TOTAL": 1, "SUCCEEDED": 0, "FAILED": 1},
            }
        }
        processor._http_session.get.return_value = response

        with self.assertRaises(RuntimeError) as ctx:
            processor._wait_result("task-id", poll_interval=1.0, max_wait=5.0)

        self.assertIn("InvalidFile.DownloadFailed", str(ctx.exception))

    def test_wait_result_classifies_failed_no_valid_fragment_as_filetrans_error(self):
        processor = AudioProcessor.__new__(AudioProcessor)
        processor._check_cancelled = lambda: None
        processor._sleep = lambda _: None
        processor._report = lambda current, total, msg: None
        processor._poll_headers = lambda: {}
        processor._http_session = Mock()
        processor.cfg = AppConfig()

        response = Mock(status_code=200)
        response.json.return_value = {
            "output": {
                "task_status": "FAILED",
                "code": "NO_VALID_FRAGMENT",
                "message": "No valid speech fragment.",
            }
        }
        processor._http_session.get.return_value = response

        with self.assertRaises(ASRNoValidFragmentError) as ctx:
            processor._wait_result("task-id", poll_interval=1.0, max_wait=5.0)

        self.assertIn("filetrans", str(ctx.exception))
        self.assertIn("NO_VALID_FRAGMENT", str(ctx.exception))

    def test_wait_result_classifies_success_with_no_valid_fragment_as_filetrans_error(self):
        processor = AudioProcessor.__new__(AudioProcessor)
        processor._check_cancelled = lambda: None
        processor._sleep = lambda _: None
        processor._report = lambda current, total, msg: None
        processor._poll_headers = lambda: {}
        processor._http_session = Mock()
        processor.cfg = AppConfig()

        response = Mock(status_code=200)
        response.json.return_value = {"output": {"task_status": "SUCCESS_WITH_NO_VALID_FRAGMENT"}}
        processor._http_session.get.return_value = response

        with self.assertRaises(ASRNoValidFragmentError) as ctx:
            processor._wait_result("task-id", poll_interval=1.0, max_wait=5.0)

        self.assertIn("filetrans", str(ctx.exception))
        self.assertIn("SUCCESS_WITH_NO_VALID_FRAGMENT", str(ctx.exception))

    def test_result_to_md_raises_when_no_transcripts(self):
        processor = AudioProcessor.__new__(AudioProcessor)
        processor._sleep = lambda _: None
        processor._http_session = Mock()
        processor.cfg = AppConfig()

        with self.assertRaises(RuntimeError) as ctx:
            processor._result_to_md({"output": {"task_status": "SUCCEEDED"}}, "lecture")

        self.assertIn("未返回任何转写结果", str(ctx.exception))

    def test_submit_task_uses_model_specific_file_input_shape(self):
        with tempfile.TemporaryDirectory() as tmp:
            processor = AudioProcessor.__new__(AudioProcessor)
            processor.cfg = AppConfig().with_updates(
                paths={"output_dir": tmp, "temp_dir": tmp},
                api={"api_key": "sk-test"},
                models={"asr_model": "qwen3-asr-flash-filetrans"},
            )
            processor._submit_headers = lambda: {}
            processor._sleep = lambda _: None
            processor._build_corpus = lambda hotwords: ""
            session = Mock()
            response = Mock(status_code=200)
            response.json.return_value = {"output": {"task_id": "task-qwen"}}
            session.post.return_value = response
            processor._get_http_session = lambda: session

            processor._submit_task("https://example.com/audio.mp3")

            payload = session.post.call_args.kwargs["json"]
            self.assertEqual(payload["input"], {"file_url": "https://example.com/audio.mp3"})

            processor.cfg = processor.cfg.with_updates(models={"asr_model": "paraformer-v2"})
            response.json.return_value = {"output": {"task_id": "task-paraformer"}}

            processor._submit_task("https://example.com/audio.mp3")

            payload = session.post.call_args.kwargs["json"]
            self.assertEqual(payload["input"], {"file_urls": ["https://example.com/audio.mp3"]})

    def test_fallback_windows_use_six_minutes_with_thirty_second_context(self):
        windows = build_fallback_audio_windows(
            duration=800.0,
            chunk_seconds=360,
            context_seconds=30,
        )

        self.assertEqual(
            [(w.actual_start, w.actual_end, w.logical_start, w.logical_end) for w in windows],
            [
                (0.0, 390.0, 0.0, 360.0),
                (330.0, 750.0, 360.0, 720.0),
                (690.0, 800.0, 720.0, 800.0),
            ],
        )

    def test_short_audio_falls_back_from_dashscope_sdk_to_openai_compatible(self):
        client = LLMClient.__new__(LLMClient)
        client.cfg = AppConfig()
        client._transcribe_short_audio_dashscope_sdk = Mock(side_effect=RuntimeError("sdk down"))
        client._transcribe_short_audio_openai_compatible = Mock(return_value="transcript")

        result = client.transcribe_short_audio("sample.mp3", model="qwen3-asr-flash")

        self.assertEqual(result, "transcript")
        client._transcribe_short_audio_dashscope_sdk.assert_called_once()
        client._transcribe_short_audio_openai_compatible.assert_called_once()

    def test_dashscope_local_file_uri_uses_windows_sdk_format(self):
        with patch("OCRLLM.core.llm_client.sys.platform", "win32"):
            with patch("OCRLLM.core.llm_client.Path.resolve", return_value=Path("D:/audio/test.mp3")):
                self.assertEqual(dashscope_local_file_uri("D:/audio/test.mp3"), "file://D:/audio/test.mp3")

    def test_filetrans_input_summary_removes_remote_url_query(self):
        summary = AudioProcessor._filetrans_input_summary(
            "https://example.com/audio.mp3?token=secret#frag",
            duration=None,
        )

        self.assertEqual(summary, "url=https://example.com/audio.mp3, duration=unknown")

    def test_filetrans_quality_gate_rejects_near_empty_long_result(self):
        markdown = "<!-- meta:audio title=lecture -->\n\n<!-- meta:segment index=1 time=06:32~06:32 -->\n\n是。\n"

        with self.assertRaises(ASRLowContentError) as ctx:
            AudioProcessor._raise_if_filetrans_text_too_short(markdown, duration=3140.0)

        self.assertIn("识别文本过短", str(ctx.exception))

    def test_filetrans_quality_gate_allows_short_audio(self):
        markdown = "<!-- meta:audio title=short -->\n\n<!-- meta:segment index=1 time=00:00~00:01 -->\n\n是。\n"

        AudioProcessor._raise_if_filetrans_text_too_short(markdown, duration=30.0)

    def test_setup_logging_suppresses_requests_debug_noise(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        setup_logging(logging.DEBUG, log_file=Path(tmp.name) / "ocrllm.log")

        self.assertGreaterEqual(logging.getLogger("urllib3").level, logging.WARNING)
        self.assertGreaterEqual(logging.getLogger("requests").level, logging.WARNING)

    def test_setup_logging_writes_persistent_log_file_once(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        log_path = Path(tmp.name) / "ocrllm.log"
        setup_logging(logging.INFO, log_file=log_path)
        logging.getLogger("ocrllm-test").info("persistent log smoke")

        for handler in logging.getLogger().handlers:
            handler.flush()

        self.assertTrue(log_path.exists())
        self.assertIn("persistent log smoke", log_path.read_text(encoding="utf-8"))

        setup_logging(logging.DEBUG, log_file=log_path)
        persistent_handlers = [
            handler for handler in logging.getLogger().handlers
            if getattr(handler, "_ocrllm_persistent_log", False)
        ]
        self.assertEqual(len(persistent_handlers), 1)


if __name__ == "__main__":
    unittest.main()
