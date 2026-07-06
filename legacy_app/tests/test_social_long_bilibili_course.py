from pathlib import Path

import pytest

from OCRLLM.cli import _normalize_part_indices
from OCRLLM.config import AppConfig
from OCRLLM.processors.social import bilibili_api
from OCRLLM.processors.social.downloader import (
    DownloadPart,
    DownloadResult,
    _download_bilibili,
)
from OCRLLM.processors.social.long_video import SocialLongVideoProcessor
from OCRLLM.processors.social import platform_router
from OCRLLM.processors.social.platform_router import VideoCategory, classify_video


def test_bilibili_download_captures_danmaku_per_part(monkeypatch, tmp_path):
    parts = [
        bilibili_api.BiliPartInfo(page=1, cid=101, part="intro", duration=10),
        bilibili_api.BiliPartInfo(page=2, cid=202, part="assignment", duration=20),
    ]
    playlist = bilibili_api.BiliPlaylistInfo(
        bvid="BVtest",
        aid=777,
        title="course",
        description="desc",
        duration=30,
        parts=parts,
    )

    monkeypatch.setattr(bilibili_api, "BiliSession", lambda **_kwargs: object())
    monkeypatch.setattr(bilibili_api, "extract_bvid", lambda _url: "BVtest")
    monkeypatch.setattr(bilibili_api, "get_video_info", lambda _session, _bvid: playlist)
    monkeypatch.setattr(
        bilibili_api,
        "fetch_danmaku",
        lambda _session, cid, **_kwargs: [f"dm-{cid}", "shared"],
    )
    monkeypatch.setattr(
        bilibili_api,
        "fetch_comments",
        lambda _session, _aid, max_pages=3: ["resource https://example.com/hw"],
    )

    def fake_download(_session, _bvid, part, output_dir, *, quality=80):
        path = Path(output_dir) / f"p{part.page}.mp4"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"video")
        return str(path)

    monkeypatch.setattr(bilibili_api, "download_video_part", fake_download)

    result = _download_bilibili("https://www.bilibili.com/video/BVtest", str(tmp_path), AppConfig())

    assert result.is_playlist
    assert [part.danmaku_texts for part in result.parts] == [
        ["dm-101", "shared"],
        ["dm-202", "shared"],
    ]
    assert result.danmaku_texts == ["dm-101", "shared", "dm-202"]
    assert result.comment_texts == ["resource https://example.com/hw"]


def test_fetch_danmaku_keeps_items_from_malformed_xml():
    class FakeSession:
        def get_raw(self, _url):
            return (
                b'<i><d p="9,1,25,16777215,0,0,hash,1">later</d>'
                b'<d p="1,1,25,16777215,0,0,hash,2">bad < raw &amp; useful</d>'
                b'<d p="5,1,25,16777215,0,0,hash,3">later</d></i>'
            )

    assert bilibili_api.fetch_danmaku(FakeSession(), 123) == [
        "bad < raw & useful",
        "later",
    ]


def test_fetch_danmaku_falls_back_to_segment_api_for_bilibili_412():
    segment_payload = (
        b"\n"
        + bytes([len(b"\x10\xe8\x07:\rsegmented one")])
        + b"\x10\xe8\x07:\rsegmented one"
    )

    class FakeSession:
        def get_raw(self, url, **_kwargs):
            if "list.so" in url:
                return b'<!DOCTYPE html><title>error 412</title><div class="error-container"></div>'
            if "segment_index=1" in url:
                return segment_payload
            return b""

    assert bilibili_api.fetch_danmaku(FakeSession(), 123, duration=360) == ["segmented one"]


def test_bilibili_download_fails_when_any_requested_part_fails(monkeypatch, tmp_path):
    parts = [
        bilibili_api.BiliPartInfo(page=1, cid=101, part="intro", duration=10),
        bilibili_api.BiliPartInfo(page=2, cid=202, part="assignment", duration=20),
    ]
    playlist = bilibili_api.BiliPlaylistInfo(
        bvid="BVtest",
        aid=777,
        title="course",
        description="desc",
        duration=30,
        parts=parts,
    )

    monkeypatch.setattr(bilibili_api, "BiliSession", lambda **_kwargs: object())
    monkeypatch.setattr(bilibili_api, "extract_bvid", lambda _url: "BVtest")
    monkeypatch.setattr(bilibili_api, "get_video_info", lambda _session, _bvid: playlist)
    monkeypatch.setattr(bilibili_api, "fetch_danmaku", lambda _session, _cid, **_kwargs: [])
    monkeypatch.setattr(bilibili_api, "fetch_comments", lambda _session, _aid, max_pages=3: [])

    def fake_download(_session, _bvid, part, output_dir, *, quality=80):
        if part.page == 2:
            raise RuntimeError("network stopped")
        path = Path(output_dir) / f"p{part.page}.mp4"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"video")
        return str(path)

    monkeypatch.setattr(bilibili_api, "download_video_part", fake_download)

    with pytest.raises(RuntimeError, match="P2 assignment"):
        _download_bilibili("https://www.bilibili.com/video/BVtest", str(tmp_path), AppConfig())


def test_social_long_preserves_board_and_audio_markdown(tmp_path):
    video_path = tmp_path / "lecture.mp4"
    video_path.write_bytes(b"video")
    dl = DownloadResult(
        title="course",
        platform="bilibili",
        video_path="",
        duration=10,
        parts=[
            DownloadPart(index=1, title="intro", video_path=str(video_path), duration=10),
        ],
        is_playlist=True,
    )
    proc = SocialLongVideoProcessor.__new__(SocialLongVideoProcessor)
    proc._check_cancelled = lambda: None
    proc._report = lambda *_args: None

    def fake_run(video_path_text, output_dir, *_args):
        stem = Path(video_path_text).stem
        board = Path(output_dir) / f"{stem}_板书识别.md"
        transcript = Path(output_dir) / f"{stem}_录音识别.md"
        board.write_text("# board\n", encoding="utf-8")
        transcript.write_text("# audio\n", encoding="utf-8")
        return {"board_md": str(board), "transcript_md": str(transcript)}

    proc._run_video_processor = fake_run

    out_dir = tmp_path / "out"
    proc._process_multi_parts(dl, str(out_dir), None, False, None, True)

    part_dir = out_dir / "P1_intro"
    assert (part_dir / "lecture_板书识别.md").read_text(encoding="utf-8") == "# board\n"
    assert (part_dir / "lecture_录音识别.md").read_text(encoding="utf-8") == "# audio\n"
    assert not (part_dir / "lecture_识别.md").exists()


def test_social_long_fails_when_audio_markdown_is_missing(tmp_path):
    video_path = tmp_path / "lecture.mp4"
    video_path.write_bytes(b"video")
    dl = DownloadResult(
        title="course",
        platform="bilibili",
        video_path="",
        duration=10,
        parts=[
            DownloadPart(index=1, title="intro", video_path=str(video_path), duration=10),
        ],
        is_playlist=True,
    )
    proc = SocialLongVideoProcessor.__new__(SocialLongVideoProcessor)
    proc._check_cancelled = lambda: None
    proc._report = lambda *_args: None

    def fake_run(video_path_text, output_dir, *_args):
        stem = Path(video_path_text).stem
        board = Path(output_dir) / f"{stem}_板书识别.md"
        board.write_text("# board\n", encoding="utf-8")
        return {"board_md": str(board), "transcript_md": str(Path(output_dir) / f"{stem}_录音识别.md")}

    proc._run_video_processor = fake_run

    with pytest.raises(RuntimeError, match="P1 intro"):
        proc._process_multi_parts(dl, str(tmp_path / "out"), None, False, None, True)


def test_social_long_caps_video_llm_concurrency_for_course_runs():
    cfg = AppConfig().with_updates(
        concurrency={
            "llm_parallel_requests": 15,
            "llm_request_stagger_seconds": 0.25,
        },
        social={
            "long_video_llm_parallel_requests": 4,
            "long_video_llm_request_stagger_seconds": 1.0,
        },
    )
    proc = SocialLongVideoProcessor.__new__(SocialLongVideoProcessor)
    proc.cfg = cfg

    video_cfg = proc._video_processor_config()

    assert video_cfg.concurrency.llm_parallel_requests == 4
    assert video_cfg.concurrency.llm_request_stagger_seconds == 1.0
    assert not video_cfg.video.extract_hotwords_with_text_model
    assert cfg.concurrency.llm_parallel_requests == 15
    assert cfg.video.extract_hotwords_with_text_model


def test_bilibili_parts_route_as_long_playlist(monkeypatch):
    monkeypatch.setattr(
        platform_router,
        "probe_video_info",
        lambda _url, _cfg: {
            "platform": "bilibili",
            "title": "short clips course",
            "duration": 30,
            "parts": [{"page": 1}, {"page": 2}],
            "total_parts": 2,
        },
    )

    route = classify_video("https://www.bilibili.com/video/BVtest", AppConfig())

    assert route.category == VideoCategory.LONG
    assert route.is_playlist
    assert route.part_count == 2


def test_cli_part_indices_support_ranges():
    assert _normalize_part_indices("1,3,5-7,3") == [1, 3, 5, 6, 7]
    assert _normalize_part_indices(None) is None
    with pytest.raises(ValueError):
        _normalize_part_indices("7-5")
