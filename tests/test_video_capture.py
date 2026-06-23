import unittest
from unittest.mock import patch

from OCRLLM.core.video_capture import open_video_capture


class _FakeCapture:
    def __init__(self, backend, opened):
        self.backend = backend
        self._opened = opened
        self.released = False

    def isOpened(self):
        return self._opened

    def release(self):
        self.released = True


class _FakeCv2:
    CAP_ANY = 0
    CAP_FFMPEG = 1900
    CAP_MSMF = 1400
    CAP_DSHOW = 700

    def __init__(self, opened_backends):
        self.opened_backends = set(opened_backends)
        self.calls = []

    def VideoCapture(self, path, backend=None):
        self.calls.append((path, backend))
        return _FakeCapture(backend, backend in self.opened_backends)


class VideoCaptureTests(unittest.TestCase):
    def test_windows_file_capture_prefers_ffmpeg_before_msmf(self):
        fake_cv2 = _FakeCv2(opened_backends={_FakeCv2.CAP_FFMPEG})

        with patch("OCRLLM.core.video_capture.os.name", "nt"), \
                patch("OCRLLM.core.video_capture.cv2", fake_cv2), \
                patch.dict("OCRLLM.core.video_capture.os.environ", {}, clear=True):
            cap = open_video_capture("G:/lecture.mp4")

        self.assertTrue(cap.isOpened())
        self.assertEqual(fake_cv2.calls[0], ("G:/lecture.mp4", _FakeCv2.CAP_FFMPEG))

    def test_non_windows_capture_keeps_any_first_for_linux(self):
        fake_cv2 = _FakeCv2(opened_backends={_FakeCv2.CAP_ANY})

        with patch("OCRLLM.core.video_capture.os.name", "posix"), \
                patch("OCRLLM.core.video_capture.cv2", fake_cv2), \
                patch.dict("OCRLLM.core.video_capture.os.environ", {}, clear=True):
            cap = open_video_capture("/mnt/lecture.mp4")

        self.assertTrue(cap.isOpened())
        self.assertEqual(fake_cv2.calls[0], ("/mnt/lecture.mp4", _FakeCv2.CAP_ANY))


if __name__ == "__main__":
    unittest.main()
