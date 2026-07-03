"""基于处理器注册表的输入识别与路由。"""

from __future__ import annotations

from dataclasses import dataclass
import os

from OCRLLM.config import AppConfig
from OCRLLM.processors.registry import ProcessorSpec, get_default_registry


class InputRoutingError(ValueError):
    """输入文件无法唯一映射到某个处理器。"""


@dataclass(frozen=True, slots=True)
class RoutedInputs:
    """路由结果 — 包含匹配的处理器规格和规范化后的文件路径。"""
    spec: ProcessorSpec
    paths: tuple[str, ...]

    @property
    def is_single_file(self) -> bool:
        """输入是否仅包含单个文件。"""
        return len(self.paths) == 1


def _is_url(text: str) -> bool:
    """判断是否为 URL 格式。"""
    return text.startswith(("http://", "https://"))


def _route_social_url(url: str) -> ProcessorSpec:
    """将社交媒体 URL 路由到对应的处理器。

    自动探测时长/playlist 并路由到 long / short。
    若探测失败，回退到 short，避免把 URL 当成本地文件处理。
    """
    from OCRLLM.processors.social.downloader import is_social_url
    from OCRLLM.processors.social.platform_router import classify_video, VideoCategory

    if not is_social_url(url):
        raise InputRoutingError(f"不是已知的社交媒体 URL: {url}")

    registry = get_default_registry()
    try:
        route = classify_video(url, AppConfig.from_env())
    except Exception:
        return registry.get("social_short")

    if route.category == VideoCategory.LONG:
        return registry.get("social_long")
    return registry.get("social_short")


def route_input_paths(
    paths: list[str] | tuple[str, ...] | str,
    *,
    allow_multiple_same_type: bool = False,
) -> RoutedInputs:
    """将输入文件路径路由到对应的处理器。

    支持本地文件路径和社交媒体 URL。

    Args:
        paths: 文件路径或 URL（字符串或列表）。

    Returns:
        RoutedInputs 实例。

    Raises:
        InputRoutingError: 无法识别或混合类型。
    """
    if isinstance(paths, str):
        normalized_paths = [_normalize_path(paths)]
    else:
        normalized_paths = [_normalize_path(path) for path in paths if str(path).strip()]

    if not normalized_paths:
        raise InputRoutingError("未提供可识别的输入文件")

    # 检查是否为社交媒体 URL
    if len(normalized_paths) == 1 and _is_url(normalized_paths[0]):
        try:
            spec = _route_social_url(normalized_paths[0])
            return RoutedInputs(spec=spec, paths=tuple(normalized_paths))
        except InputRoutingError:
            pass  # 不是社交媒体 URL，继续走文件路由

    registry = get_default_registry()
    specs = [registry.for_path(path) for path in normalized_paths]
    keys = {spec.key for spec in specs}

    if len(keys) == 1:
        spec = specs[0]
        if len(normalized_paths) > 1 and not (spec.accepts_multiple_files or allow_multiple_same_type):
            raise InputRoutingError(
                f"处理器 {spec.display_name} 不支持一次接收 {len(normalized_paths)} 个文件"
            )
        return RoutedInputs(spec=spec, paths=tuple(normalized_paths))

    raise InputRoutingError(
        "暂不支持混合文件类型一起处理: " + ", ".join(sorted(keys))
    )


def route_social_url(url: str, category: str = "auto") -> RoutedInputs:
    """专门为社交媒体 URL 提供的路由入口。

    Args:
        url: 社交媒体视频 URL。
        category: "long" / "short" / "auto"。auto 时按实际探测分类。

    Returns:
        RoutedInputs 实例。
    """
    from OCRLLM.processors.social.downloader import is_social_url
    if not is_social_url(url):
        raise InputRoutingError(f"不是已知的社交媒体 URL: {url}")

    registry = get_default_registry()
    if category == "long":
        spec = registry.get("social_long")
    elif category == "auto":
        spec = _route_social_url(url)
    else:
        spec = registry.get("social_short")

    return RoutedInputs(spec=spec, paths=(url,))


def identify_input_type(paths: list[str] | tuple[str, ...] | str) -> str:
    """识别输入文件的处理器类型 key。

    Args:
        paths: 文件路径（字符串或列表）。

    Returns:
        处理器 key（如 ``pdf``、``video``）。
    """
    return route_input_paths(paths).spec.key


def _normalize_path(path: str) -> str:
    text = str(path).strip().strip('"')
    if not text:
        return ""
    if text.startswith(("http://", "https://", "oss://")):
        return text
    return os.path.abspath(os.path.normpath(text))
