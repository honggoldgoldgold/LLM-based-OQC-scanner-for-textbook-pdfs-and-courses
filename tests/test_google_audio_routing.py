import os
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

from OCRLLM.config import AppConfig
from OCRLLM.core.providers.google_provider import GoogleProviderClient
from OCRLLM.processors.audio import AudioChunk, AudioProcessor, AudioSignalStats, build_google_audio_windows
from OCRLLM.processors.video import VideoProcessor


class GoogleAudioRoutingTests(unittest.TestCase):
    def test_google_audio_windows_default_to_30_minutes_with_overlap_context(self):
        windows = build_google_audio_windows(duration=3700, chunk_seconds=1800, overlap_seconds=30)

        self.assertEqual(len(windows), 3)
        self.assertEqual((windows[0].logical_start, windows[0].logical_end), (0.0, 1800.0))
        self.assertEqual((windows[0].actual_start, windows[0].actual_end), (0.0, 1830.0))
        self.assertEqual((windows[1].logical_start, windows[1].logical_end), (1800.0, 3600.0))
        self.assertEqual((windows[1].actual_start, windows[1].actual_end), (1770.0, 3630.0))
        self.assertEqual((windows[2].logical_start, windows[2].logical_end), (3600.0, 3700.0))
        self.assertEqual((windows[2].actual_start, windows[2].actual_end), (3570.0, 3700.0))

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
            processor._get_cached_duration = Mock(return_value=None)
            processor._split_google_audio = Mock(return_value=[
                AudioChunk(audio_path, 0.0, 10.0, 0.0, 10.0),
            ])
            processor._short_asr = Mock(side_effect=AssertionError("short fallback must not run"))

            result = processor.process(audio_path, output_path=output_path)

            self.assertEqual(result, output_path)
            llm.transcribe_long_audio.assert_called_once()
            prompt = llm.transcribe_long_audio.call_args.kwargs["system_prompt"]
            self.assertIn("meta:segment", prompt)
            validator = llm.transcribe_long_audio.call_args.kwargs["text_validator"]
            self.assertIn("返回空内容", validator("```markdown\n\n```"))
            with open(output_path, encoding="utf-8") as f:
                md = f.read()
            self.assertIn("<!-- meta:segment index=1 time=00:00~00:10 -->", md)
            self.assertIn("hello from google", md)
            processor._short_asr.assert_not_called()

    def test_google_mode_writes_one_meta_segment_per_audio_chunk(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = os.path.join(tmp, "lecture.mp3")
            part1 = os.path.join(tmp, "part001.mp3")
            part2 = os.path.join(tmp, "part002.mp3")
            for path in (source, part1, part2):
                with open(path, "wb") as f:
                    f.write(b"fake audio")
            output_path = os.path.join(tmp, "out.md")

            cfg = AppConfig().with_updates(
                paths={"output_dir": tmp, "temp_dir": tmp},
                google_api={
                    "enabled": True,
                    "api_key": "AIza-test",
                    "audio_model": "gemini-2.5-pro",
                    "audio_chunk_seconds": 1800,
                    "audio_overlap_seconds": 30,
                },
            )
            llm = Mock()
            llm.transcribe_long_audio.side_effect = [
                "first transcript " + "老师继续讲解课程内容。" * 900,
                "second transcript " + "老师继续讲解课程内容。" * 900,
            ]
            processor = AudioProcessor(cfg=cfg, llm=llm)
            processor._get_cached_duration = Mock(return_value=3605.0)
            processor._split_google_audio = Mock(return_value=[
                AudioChunk(part1, 0.0, 1830.0, 0.0, 1800.0),
                AudioChunk(part2, 1770.0, 3605.0, 1800.0, 3605.0),
            ])

            processor.process(source, output_path=output_path)

            self.assertEqual(llm.transcribe_long_audio.call_count, 2)
            with open(output_path, encoding="utf-8") as f:
                md = f.read()
            self.assertIn("<!-- meta:segment index=1 time=00:00~30:00 -->", md)
            self.assertIn("<!-- meta:segment index=2 time=30:00~01:00:05 -->", md)
            self.assertIn("first transcript", md)
            self.assertIn("second transcript", md)

    def test_google_mode_removes_model_emitted_segment_markers_from_body(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = os.path.join(tmp, "lecture.mp3")
            with open(source, "wb") as f:
                f.write(b"fake audio")
            output_path = os.path.join(tmp, "out.md")

            cfg = AppConfig().with_updates(
                paths={"output_dir": tmp, "temp_dir": tmp},
                google_api={
                    "enabled": True,
                    "api_key": "AIza-test",
                    "audio_model": "gemini-2.5-pro",
                    "audio_chunk_seconds": 1800,
                    "audio_overlap_seconds": 30,
                },
            )
            llm = Mock()
            long_body = "老师继续讲解数据库事务隔离级别和调度等价。" * 1300
            llm.transcribe_long_audio.return_value = (
                long_body
                + "\n<!-- meta:segment index=1 time=00:00~30:00 -->\n"
                + "这行注释来自模型正文，程序需要剥掉。"
            )
            processor = AudioProcessor(cfg=cfg, llm=llm)
            processor._get_cached_duration = Mock(return_value=1800.0)
            processor._split_google_audio = Mock(return_value=[
                AudioChunk(source, 0.0, 1800.0, 0.0, 1800.0),
            ])

            processor.process(source, output_path=output_path)

            with open(output_path, encoding="utf-8") as f:
                md = f.read()
            self.assertEqual(md.count("meta:segment"), 1)
            self.assertIn("老师继续讲解数据库事务隔离级别", md)
            self.assertIn("这行注释来自模型正文", md)

    def test_google_mode_removes_inline_model_segment_markers_from_body(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = os.path.join(tmp, "lecture.mp3")
            with open(source, "wb") as f:
                f.write(b"fake audio")
            output_path = os.path.join(tmp, "out.md")

            cfg = AppConfig().with_updates(
                paths={"output_dir": tmp, "temp_dir": tmp},
                google_api={
                    "enabled": True,
                    "api_key": "AIza-test",
                    "audio_model": "gemini-2.5-pro",
                    "audio_chunk_seconds": 1800,
                    "audio_overlap_seconds": 30,
                },
            )
            llm = Mock()
            long_body = "老师继续讲解马尔可夫链状态分类和极限分布。" * 1300
            llm.transcribe_long_audio.return_value = (
                long_body
                + " <!-- meta:segment index=1 time=00:00~30:00 --> "
                + "后面这句仍然是正文。"
            )
            processor = AudioProcessor(cfg=cfg, llm=llm)
            processor._get_cached_duration = Mock(return_value=1800.0)
            processor._split_google_audio = Mock(return_value=[
                AudioChunk(source, 0.0, 1800.0, 0.0, 1800.0),
            ])

            processor.process(source, output_path=output_path)

            with open(output_path, encoding="utf-8") as f:
                md = f.read()
            self.assertEqual(md.count("meta:segment"), 1)
            self.assertIn("老师继续讲解马尔可夫链", md)
            self.assertIn("后面这句仍然是正文", md)

    def test_google_mode_rejects_hotword_only_long_audio_body(self):
        with tempfile.TemporaryDirectory() as tmp:
            audio_path = os.path.join(tmp, "lecture.mp3")
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
            llm.transcribe_long_audio.return_value = "根据您提供的板书内容，为您提取的专业术语热词表如下：共产主义"
            processor = AudioProcessor(cfg=cfg, llm=llm)
            processor._get_cached_duration = Mock(return_value=9_600.0)
            processor._split_google_audio = Mock(return_value=[
                AudioChunk(audio_path, 0.0, 9600.0, 0.0, 9600.0),
            ])

            with self.assertRaisesRegex(RuntimeError, "Google 长音频识别疑似假成功"):
                processor.process(audio_path, output_path=output_path)

            self.assertFalse(os.path.exists(output_path))

    def test_google_mode_rejects_too_short_long_audio_body(self):
        with tempfile.TemporaryDirectory() as tmp:
            audio_path = os.path.join(tmp, "lecture.mp3")
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
            llm.transcribe_long_audio.return_value = "老师开始讲课。"
            processor = AudioProcessor(cfg=cfg, llm=llm)
            processor._get_cached_duration = Mock(return_value=9_600.0)
            processor._split_google_audio = Mock(return_value=[
                AudioChunk(audio_path, 0.0, 9600.0, 0.0, 9600.0),
            ])

            with self.assertRaisesRegex(RuntimeError, "转写正文过短"):
                processor.process(audio_path, output_path=output_path)

    def test_google_mode_rejects_prompt_echo_long_audio_body(self):
        with tempfile.TemporaryDirectory() as tmp:
            audio_path = os.path.join(tmp, "lecture.mp3")
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
            llm.transcribe_long_audio.return_value = (
                "请把这段课程录音尽量逐字转写成中文文本。要求：只输出转写内容本身。"
                "嗯，后面才像课堂内容。"
            )
            processor = AudioProcessor(cfg=cfg, llm=llm)
            processor._get_cached_duration = Mock(return_value=None)
            processor._split_google_audio = Mock(return_value=[
                AudioChunk(audio_path, 0.0, 20.0, 0.0, 20.0),
            ])

            with self.assertRaisesRegex(RuntimeError, "提示词回显"):
                processor.process(audio_path, output_path=output_path)

    def test_google_mode_rejects_repetitive_noise_long_audio_body(self):
        with tempfile.TemporaryDirectory() as tmp:
            audio_path = os.path.join(tmp, "lecture.mp3")
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
            llm.transcribe_long_audio.return_value = "嗯，" + "你，" * 80 + "后面仍然是重复噪声。"
            processor = AudioProcessor(cfg=cfg, llm=llm)
            processor._get_cached_duration = Mock(return_value=None)
            processor._split_google_audio = Mock(return_value=[
                AudioChunk(audio_path, 0.0, 20.0, 0.0, 20.0),
            ])

            with self.assertRaisesRegex(RuntimeError, "重复噪声"):
                processor.process(audio_path, output_path=output_path)

    def test_google_mode_rejects_extremely_weak_long_audio_before_upload(self):
        with tempfile.TemporaryDirectory() as tmp:
            audio_path = os.path.join(tmp, "lecture.mp3")
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
            processor = AudioProcessor(cfg=cfg, llm=llm)
            processor._get_cached_duration = Mock(return_value=9_600.0)

            with patch(
                "OCRLLM.processors.audio.measure_audio_signal",
                return_value=AudioSignalStats(mean_volume_db=-71.1, max_volume_db=-60.0),
            ):
                with self.assertRaisesRegex(RuntimeError, "音轨整体响度过低"):
                    processor.process(audio_path, output_path=output_path)

            llm.transcribe_long_audio.assert_not_called()
            self.assertFalse(os.path.exists(output_path))

    def test_google_mode_allows_sparse_long_audio_when_peak_is_clear(self):
        with tempfile.TemporaryDirectory() as tmp:
            audio_path = os.path.join(tmp, "lecture.mp3")
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
            llm.transcribe_long_audio.return_value = "老师继续讲解马克思主义基本原理课程内容。" * 2000
            processor = AudioProcessor(cfg=cfg, llm=llm)
            processor._get_cached_duration = Mock(return_value=9_600.0)
            processor._split_google_audio = Mock(return_value=[
                AudioChunk(audio_path, 0.0, 9600.0, 0.0, 9600.0),
            ])

            with patch(
                "OCRLLM.processors.audio.measure_audio_signal",
                return_value=AudioSignalStats(mean_volume_db=-73.7, max_volume_db=-7.6),
            ):
                processor.process(audio_path, output_path=output_path)

            llm.transcribe_long_audio.assert_called_once()
            self.assertTrue(os.path.exists(output_path))

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

            with patch("OCRLLM.processors.audio.AudioProcessor._get_cached_duration", return_value=None), \
                 patch("OCRLLM.processors.audio.AudioProcessor._split_google_audio", return_value=[
                     AudioChunk(audio_path, 0.0, 20.0, 0.0, 20.0),
                 ]):
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
