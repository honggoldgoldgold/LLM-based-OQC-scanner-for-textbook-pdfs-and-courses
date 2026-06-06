"""
OCRLLM 全局配置。

配置拆成多个子域，统一使用嵌套 section 访问和更新，避免单个 dataclass 持续膨胀。
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field, replace
from typing import Any


# 历史遗留：旧 GUI / 旧测试可能 import VISION_MODEL_OPTIONS。
# 真正的模型清单现在维护在 OCRLLM.core.model_catalog 里。
def _legacy_vision_options() -> tuple[str, ...]:
    try:
        from OCRLLM.core.model_catalog import BUILTIN_VISION_MODELS
        return tuple(m.name for m in BUILTIN_VISION_MODELS if m.kind == "vlm")
    except Exception:
        return ("qwen-vl-max", "qwen-vl-plus", "qwen3-vl-plus", "qwen3-vl-flash")


VISION_MODEL_OPTIONS = _legacy_vision_options()


@dataclass
class APIConfig:
    """API 连接配置（密钥、地址、付费模式）。"""
    api_key: str = field(
        default_factory=lambda: os.environ.get(
            "DASHSCOPE_API_KEY",
            "",
        )
    )
    base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    paid_mode: bool = False
    api_keys: list[str] = field(default_factory=list)


@dataclass
class VisionAPIConfig:
    """视觉模型可选的独立 OpenAI-compatible Provider 配置。

    留空/禁用时，图片、PDF、视频帧识别沿用 api 段；启用后仅视觉请求切到这里，
    长音频 filetrans 仍使用 DashScope api 段。
    """
    enabled: bool = False
    provider: str = ""
    api_key: str = ""
    base_url: str = ""
    wire_api: str = "chat"  # "chat" 或 "responses"
    model_reasoning_effort: str = ""
    network_access: bool = False
    disable_response_storage: bool = True


@dataclass
class ModelConfig:
    """模型名称配置。

    `vision_model` ：图片/截图/PDF/视频帧识别用的模型（VLM 或 omni）。
    `text_model`   ：纯文本任务用的模型，一般跟 vision_model 同一个或 flash 系列。
    `asr_model`    ：长录音异步识别（filetrans）模型。GUI 中的"音频模型"下拉控制此项。
    `asr_short_model` ：短录音同步模型，用于 <5min 音频；GUI 不直接暴露，
                       由系统在 audio_model 选定后自动派生（asr_long → 默认 short_model）。
    `allow_asr_short_fallback` ：长音频失败时是否允许回退分段短 ASR（默认禁用）。
    """
    vision_model: str = "qwen-vl-max"
    text_model: str = "qwen-vl-plus"
    asr_model: str = "qwen3-asr-flash-filetrans"
    asr_short_model: str = "qwen3-asr-flash"
    allow_asr_short_fallback: bool = False


@dataclass
class ProcessingConfig:
    """处理参数配置（批量大小、DPI、图像质量等）。"""
    batch_size: int = 10
    pdf_dpi: int = 200
    image_quality: int = 90
    image_max_side: int = 2048
    asr_short_chunk_seconds: int = 290


@dataclass
class ConcurrencyConfig:
    """并发参数配置（渲染线程、LLM 并行数、错峰间隔等）。"""
    pdf_render_workers: int = 0
    llm_parallel_requests: int = 15
    llm_request_stagger_seconds: float = 0.5
    video_resize_workers: int = 0
    audio_split_workers: int = 0
    audio_asr_parallel_requests: int = 4


@dataclass
class ResponseValidationConfig:
    """LLM 响应质量验证配置。"""
    enabled: bool = True
    min_chars: int = 20


@dataclass
class PathConfig:
    """输出和临时文件路径配置。"""
    output_dir: str = ""
    temp_dir: str = ""


@dataclass
class VideoConfig:
    """视频处理参数配置（抽帧间隔、变化阈值、遮挡检测等）。"""
    initial_sample_frames: int = 10
    frame_interval: float = 5.0
    refine_interval: float = 2.0
    change_threshold: float = 0.15
    drift_threshold: float = 0.10
    max_segment_sec: float = 150.0
    min_content_ratio: float = 0.005
    occlusion_threshold: float = 0.45
    phash_threshold: int = 3
    target_frames_per_hour: float = 40.0
    board_roi_padding: int = 10
    board_roi_override: tuple | None = None
    batch_size: int = 4


@dataclass
class ShotDetectionConfig:
    """场景切换检测参数配置（用于短视频抽帧）。"""
    backend: str = "scenedetect"           # "scenedetect" 或 "transnetv2"
    default_threshold: float = 0.3
    threshold_step: float = 0.05
    max_iterations: int = 8
    # 目标切换密度 (cuts/min)
    short_video_density_min: float = 5.0    # ≤2min 视频
    short_video_density_max: float = 35.0
    medium_video_density_min: float = 3.0   # 2-10min 视频
    medium_video_density_max: float = 20.0
    # 长短视频分界 (秒)
    long_video_threshold_sec: float = 600.0


@dataclass
class SocialConfig:
    """社交媒体下载与处理参数配置。"""
    download_format: str = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
    cookies_file: str = ""                  # cookies.txt 路径，留空则不使用
    cookies_from_browser: str = ""          # 浏览器名称（chrome/firefox/edge），留空则不使用
    max_download_retries: int = 3
    concurrent_fragment_downloads: int = 4
    # 长短视频分类阈值 (秒)；与 ShotDetectionConfig.long_video_threshold_sec 保持一致
    long_short_boundary_sec: float = 600.0
    # 短视频帧截取：终点前偏移 (秒)
    end_frame_offset_sec: float = 0.2
    # 短视频 LLM batch size (帧/批)
    short_video_batch_size: int = 2
    # B站原生 API 相关
    bilibili_quality: int = 80              # 16=360P, 32=480P, 64=720P, 80=1080P
    fetch_danmaku: bool = True              # 获取弹幕
    fetch_comments: bool = True             # 获取评论
    comment_max_pages: int = 3              # 评论最大翻页数


@dataclass
class ImagingConfig:
    """图像预处理参数配置（降噪、Canny 边缘检测、最小轮廓面积比等）。"""
    denoise_kernel_size: int = 3
    canny_low: int = 50
    canny_high: int = 150
    min_contour_area_ratio: float = 0.1


@dataclass
class AppConfig:
    """应用全局配置。"""

    api: APIConfig = field(default_factory=APIConfig)
    vision_api: VisionAPIConfig = field(default_factory=VisionAPIConfig)
    models: ModelConfig = field(default_factory=ModelConfig)
    processing: ProcessingConfig = field(default_factory=ProcessingConfig)
    concurrency: ConcurrencyConfig = field(default_factory=ConcurrencyConfig)
    response_validation: ResponseValidationConfig = field(default_factory=ResponseValidationConfig)
    paths: PathConfig = field(default_factory=PathConfig)
    video: VideoConfig = field(default_factory=VideoConfig)
    imaging: ImagingConfig = field(default_factory=ImagingConfig)
    social: SocialConfig = field(default_factory=SocialConfig)
    shot_detection: ShotDetectionConfig = field(default_factory=ShotDetectionConfig)

    def __post_init__(self):
        base_dir = os.path.dirname(__file__)
        if not self.paths.output_dir:
            self.paths.output_dir = os.path.join(base_dir, "output")
        if not self.paths.temp_dir:
            self.paths.temp_dir = os.path.join(base_dir, "temp")

    @classmethod
    def from_env(cls) -> AppConfig:
        """从环境变量加载配置。"""
        cfg = cls()
        updates = {}
        key = os.environ.get("DASHSCOPE_API_KEY")
        if key:
            updates.setdefault("api", {})["api_key"] = key
        url = os.environ.get("DASHSCOPE_BASE_URL")
        if url:
            updates.setdefault("api", {})["base_url"] = url
        vision_key = os.environ.get("OCRLLM_VISION_API_KEY")
        if vision_key:
            updates.setdefault("vision_api", {})["api_key"] = vision_key
            updates.setdefault("vision_api", {})["enabled"] = True
        vision_url = os.environ.get("OCRLLM_VISION_BASE_URL")
        if vision_url:
            updates.setdefault("vision_api", {})["base_url"] = vision_url
            updates.setdefault("vision_api", {})["enabled"] = True
        vision_wire_api = os.environ.get("OCRLLM_VISION_WIRE_API")
        if vision_wire_api:
            updates.setdefault("vision_api", {})["wire_api"] = vision_wire_api
        vision_model = os.environ.get("OCRLLM_VISION_MODEL")
        if vision_model:
            updates.setdefault("models", {})["vision_model"] = vision_model
        return cfg.with_updates(**updates) if updates else cfg

    def with_updates(self, **kwargs) -> AppConfig:
        """返回新的配置实例，只接受嵌套 section 更新。"""
        replacements: dict[str, Any] = {}
        for key, value in kwargs.items():
            if key not in _SECTION_NAMES:
                raise TypeError(f"with_updates 仅接受 section 名称，未知配置段: {key}")
            if isinstance(value, dict):
                replacements[key] = replace(getattr(self, key), **value)
            else:
                replacements[key] = value
        return replace(self, **replacements)


_SECTION_NAMES = {
    "api",
    "vision_api",
    "models",
    "processing",
    "concurrency",
    "response_validation",
    "paths",
    "video",
    "imaging",
    "social",
    "shot_detection",
}

