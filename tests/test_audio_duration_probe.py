import unittest
from unittest.mock import patch

from OCRLLM.processors.audio import _probe_duration


class AudioDurationProbeTests(unittest.TestCase):
    def test_probe_duration_uses_ffprobe_when_available(self):
        with patch("OCRLLM.processors.audio.run_subprocess_cancellable") as run_cmd:
            run_cmd.return_value.stdout = "123.45\n"
            run_cmd.return_value.stderr = ""

            duration = _probe_duration("sample.mp3", ffprobe_path="ffprobe")

        self.assertAlmostEqual(duration, 123.45)
        self.assertEqual(run_cmd.call_args.args[0][0], "ffprobe")

    def test_probe_duration_falls_back_to_ffmpeg_when_ffprobe_missing(self):
        with patch("OCRLLM.processors.audio.get_ffmpeg", return_value="ffmpeg"):
            with patch("OCRLLM.processors.audio.run_subprocess_cancellable") as run_cmd:
                run_cmd.return_value.stdout = ""
                run_cmd.return_value.stderr = "Duration: 00:03:07.50, start: 0.000000, bitrate: 32 kb/s"

                duration = _probe_duration("sample.mp3", ffprobe_path="")

        self.assertAlmostEqual(duration, 187.5)
        self.assertEqual(run_cmd.call_args.args[0][0], "ffmpeg")


if __name__ == "__main__":
    unittest.main()