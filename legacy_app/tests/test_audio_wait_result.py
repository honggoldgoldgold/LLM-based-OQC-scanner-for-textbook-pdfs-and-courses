import logging
import tempfile
import unittest
from unittest.mock import Mock, patch

from OCRLLM.config import AppConfig
from OCRLLM.core.utils import setup_logging
from OCRLLM.core.llm_client import LLMClient
from OCRLLM.processors.audio import (
    ASRNoValidFragmentError,
    AudioProcessor,
    _TLS12HttpAdapter,
    build_fallback_audio_windows,
)


class AudioWaitResultTests(unittest.TestCase):
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

    def test_filetrans_input_summary_removes_remote_url_query(self):
        summary = AudioProcessor._filetrans_input_summary(
            "https://example.com/audio.mp3?token=secret#frag",
            duration=None,
        )

        self.assertEqual(summary, "url=https://example.com/audio.mp3, duration=unknown")

    def test_setup_logging_suppresses_requests_debug_noise(self):
        setup_logging(logging.DEBUG)

        self.assertGreaterEqual(logging.getLogger("urllib3").level, logging.WARNING)
        self.assertGreaterEqual(logging.getLogger("requests").level, logging.WARNING)


if __name__ == "__main__":
    unittest.main()
