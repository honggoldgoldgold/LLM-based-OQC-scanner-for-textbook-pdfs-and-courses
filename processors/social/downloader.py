"""
统一社交媒体视频下载引擎。

平台策略：
  - B站（bilibili.com / b23.tv）→ 原生 API（bilibili_api.py），绕过 yt-dlp 412 问题
  - YouTube / 抖音 / 小红书 / X / TikTok → yt-dlp

设计原则：核心流程借鉴 yt-dlp/bilibili-api 思路并做本土化，不直接依赖不稳定的外部项目。
"""

from __future__ import annotations

import logging
import os
import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from OCRLLM.config import AppConfig

logger = logging.getLogger(__name__)


def _available_browser_cookie_sources() -> list[str]:
    """返回当前机器上可能可用的浏览器 cookie 来源列表。"""
    local_appdata = os.environ.get("LOCALAPPDATA", "")
    appdata = os.environ.get("APPDATA", "")
    candidates = [
        ("edge", os.path.join(local_appdata, "Microsoft", "Edge", "User Data")),
        ("chrome", os.path.join(local_appdata, "Google", "Chrome", "User Data")),
        ("brave", os.path.join(local_appdata, "BraveSoftware", "Brave-Browser", "User Data")),
        ("firefox", os.path.join(appdata, "Mozilla", "Firefox", "Profiles")),
    ]
    available: list[str] = []
    for browser, profile_dir in candidates:
        if profile_dir and os.path.isdir(profile_dir):
            available.append(browser)
    return available

# ---------------------------------------------------------------------------
# 数据模型
# ---------------------------------------------------------------------------


@dataclass
class DownloadPart:
    """Playlist 中单个 part（如 B站分P）的信息。"""
    index: int
    title: str
    video_path: str
    duration: float
    url: str = ""
    cid: int = 0            # B站 cid（弹幕/字幕用）


@dataclass
class DownloadResult:
    """统一下载结果。"""
    title: str
    platform: str
    video_path: str            # 单视频时的本地路径（多P时为空）
    duration: float            # 秒
    parts: list[DownloadPart] = field(default_factory=list)
    subtitle_paths: list[str] = field(default_factory=list)
    danmaku_texts: list[str] = field(default_factory=list)      # 弹幕文本列表
    comment_texts: list[str] = field(default_factory=list)      # 评论文本列表
    thumbnail_path: str = ""
    description: str = ""
    is_playlist: bool = False
    # B站专用字段
    bvid: str = ""
    aid: int = 0
    raw_info: dict = field(default_factory=dict, repr=False)


# ---------------------------------------------------------------------------
# 平台识别
# ---------------------------------------------------------------------------

_PLATFORM_PATTERNS: list[tuple[str, re.Pattern]] = [
    ("bilibili",    re.compile(r"bilibili\.com|b23\.tv|bili\w+\.com", re.I)),
    ("youtube",     re.compile(r"youtube\.com|youtu\.be", re.I)),
    ("douyin",      re.compile(r"douyin\.com|iesdouyin\.com", re.I)),
    ("xiaohongshu", re.compile(r"xiaohongshu\.com|xhslink\.com", re.I)),
    ("x",           re.compile(r"(?:^|\W)x\.com|twitter\.com", re.I)),
    ("tiktok",      re.compile(r"tiktok\.com", re.I)),
]


def detect_platform(url: str) -> str:
    """从 URL 识别平台名称，未知返回 ``'unknown'``。"""
    for name, pattern in _PLATFORM_PATTERNS:
        if pattern.search(url):
            return name
    return "unknown"


def is_social_url(url: str) -> bool:
    """判断是否为已知社交媒体 URL。"""
    return detect_platform(url) != "unknown"


# ---------------------------------------------------------------------------
# B站下载（原生 API）
# ---------------------------------------------------------------------------


def _resolve_bilibili_url(url: str) -> str:
    """如果是 b23.tv 短链，解析为完整 URL。"""
    if "b23.tv" in url:
        from OCRLLM.processors.social.bilibili_api import resolve_b23_short_url
        return resolve_b23_short_url(url)
    return url


def _download_bilibili(
    url: str,
    output_dir: str,
    cfg: AppConfig,
    *,
    part_indices: Optional[list[int]] = None,
    progress_hook: Optional[callable] = None,
) -> DownloadResult:
    """B站视频下载 — 使用原生 API。

    Args:
        url: B站视频 URL（支持 b23.tv 短链）。
        output_dir: 输出目录。
        cfg: 应用配置。
        part_indices: 仅下载指定的分P（从1开始）；None 表示全部。
        progress_hook: 进度回调 (current, total, message)。

    Returns:
        DownloadResult 实例。
    """
    from OCRLLM.processors.social.bilibili_api import (
        BiliSession, extract_bvid, get_video_info,
        download_video_part, fetch_danmaku, fetch_comments,
    )

    # 1. 解析 URL
    full_url = _resolve_bilibili_url(url)
    bvid = extract_bvid(full_url)

    # 2. 创建会话
    session = BiliSession(cookies_file=cfg.social.cookies_file)

    # 3. 获取视频信息
    info = get_video_info(session, bvid)
    logger.info(
        "[B站] 视频信息: %s (%d秒, %dP), 弹幕=%d, 评论=%d",
        info.title, info.duration, info.total_parts,
        info.danmaku_count, info.reply_count,
    )

    os.makedirs(output_dir, exist_ok=True)
    quality = cfg.social.bilibili_quality

    # 4. 确定要下载的分P
    target_parts = info.parts
    if part_indices:
        page_set = set(part_indices)
        target_parts = [p for p in info.parts if p.page in page_set]
        if not target_parts:
            raise ValueError(f"指定的分P {part_indices} 不存在，可用: 1-{info.total_parts}")

    # 5. 获取弹幕和评论
    danmaku_texts: list[str] = []
    comment_texts: list[str] = []

    if cfg.social.fetch_danmaku and target_parts:
        first_cid = target_parts[0].cid
        danmaku_texts = fetch_danmaku(session, first_cid)

    if cfg.social.fetch_comments:
        comment_texts = fetch_comments(session, info.aid, max_pages=cfg.social.comment_max_pages)

    # 6. 下载视频
    is_multi = len(target_parts) > 1
    total = len(target_parts)
    parts_result: list[DownloadPart] = []

    if is_multi:
        # 多P下载
        for idx, part in enumerate(target_parts):
            safe_name = re.sub(r'[<>:"/\\|?*]', '_', f"P{part.page}_{part.part}")[:80]
            part_dir = os.path.join(output_dir, safe_name)

            if progress_hook:
                progress_hook(idx, total, f"下载 P{part.page}: {part.part}")

            try:
                video_path = download_video_part(
                    session, bvid, part, part_dir, quality=quality,
                )
                parts_result.append(DownloadPart(
                    index=part.page, title=part.part,
                    video_path=video_path, duration=part.duration,
                    cid=part.cid,
                ))
                logger.info("[B站] P%d/%d 下载完成: %s", idx + 1, total, part.part)
            except Exception as exc:
                logger.error("[B站] P%d 下载失败: %s — %s", part.page, part.part, exc)
                parts_result.append(DownloadPart(
                    index=part.page, title=part.part,
                    video_path="", duration=part.duration,
                    cid=part.cid,
                ))

        return DownloadResult(
            title=info.title, platform="bilibili",
            video_path="", duration=info.duration,
            parts=parts_result, is_playlist=True,
            bvid=bvid, aid=info.aid,
            description=info.description,
            danmaku_texts=danmaku_texts,
            comment_texts=comment_texts,
        )

    else:
        # 单P下载
        part = target_parts[0]
        if progress_hook:
            progress_hook(0, 1, f"下载: {info.title}")

        video_path = download_video_part(
            session, bvid, part, output_dir, quality=quality,
        )

        # 单P也获取弹幕
        if cfg.social.fetch_danmaku and not danmaku_texts:
            danmaku_texts = fetch_danmaku(session, part.cid)

        return DownloadResult(
            title=info.title, platform="bilibili",
            video_path=video_path, duration=part.duration,
            bvid=bvid, aid=info.aid,
            description=info.description,
            danmaku_texts=danmaku_texts,
            comment_texts=comment_texts,
            parts=[DownloadPart(
                index=part.page, title=part.part,
                video_path=video_path, duration=part.duration,
                cid=part.cid,
            )],
        )


# ---------------------------------------------------------------------------
# yt-dlp 下载（非B站平台）
# ---------------------------------------------------------------------------


def _build_ydl_opts(
    cfg: AppConfig,
    output_dir: str,
    *,
    extract_subs: bool = True,
    browser_cookie_override: Optional[str] = None,
) -> dict:
    """构建 yt-dlp 选项字典。"""
    opts: dict = {
        "format": cfg.social.download_format,
        "outtmpl": os.path.join(output_dir, "%(title)s_%(id)s.%(ext)s"),
        "merge_output_format": "mp4",
        "retries": cfg.social.max_download_retries,
        "fragment_retries": cfg.social.max_download_retries,
        "concurrent_fragment_downloads": cfg.social.concurrent_fragment_downloads,
        "quiet": True,
        "no_warnings": False,
        "noprogress": True,
        "writeinfojson": True,
        "writesubtitles": extract_subs,
        "writeautomaticsub": extract_subs,
        "subtitleslangs": ["zh-Hans", "zh", "en", "ja"],
        "subtitlesformat": "srt/ass/vtt",
    }

    # Cookie 配置
    if cfg.social.cookies_file and os.path.isfile(cfg.social.cookies_file):
        opts["cookiefile"] = cfg.social.cookies_file
    elif browser_cookie_override:
        opts["cookiesfrombrowser"] = (browser_cookie_override,)
    elif cfg.social.cookies_from_browser:
        opts["cookiesfrombrowser"] = (cfg.social.cookies_from_browser,)

    # curl_cffi impersonate（绕过 TLS 指纹）
    try:
        from yt_dlp.networking.impersonate import ImpersonateTarget
        opts["impersonate"] = ImpersonateTarget(client="chrome")
    except Exception:
        pass

    # 新版 yt-dlp 默认只启用 deno；若系统已有其他 runtime，需要显式开启。
    js_runtimes: dict[str, dict[str, str]] = {}
    for runtime in ("node", "bun", "quickjs", "deno"):
        runtime_path = shutil.which(runtime)
        if runtime_path:
            js_runtimes[runtime] = {"path": runtime_path}
    if js_runtimes:
        opts["js_runtimes"] = js_runtimes

    return opts


def _collect_subtitle_paths(output_dir: str, video_id: str) -> list[str]:
    """收集已下载的字幕文件路径。"""
    results = []
    for f in Path(output_dir).iterdir():
        if video_id in f.name and f.suffix in (".srt", ".ass", ".vtt"):
            results.append(str(f))
    return sorted(results)


def _download_yt_dlp(
    url: str,
    output_dir: str,
    cfg: AppConfig,
    *,
    progress_hook: Optional[callable] = None,
) -> DownloadResult:
    """通用 yt-dlp 下载（非B站平台）。"""
    import yt_dlp

    os.makedirs(output_dir, exist_ok=True)
    platform = detect_platform(url)
    explicit_cookiefile = bool(cfg.social.cookies_file and os.path.isfile(cfg.social.cookies_file))
    explicit_browser = bool(cfg.social.cookies_from_browser)
    cookie_attempts: list[Optional[str]] = [None]
    if not explicit_cookiefile and not explicit_browser:
        cookie_attempts.extend(_available_browser_cookie_sources())

    info = None
    last_exc: Optional[Exception] = None
    for extract_subs in (True, False):
        if not extract_subs:
            logger.warning("[yt-dlp] 回退为无字幕模式继续下载: %s", url)

        retry_without_subs = False
        for attempt_idx, browser in enumerate(cookie_attempts, start=1):
            opts = _build_ydl_opts(
                cfg,
                output_dir,
                extract_subs=extract_subs,
                browser_cookie_override=browser,
            )
            opts["noplaylist"] = True
            if platform == "youtube":
                opts["remote_components"] = ["ejs:github"]
            if progress_hook:
                opts["progress_hooks"] = [progress_hook]

            if browser:
                logger.info("[yt-dlp] 尝试浏览器 cookies: %s (%d/%d)", browser, attempt_idx, len(cookie_attempts))

            try:
                with yt_dlp.YoutubeDL(opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                if info is None:
                    raise RuntimeError(f"yt-dlp 无法解析 URL: {url}")
                break
            except Exception as exc:
                last_exc = exc
                message = str(exc).lower()
                retryable = (
                    "sign in to confirm" in message
                    or "failed to load cookies" in message
                    or "could not copy chrome cookie database" in message
                )
                subtitle_failed = (
                    "unable to download video subtitles" in message
                    or ("video subtitles" in message and "http error 429" in message)
                )
                if browser:
                    logger.warning("[yt-dlp] 浏览器 cookies=%s 失败: %s", browser, exc)
                if subtitle_failed and extract_subs:
                    retry_without_subs = True
                    logger.warning("[yt-dlp] 字幕下载失败，准备切换为无字幕模式: %s", exc)
                    break
                if not retryable or attempt_idx == len(cookie_attempts):
                    raise

        if info is not None:
            break
        if not retry_without_subs:
            break

    if info is None:
        if last_exc:
            raise last_exc
        raise RuntimeError(f"yt-dlp 无法解析 URL: {url}")

    video_id = info.get("id", "unknown")
    title = info.get("title", "untitled")
    duration = float(info.get("duration") or 0)

    video_path = ""
    for f in Path(output_dir).iterdir():
        if f.suffix == ".mp4" and video_id in f.name:
            video_path = str(f)
            break
    if not video_path:
        mp4s = list(Path(output_dir).glob("*.mp4"))
        if mp4s:
            video_path = str(mp4s[0])

    return DownloadResult(
        title=title,
        platform=platform,
        video_path=video_path,
        duration=duration,
        subtitle_paths=_collect_subtitle_paths(output_dir, video_id),
        description=info.get("description", ""),
        raw_info=info,
    )


# ---------------------------------------------------------------------------
# 统一入口
# ---------------------------------------------------------------------------


def probe_video_info(url: str, cfg: AppConfig) -> dict:
    """仅提取视频信息，不下载。

    B站使用原生 API，其他平台使用 yt-dlp。

    Returns:
        标准化的视频信息字典。
    """
    platform = detect_platform(url)

    if platform == "bilibili":
        from OCRLLM.processors.social.bilibili_api import (
            BiliSession, extract_bvid, get_video_info,
        )
        full_url = _resolve_bilibili_url(url)
        bvid = extract_bvid(full_url)
        session = BiliSession(cookies_file=cfg.social.cookies_file)
        info = get_video_info(session, bvid)
        parts_info = [
            {"page": p.page, "part": p.part, "duration": p.duration, "cid": p.cid}
            for p in info.parts
        ]
        return {
            "platform": "bilibili",
            "bvid": bvid,
            "aid": info.aid,
            "title": info.title,
            "duration": info.duration,
            "parts": parts_info,
            "total_parts": info.total_parts,
            "description": info.description,
            "danmaku_count": info.danmaku_count,
            "reply_count": info.reply_count,
        }

    else:
        import yt_dlp
        explicit_cookiefile = bool(cfg.social.cookies_file and os.path.isfile(cfg.social.cookies_file))
        explicit_browser = bool(cfg.social.cookies_from_browser)
        cookie_attempts: list[Optional[str]] = [None]
        if not explicit_cookiefile and not explicit_browser:
            cookie_attempts.extend(_available_browser_cookie_sources())

        info = None
        last_exc: Optional[Exception] = None
        for attempt_idx, browser in enumerate(cookie_attempts, start=1):
            opts = {"quiet": True, "no_warnings": True, "extract_flat": "in_playlist"}
            if cfg.social.cookies_file and os.path.isfile(cfg.social.cookies_file):
                opts["cookiefile"] = cfg.social.cookies_file
            elif browser:
                opts["cookiesfrombrowser"] = (browser,)
            elif cfg.social.cookies_from_browser:
                opts["cookiesfrombrowser"] = (cfg.social.cookies_from_browser,)
            if platform == "youtube":
                opts["remote_components"] = ["ejs:github"]
            try:
                from yt_dlp.networking.impersonate import ImpersonateTarget
                opts["impersonate"] = ImpersonateTarget(client="chrome")
            except Exception:
                pass

            try:
                with yt_dlp.YoutubeDL(opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                break
            except Exception as exc:
                last_exc = exc
                message = str(exc).lower()
                retryable = (
                    "sign in to confirm" in message
                    or "fresh cookies" in message
                    or "failed to load cookies" in message
                    or "could not copy chrome cookie database" in message
                )
                if not retryable or attempt_idx == len(cookie_attempts):
                    raise

        if info is None:
            if last_exc:
                raise last_exc
            raise RuntimeError(f"yt-dlp 无法解析 URL: {url}")
        return {
            "platform": platform,
            "title": info.get("title", ""),
            "duration": info.get("duration", 0),
            "parts": [],
            "total_parts": 1,
        }


def download_media(
    url: str,
    output_dir: str,
    cfg: AppConfig,
    *,
    part_indices: Optional[list[int]] = None,
    progress_hook: Optional[callable] = None,
) -> DownloadResult:
    """统一下载入口 — 自动识别平台并选择最佳引擎。

    Args:
        url: 社交媒体视频 URL。
        output_dir: 输出根目录。
        cfg: 应用配置。
        part_indices: B站分P选择（从1开始），None=全部。
        progress_hook: 下载进度回调。

    Returns:
        DownloadResult 实例。
    """
    platform = detect_platform(url)
    logger.info("开始下载: platform=%s url=%s", platform, url)

    if platform == "bilibili":
        return _download_bilibili(
            url, output_dir, cfg,
            part_indices=part_indices,
            progress_hook=progress_hook,
        )

    # 非B站平台走 yt-dlp
    try:
        import yt_dlp  # noqa: F401
    except ImportError as exc:
        raise ImportError(
            "社交媒体下载需要 yt-dlp，请运行: pip install yt-dlp"
        ) from exc

    return _download_yt_dlp(url, output_dir, cfg, progress_hook=progress_hook)
