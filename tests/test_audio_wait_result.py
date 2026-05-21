import logging
import unittest
from unittest.mock import Mock, patch

from OCRLLM.core.utils import setup_logging
from OCRLLM.processors.audio import AudioProcessor, _TLS12HttpAdapter


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

        response = Mock(status_code=200)
        response.json.return_value = {"output": {"task_status": "UNKNOWN"}}
        processor._http_session.get.return_value = response

        with self.assertRaises(RuntimeError) as ctx:
            processor._wait_result("task-id", poll_interval=1.0, max_wait=5.0)

        self.assertIn("UNKNOWN", str(ctx.exception))

    def test_result_to_md_raises_when_no_transcripts(self):
        processor = AudioProcessor.__new__(AudioProcessor)
        processor._sleep = lambda _: None
        processor._http_session = Mock()

        with self.assertRaises(RuntimeError) as ctx:
            processor._result_to_md({"output": {"task_status": "SUCCEEDED"}}, "lecture")

        self.assertIn("未返回任何转写结果", str(ctx.exception))

    def test_setup_logging_suppresses_requests_debug_noise(self):
        setup_logging(logging.DEBUG)

        self.assertGreaterEqual(logging.getLogger("urllib3").level, logging.WARNING)
        self.assertGreaterEqual(logging.getLogger("requests").level, logging.WARNING)


if __name__ == "__main__":
    unittest.main()