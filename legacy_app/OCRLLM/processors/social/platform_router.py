"""
URL → 平台路由 + 长短视频分流。

根据 URL 自动判断来源平台和视频类型（长视频教学 / 短视频知识），
并路由到对应的处理器。
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from OCRLLM.config import AppConfig
from OCRLLM.processors.social.downloader import detect_platform, probe_video_info

logger = logging.getLogger(__name__)


class VideoCategory(str, Enum):
    """视频分类。"""
    LONG = "long"     # 长视频教学（>阈值，走录课 Pipeline）
    SHORT = "short"   # 短视频知识（≤阈值，走场景切换 Pipeline）


@dataclass(frozen=True, slots=True)
class PlatformRoute:
    """URL 路由结果。"""
    url: str
    platform: str          # bilibili / youtube / douyin / xiaohongshu / x / unknown
    category: VideoCategory
    duration: float        # 秒（0 表示未知）
    title: str = ""
    is_playlist: bool = False
    part_count: int = 1


def classify_video(
    url: str,
    cfg: AppConfig,
    *,
    duration_override: Optional[float] = None,
) -> PlatformRoute:
    """根据 URL 和视频时长自动分类。

    如果无法获取时长（网络错误等），默认归为短视频处理路径。

    Args:
        url: 社交媒体 URL。
        cfg: 应用配置。
        duration_override: 手动指定时长（跳过网络探测）。

    Returns:
        PlatformRoute 路由结果。
    """
    platform = detect_platform(url)
    boundary = cfg.social.long_short_boundary_sec

    if duration_override is not None:
        duration = duration_override
        title = ""
        is_playlist = False
        part_count = 1
    else:
        try:
            info = probe_video_info(url, cfg)
            duration = float(info.get("duration") or 0)
            title = info.get("title", "")
            entries = info.get("entries")
            is_playlist = bool(entries)
            part_count = len(entries) if entries else 1
        except Exception as exc:
            logger.warning("无法探测视频信息 (url=%s): %s — 默认为短视频", url, exc)
            duration = 0
            title = ""
            is_playlist = False
            part_count = 1

    # 分类逻辑
    if is_playlist and part_count > 1:
        # playlist 不论单P时长，都走长视频路径（逐P处理）
        category = VideoCategory.LONG
    elif duration > boundary:
        category = VideoCategory.LONG
    else:
        category = VideoCategory.SHORT

    return PlatformRoute(
        url=url,
        platform=platform,
        category=category,
        duration=duration,
        title=title,
        is_playlist=is_playlist,
        part_count=part_count,
    )
