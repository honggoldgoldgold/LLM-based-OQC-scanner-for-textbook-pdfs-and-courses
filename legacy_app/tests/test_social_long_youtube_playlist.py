import sys
import types
from pathlib import Path

import pytest

from OCRLLM.config import AppConfig
from OCRLLM.processors.social import downloader, platform_router
from OCRLLM.processors.social.downloader import _download_yt_dlp
from OCRLLM.processors.social.platform_router import VideoCategory, classify_video


def test_youtube_playlist_probe_routes_as_long_course(monkeypatch):
    monkeypatch.setattr(
        platform_router,
        "probe_video_info",
        lambda _url, _cfg: {
            "platform": "youtube",
            "title": "course playlist",
            "duration": 180,
            "parts": [{"page": 1}, {"page": 2}, {"page": 3}],
            "total_parts": 3,
        },
    )

    route = classify_video("https://youtube.com/playlist?list=PLcourse", AppConfig())

    assert route.platform == "youtube"
    assert route.category == VideoCategory.LONG
    assert route.is_playlist
    assert route.part_count == 3


def test_youtube_probe_reports_flat_playlist_entries(monkeypatch):
    captured_opts = []

    class FakeYoutubeDL:
        def __init__(self, opts):
            captured_opts.append(opts)

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

        def extract_info(self, _url, download=False):
            assert not download
            return {
                "_type": "playlist",
                "title": "Modern Robotics",
                "playlist_count": 2,
                "entries": [
                    {"id": "a1", "title": "intro", "duration": 10, "url": "https://youtube.com/watch?v=a1"},
                    {"id": "b2", "title": "chapter", "duration": 20, "url": "https://youtube.com/watch?v=b2"},
                ],
            }

    monkeypatch.setitem(sys.modules, "yt_dlp", types.SimpleNamespace(YoutubeDL=FakeYoutubeDL))
    cfg = AppConfig()

    info = downloader.probe_video_info("https://youtube.com/playlist?list=PLcourse", cfg)

    assert captured_opts[0]["extract_flat"] == "in_playlist"
    assert info["platform"] == "youtube"
    assert info["total_parts"] == 2
    assert info["duration"] == 30
    assert [part["part"] for part in info["parts"]] == ["intro", "chapter"]


def test_youtube_playlist_download_returns_parts_and_uses_playlist_items(monkeypatch, tmp_path):
    captured_opts = []

    class FakeYoutubeDL:
        def __init__(self, opts):
            captured_opts.append(opts)

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

        def extract_info(self, _url, download=True):
            assert download
            first = tmp_path / "001_intro_a1.mp4"
            second = tmp_path / "003_chapter_b2.mp4"
            first.write_bytes(b"video")
            second.write_bytes(b"video")
            return {
                "_type": "playlist",
                "title": "course",
                "entries": [
                    {
                        "id": "a1",
                        "title": "intro",
                        "duration": 10,
                        "playlist_index": 1,
                        "requested_downloads": [{"filepath": str(first)}],
                    },
                    {
                        "id": "b2",
                        "title": "chapter",
                        "duration": 20,
                        "playlist_index": 3,
                        "requested_downloads": [{"filepath": str(second)}],
                    },
                ],
            }

    monkeypatch.setitem(sys.modules, "yt_dlp", types.SimpleNamespace(YoutubeDL=FakeYoutubeDL))

    result = _download_yt_dlp(
        "https://youtube.com/playlist?list=PLcourse",
        str(tmp_path),
        AppConfig(),
        part_indices=[1, 3],
    )

    assert captured_opts[0]["noplaylist"] is False
    assert captured_opts[0]["playlist_items"] == "1,3"
    assert result.is_playlist
    assert result.video_path == ""
    assert [(part.index, part.title, Path(part.video_path).name) for part in result.parts] == [
        (1, "intro", "001_intro_a1.mp4"),
        (3, "chapter", "003_chapter_b2.mp4"),
    ]


def test_youtube_playlist_download_fails_when_an_entry_has_no_file(monkeypatch, tmp_path):
    class FakeYoutubeDL:
        def __init__(self, _opts):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

        def extract_info(self, _url, download=True):
            assert download
            return {
                "_type": "playlist",
                "title": "course",
                "entries": [
                    {"id": "a1", "title": "intro", "playlist_index": 1},
                ],
            }

    monkeypatch.setitem(sys.modules, "yt_dlp", types.SimpleNamespace(YoutubeDL=FakeYoutubeDL))

    with pytest.raises(RuntimeError, match="P1 intro"):
        _download_yt_dlp("https://youtube.com/playlist?list=PLcourse", str(tmp_path), AppConfig())
