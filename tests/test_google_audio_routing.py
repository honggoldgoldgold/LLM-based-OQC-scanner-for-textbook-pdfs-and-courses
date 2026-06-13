import os
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

from OCRLLM.config import AppConfig
from OCRLLM.core.providers.google_provider import GoogleProviderClient
from OCRLLM.processors.audio import AudioProcessor
from OCRLLM.processors.video import VideoProcessor


class GoogleAudioRoutingTests(unittest.TestCase):
    def test_google_mode_uses_long_audio_provider_even_for_short_local_audio(self):
        with tempfile.TemporaryDirectory() as tmp:
            audio_path = os.path.join(tmp, "short.mp3")
            with open(audio_path, "wb") as f:
                f.write(b"fake audio")
            output_path = os.path.join(tmp, "out.md")

            cfg = AppConfig().with_updates(
                paths={"output_dir": tmp, "temp_dir": tmp},
                google_api={
                    "enabled": True,
                    "api_key": "AIza-test",
                    "audio_model": "gemini-3.5-flash",
                },
            )
            llm = Mock()
            llm.transcribe_long_audio.return_value = "hello from google"
            processor = AudioProcessor(cfg=cfg, llm=llm)
            processor._ensure_upload_format = Mock(return_value=audio_path)
            processor._short_asr = Mock(side_effect=AssertionError("short fallback must not run"))

            result = processor.process(audio_path, output_path=output_path)

            self.assertEqual(result, output_path)
            llm.transcribe_long_audio.assert_called_once()
            with open(output_path, encoding="utf-8") as f:
                self.assertIn("hello from google", f.read())
            processor._short_asr.assert_not_called()

    def test_qwen_no_valid_fragment_no_longer_forces_short_audio_fallback(self):
        with tempfile.TemporaryDirectory() as tmp:
            audio_path = os.path.join(tmp, "lecture.mp3")
            with open(audio_path, "wb") as f:
                f.write(b"fake audio")
            output_path = os.path.join(tmp, "out.md")

            cfg = AppConfig().with_updates(
                paths={"output_dir": tmp, "temp_dir": tmp},
                api={"api_key": "sk-test"},
                models={"allow_asr_short_fallback": False},
            )
            processor = AudioProcessor.__new__(AudioProcessor)
            processor.cfg = cfg
            processor.reporter = Mock()
            processor.reporter.cancel_event = None
            processor._report = Mock()
            processor._report_content = Mock()
            processor._close_http_session = Mock()
            processor._ensure_upload_format = Mock(return_value=audio_path)
            processor._should_use_short_asr = Mock(return_value=(False, 600.0))
            processor._upload_file = Mock(return_value="https://example.com/audio.mp3")
            processor._submit_task = Mock(return_value="task-id")
            processor._wait_result = Mock(side_effect=RuntimeError("NO_VALID_FRAGMENT"))
            processor._short_asr = Mock(side_effect=AssertionError("short fallback must not run"))

            with self.assertRaises(RuntimeError) as ctx:
                processor.process(audio_path, output_path=output_path)

            self.assertIn("已禁止自动回退短音频", str(ctx.exception))
            processor._short_asr.assert_not_called()

    def test_video_phase5_uses_google_long_audio_route(self):
        with tempfile.TemporaryDirectory() as tmp:
            audio_path = os.path.join(tmp, "lecture.mp3")
            with open(audio_path, "wb") as f:
                f.write(b"fake audio")

            cfg = AppConfig().with_updates(
                paths={"output_dir": tmp, "temp_dir": tmp},
                google_api={
                    "enabled": True,
                    "api_key": "AIza-test",
                    "audio_model": "gemini-3.5-flash",
                },
            )
            llm = Mock()
            llm.transcribe_long_audio.return_value = "video audio through google"
            pool = Mock()
            pool.get_single_client.return_value = llm
            processor = VideoProcessor(cfg=cfg, llm=llm, api_pool=pool)

            processor._phase5_asr(audio_path, ["convex"], tmp, "lecture")

            llm.transcribe_long_audio.assert_called_once()
            output_path = os.path.join(tmp, "lecture_录音识别.md")
            with open(output_path, encoding="utf-8") as f:
                self.assertIn("video audio through google", f.read())

    def test_google_long_audio_upload_uses_ascii_safe_temp_path_for_chinese_filenames(self):
        with tempfile.TemporaryDirectory() as tmp:
            audio_path = Path(tmp) / "数据库及实现_录音.mp3"
            audio_path.write_bytes(b"fake audio")
            uploaded_paths: list[str] = []

            class FakeFiles:
                def upload(self, file):
                    uploaded_paths.append(str(file))
                    Path(file).read_bytes()
                    return SimpleNamespace(name="files/test", state="ACTIVE")

                def get(self, name):
                    return SimpleNamespace(name=name, state="ACTIVE")

            class FakeModels:
                def generate_content(self, **_kwargs):
                    return SimpleNamespace(text="ok transcript")

            cfg = AppConfig().with_updates(google_api={"enabled": True, "api_key": "AIza-test"})
            client = GoogleProviderClient(cfg=cfg)
            client._client = SimpleNamespace(files=FakeFiles(), models=FakeModels())

            text = client.transcribe_long_audio(str(audio_path), model="gemini-3.5-flash")

            self.assertEqual(text, "ok transcript")
            self.assertEqual(len(uploaded_paths), 1)
            uploaded_paths[0].encode("ascii")
            self.assertNotEqual(uploaded_paths[0], str(audio_path))


if __name__ == "__main__":
    unittest.main()
