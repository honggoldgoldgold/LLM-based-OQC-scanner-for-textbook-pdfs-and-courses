"""
B站原生 API 引擎 — 绕过 yt-dlp 的 412 问题。

核心流程：
  1. curl_cffi 会话 + buvid cookie 认证
  2. 视频信息：/x/web-interface/view
  3. 视频流下载：/x/player/wbi/playurl → ffmpeg 合并
  4. 弹幕 XML：/x/v1/dm/list.so
  5. 评论：/x/v2/reply/main
  6. b23.tv 短链解析
"""

from __future__ import annotations

import io
import json
import logging
import os
import re
import struct
import subprocess
import time
import zlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
from xml.etree import ElementTree

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# 公共数据模型
# ---------------------------------------------------------------------------


@dataclass
class BiliVideoInfo:
    """单个 B站 视频/分P 的元信息。"""
    bvid: str
    aid: int
    cid: int                 # 当前 P 的 cid
    title: str
    part_title: str = ""     # 分P 标题
    duration: int = 0        # 秒
    page: int = 1
    description: str = ""
    pic: str = ""            # 封面 URL
    owner_name: str = ""
    view_count: int = 0
    danmaku_count: int = 0
    reply_count: int = 0


@dataclass
class BiliPartInfo:
    """B站分P 信息。"""
    page: int
    cid: int
    part: str       # 分P 标题
    duration: int   # 秒


@dataclass
class BiliPlaylistInfo:
    """B站视频（可含多P）的完整信息。"""
    bvid: str
    aid: int
    title: str
    description: str
    duration: int          # 总时长（秒）
    parts: list[BiliPartInfo] = field(default_factory=list)
    pic: str = ""
    owner_name: str = ""
    view_count: int = 0
    danmaku_count: int = 0
    reply_count: int = 0

    @property
    def is_multi_part(self) -> bool:
        return len(self.parts) > 1

    @property
    def total_parts(self) -> int:
        return len(self.parts)


# ---------------------------------------------------------------------------
# B站会话管理
# ---------------------------------------------------------------------------


class BiliSession:
    """管理 B站 API 会话（线程安全连接复用）。"""

    _API_BASE = "https://api.bilibili.com"
    _WWW_BASE = "https://www.bilibili.com"

    def __init__(self, *, cookies_file: str = "", sessdata: str = ""):
        self._session = None
        self._cookies_file = cookies_file
        self._sessdata = sessdata
        self._initialized = False

    def _ensure_session(self):
        """惰性初始化会话并获取 buvid。"""
        if self._initialized and self._session is not None:
            return
        try:
            from curl_cffi.requests import Session
        except ImportError:
            raise ImportError(
                "B站下载需要 curl_cffi，请运行: pip install 'curl_cffi>=0.10,<0.15'"
            )

        self._session = Session(impersonate="chrome")

        # 加载外部 cookie
        if self._cookies_file and os.path.isfile(self._cookies_file):
            self._load_cookies_file(self._cookies_file)
        if self._sessdata:
            self._session.cookies.set("SESSDATA", self._sessdata, domain=".bilibili.com")

        # 获取 buvid（即使有外部 cookie 也要）
        try:
            self._session.get(self._WWW_BASE, timeout=10)
            r = self._session.get(f"{self._API_BASE}/x/frontend/finger/spi", timeout=10)
            data = r.json().get("data", {})
            if data.get("b_3"):
                self._session.cookies.set("buvid3", data["b_3"], domain=".bilibili.com")
            if data.get("b_4"):
                self._session.cookies.set("buvid4", data["b_4"], domain=".bilibili.com")
            logger.debug("[B站] buvid 获取成功")
        except Exception as exc:
            logger.warning("[B站] buvid 获取失败: %s", exc)

        self._initialized = True

    def _load_cookies_file(self, path: str):
        """加载 Netscape cookies.txt 格式文件。"""
        try:
            with open(path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    parts = line.split("\t")
                    if len(parts) >= 7:
                        domain, _, _, _, _, name, value = parts[:7]
                        self._session.cookies.set(name, value, domain=domain)
            logger.info("[B站] 已加载 cookies: %s", path)
        except Exception as exc:
            logger.warning("[B站] Cookie 文件加载失败: %s — %s", path, exc)

    def get(self, url: str, **kwargs) -> dict:
        """发起 GET 请求，返回 JSON data 字段。"""
        self._ensure_session()
        kwargs.setdefault("timeout", 15)
        r = self._session.get(url, **kwargs)
        body = r.json()
        if body.get("code") != 0:
            raise RuntimeError(
                f"B站 API 错误 (code={body.get('code')}): {body.get('message', '未知错误')}"
            )
        return body.get("data", {})

    def get_raw(self, url: str, **kwargs) -> bytes:
        """发起 GET 请求，返回原始字节。"""
        self._ensure_session()
        kwargs.setdefault("timeout", 30)
        r = self._session.get(url, **kwargs)
        return r.content

    def download_file(self, url: str, dest: str, *, referer: str = ""):
        """下载文件到本地。"""
        self._ensure_session()
        headers = {"Referer": referer or self._WWW_BASE}
        r = self._session.get(url, headers=headers, timeout=120, stream=True)
        os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
        with open(dest, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                f.write(chunk)


# ---------------------------------------------------------------------------
# 视频信息
# ---------------------------------------------------------------------------


def resolve_b23_short_url(short_url: str) -> str:
    """将 b23.tv 短链解析为完整 B站 URL。

    优先用 curl_cffi（速度快）；若不可用则 fallback 到系统 curl。
    """
    try:
        from curl_cffi.requests import Session
        s = Session(impersonate="chrome")
        r = s.head(short_url, allow_redirects=True, timeout=10)
        if "bilibili.com" in r.url:
            return r.url
    except Exception:
        pass

    # Fallback: 系统 curl
    try:
        from OCRLLM.core.utils import windows_no_window_kwargs
        result = subprocess.run(
            ["curl", "-sIL", "-o", os.devnull, "-w", "%{url_effective}", short_url],
            capture_output=True, text=True, timeout=15,
            **windows_no_window_kwargs(),
        )
        if result.returncode == 0 and "bilibili.com" in result.stdout:
            return result.stdout.strip()
    except Exception as exc:
        logger.warning("[B站] 短链解析失败 (curl): %s", exc)

    raise RuntimeError(f"无法解析 B站短链: {short_url}")


def extract_bvid(url: str) -> str:
    """从 URL 中提取 BV 号。"""
    m = re.search(r"(BV[\w]+)", url)
    if m:
        return m.group(1)
    raise ValueError(f"无法从 URL 中提取 BV 号: {url}")


def get_video_info(session: BiliSession, bvid: str) -> BiliPlaylistInfo:
    """获取视频元数据（含分P 列表）。"""
    data = session.get(f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}")

    stat = data.get("stat", {})
    pages_data = data.get("pages", [])
    parts = [
        BiliPartInfo(
            page=p["page"],
            cid=p["cid"],
            part=p.get("part", f"P{p['page']}"),
            duration=p.get("duration", 0),
        )
        for p in pages_data
    ]

    return BiliPlaylistInfo(
        bvid=bvid,
        aid=data["aid"],
        title=data.get("title", ""),
        description=data.get("desc", ""),
        duration=data.get("duration", 0),
        parts=parts,
        pic=data.get("pic", ""),
        owner_name=data.get("owner", {}).get("name", ""),
        view_count=stat.get("view", 0),
        danmaku_count=stat.get("danmaku", 0),
        reply_count=stat.get("reply", 0),
    )


# ---------------------------------------------------------------------------
# 视频流下载
# ---------------------------------------------------------------------------


def _get_play_url(session: BiliSession, bvid: str, cid: int, *, quality: int = 80) -> dict:
    """获取视频播放流 URL。

    quality: 16=360P, 32=480P, 64=720P, 80=1080P, 112=1080P+, 116=1080P60, 120=4K
    fnval=4048 请求 dash 流
    """
    # 使用非 wbi 端点（wbi 需要签名，且未登录时返回 v_voucher）
    url = (
        f"https://api.bilibili.com/x/player/playurl"
        f"?bvid={bvid}&cid={cid}&qn={quality}&fnval=4048&fnver=0&fourk=1"
    )
    return session.get(url)


def download_video_part(
    session: BiliSession,
    bvid: str,
    part: BiliPartInfo,
    output_dir: str,
    *,
    quality: int = 80,
    progress_hook: Optional[callable] = None,
) -> str:
    """下载单个分P 视频。

    Returns:
        合并后的 mp4 文件路径。
    """
    os.makedirs(output_dir, exist_ok=True)

    play_data = _get_play_url(session, bvid, part.cid, quality=quality)
    dash = play_data.get("dash")

    if not dash:
        # flv 模式 (旧接口)
        durl = play_data.get("durl", [])
        if not durl:
            raise RuntimeError(f"无法获取视频流: bvid={bvid}, cid={part.cid}")
        video_url = durl[0]["url"]
        safe_title = re.sub(r'[<>:"/\\|?*]', '_', part.part)[:60]
        dest = os.path.join(output_dir, f"{safe_title}.mp4")
        logger.info("[B站] 下载 (flv): P%d %s", part.page, part.part)
        session.download_file(video_url, dest, referer=f"https://www.bilibili.com/video/{bvid}")
        return dest

    # DASH 模式：分别下载视频和音频，ffmpeg 合并
    video_streams = dash.get("video", [])
    audio_streams = dash.get("audio", [])

    if not video_streams:
        raise RuntimeError(f"DASH 无视频流: bvid={bvid}, cid={part.cid}")

    # 选最高质量但不超过请求的 quality
    best_video = sorted(
        [v for v in video_streams if v.get("id", 0) <= quality],
        key=lambda v: v.get("id", 0),
        reverse=True,
    )
    if not best_video:
        best_video = video_streams
    video_url = best_video[0].get("baseUrl") or best_video[0].get("base_url", "")

    audio_url = ""
    if audio_streams:
        best_audio = sorted(audio_streams, key=lambda a: a.get("bandwidth", 0), reverse=True)
        audio_url = best_audio[0].get("baseUrl") or best_audio[0].get("base_url", "")

    safe_title = re.sub(r'[<>:"/\\|?*]', '_', part.part)[:60]
    referer = f"https://www.bilibili.com/video/{bvid}"

    video_tmp = os.path.join(output_dir, f"_tmp_video_{part.page}.m4s")
    audio_tmp = os.path.join(output_dir, f"_tmp_audio_{part.page}.m4s")
    final_path = os.path.join(output_dir, f"{safe_title}.mp4")

    logger.info("[B站] 下载视频流: P%d %s", part.page, part.part)
    session.download_file(video_url, video_tmp, referer=referer)

    if audio_url:
        logger.info("[B站] 下载音频流: P%d", part.page)
        session.download_file(audio_url, audio_tmp, referer=referer)

    # ffmpeg 合并
    if audio_url and os.path.isfile(audio_tmp):
        cmd = [
            "ffmpeg", "-y", "-i", video_tmp, "-i", audio_tmp,
            "-c:v", "copy", "-c:a", "copy", "-movflags", "+faststart",
            final_path,
        ]
    else:
        cmd = ["ffmpeg", "-y", "-i", video_tmp, "-c", "copy", final_path]

    try:
        from OCRLLM.core.utils import windows_no_window_kwargs
        subprocess.run(cmd, capture_output=True, timeout=300, check=True, **windows_no_window_kwargs())
    except FileNotFoundError:
        raise RuntimeError("ffmpeg 未安装或不在 PATH 中，B站视频合并需要 ffmpeg")
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(f"ffmpeg 合并失败: {exc.stderr.decode(errors='replace')[:500]}")
    finally:
        for tmp in (video_tmp, audio_tmp):
            if os.path.isfile(tmp):
                try:
                    os.remove(tmp)
                except OSError:
                    pass

    logger.info("[B站] 合并完成: %s (%.1fMB)", final_path, os.path.getsize(final_path) / 1024 / 1024)
    return final_path


# ---------------------------------------------------------------------------
# 弹幕获取
# ---------------------------------------------------------------------------


def fetch_danmaku(session: BiliSession, cid: int) -> list[str]:
    """获取弹幕内容列表（去重、按时间排序）。

    Returns:
        弹幕文本列表。
    """
    url = f"https://api.bilibili.com/x/v1/dm/list.so?oid={cid}"
    try:
        raw = session.get_raw(url)
        # B站弹幕 API 返回 deflate 压缩的 XML
        try:
            xml_bytes = zlib.decompress(raw, -zlib.MAX_WBITS)
        except zlib.error:
            xml_bytes = raw

        root = ElementTree.fromstring(xml_bytes)
        danmakus: list[tuple[float, str]] = []
        seen = set()
        for d in root.findall(".//d"):
            text = (d.text or "").strip()
            if not text or text in seen:
                continue
            seen.add(text)
            # p 属性: "时间,模式,字号,颜色,时间戳,弹幕池,用户hash,dmid"
            p_attr = d.get("p", "0")
            try:
                time_sec = float(p_attr.split(",")[0])
            except (ValueError, IndexError):
                time_sec = 0.0
            danmakus.append((time_sec, text))

        danmakus.sort(key=lambda x: x[0])
        logger.info("[B站] 弹幕获取: cid=%d, %d 条", cid, len(danmakus))
        return [t for _, t in danmakus]

    except Exception as exc:
        logger.warning("[B站] 弹幕获取失败 (cid=%d): %s", cid, exc)
        return []


# ---------------------------------------------------------------------------
# 评论获取
# ---------------------------------------------------------------------------


def fetch_comments(session: BiliSession, aid: int, *, max_pages: int = 3) -> list[str]:
    """获取视频评论（热门 + 前几页）。

    Returns:
        评论文本列表（已去重）。
    """
    comments: list[str] = []
    seen: set[str] = set()

    for pn in range(1, max_pages + 1):
        url = (
            f"https://api.bilibili.com/x/v2/reply/main"
            f"?type=1&oid={aid}&mode=3&ps=20&pn={pn}"
        )
        try:
            data = session.get(url)
            replies = data.get("replies") or []
            if not replies:
                break
            for reply in replies:
                text = (reply.get("content", {}).get("message") or "").strip()
                if text and text not in seen:
                    seen.add(text)
                    comments.append(text)
                # 子评论
                sub_replies = reply.get("replies") or []
                for sub in sub_replies:
                    sub_text = (sub.get("content", {}).get("message") or "").strip()
                    if sub_text and sub_text not in seen:
                        seen.add(sub_text)
                        comments.append(sub_text)
        except Exception as exc:
            logger.warning("[B站] 评论获取失败 (aid=%d, pn=%d): %s", aid, pn, exc)
            break

    logger.info("[B站] 评论获取: aid=%d, %d 条", aid, len(comments))
    return comments


# ---------------------------------------------------------------------------
# 字幕获取
# ---------------------------------------------------------------------------


def fetch_subtitles(session: BiliSession, bvid: str, cid: int) -> list[dict]:
    """获取视频字幕（CC 字幕）。

    Returns:
        字幕段列表 [{"from": sec, "to": sec, "content": "..."}, ...]
    """
    url = (
        f"https://api.bilibili.com/x/player/wbi/v2"
        f"?bvid={bvid}&cid={cid}"
    )
    try:
        data = session.get(url)
        subtitle_info = data.get("subtitle", {})
        subtitles_list = subtitle_info.get("subtitles", [])
        if not subtitles_list:
            return []

        # 优先中文字幕
        target = subtitles_list[0]
        for s in subtitles_list:
            if "zh" in s.get("lan", ""):
                target = s
                break

        sub_url = target.get("subtitle_url", "")
        if not sub_url:
            return []
        if sub_url.startswith("//"):
            sub_url = "https:" + sub_url

        raw = session.get_raw(sub_url)
        sub_data = json.loads(raw)
        segments = sub_data.get("body", [])
        logger.info("[B站] 字幕获取: %d 段 (lang=%s)", len(segments), target.get("lan"))
        return segments

    except Exception as exc:
        logger.warning("[B站] 字幕获取失败 (bvid=%s, cid=%d): %s", bvid, cid, exc)
        return []


# ---------------------------------------------------------------------------
# 高层便捷函数
# ---------------------------------------------------------------------------


def extract_hotwords_from_social(
    danmaku: list[str],
    comments: list[str],
    *,
    max_hotwords: int = 100,
) -> list[str]:
    """从弹幕和评论中提取热词候选。

    简单策略：高频词 + 长度过滤。
    """
    from collections import Counter

    all_texts = danmaku + comments
    if not all_texts:
        return []

    # 简单分词：按标点/空格切分后取 2-8 字的片段（过长的是完整句子，不是热词）
    words: list[str] = []
    for text in all_texts:
        # 移除 @提及、表情标记
        text = re.sub(r"@\S+", "", text)
        text = re.sub(r"\[.*?\]", "", text)
        segments = re.split(r"[，。！？；：、\s,.\-!?;:]+", text)
        for seg in segments:
            seg = seg.strip()
            if 2 <= len(seg) <= 8:
                words.append(seg)

    counter = Counter(words)
    # 按频率排序，取出现 ≥2 次的或前 N 个
    hotwords = [w for w, c in counter.most_common(max_hotwords) if c >= 1]
    return hotwords[:max_hotwords]
