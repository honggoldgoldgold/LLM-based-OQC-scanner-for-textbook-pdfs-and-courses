"""
视频场景切换检测 — 自适应阈值。

支持两种后端：
  - scenedetect: PySceneDetect (纯 OpenCV，pip install scenedetect[opencv])
  - transnetv2:  TransNetV2 (需 TensorFlow/PyTorch)

默认使用 scenedetect，因安装门槛最低。
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Optional

from OCRLLM.config import AppConfig

logger = logging.getLogger(__name__)


@dataclass
class SceneCut:
    """单个场景切换点。"""
    frame_index: int       # 切换点帧号
    timestamp: float       # 秒
    confidence: float      # 检测置信度 (0-1)


@dataclass
class SceneSegment:
    """两个切换点之间的场景片段。"""
    index: int
    start_frame: int
    end_frame: int
    start_time: float      # 秒
    end_time: float        # 秒
    mid_frame: int = 0     # 中点帧
    end_offset_frame: int = 0  # 终点前偏移帧


@dataclass
class ShotDetectionResult:
    """场景检测完整结果。"""
    cuts: list[SceneCut] = field(default_factory=list)
    segments: list[SceneSegment] = field(default_factory=list)
    threshold_used: float = 0.0
    iterations_used: int = 0
    fps: float = 0.0
    total_frames: int = 0
    duration: float = 0.0


# ---------------------------------------------------------------------------
# PySceneDetect 后端
# ---------------------------------------------------------------------------


def _detect_with_scenedetect(
    video_path: str,
    threshold: float,
    fps: float,
) -> list[SceneCut]:
    """使用 PySceneDetect 的 AdaptiveDetector 检测场景切换。"""
    from scenedetect import open_video, SceneManager
    from scenedetect.detectors import AdaptiveDetector

    video = open_video(video_path)
    scene_manager = SceneManager()
    scene_manager.add_detector(AdaptiveDetector(
        adaptive_threshold=threshold,
        min_scene_len=15,  # 至少 15 帧才算一个场景
    ))
    scene_manager.detect_scenes(video, show_progress=False)
    scene_list = scene_manager.get_scene_list()

    cuts: list[SceneCut] = []
    for _start, end in scene_list:
        frame_idx = end.get_frames()
        ts = end.get_seconds()
        cuts.append(SceneCut(
            frame_index=frame_idx,
            timestamp=ts,
            confidence=1.0,  # scenedetect 不提供置信度
        ))
    return cuts


# ---------------------------------------------------------------------------
# TransNetV2 后端 (可选)
# ---------------------------------------------------------------------------


def _detect_with_transnetv2(
    video_path: str,
    threshold: float,
    fps: float,
) -> list[SceneCut]:
    """使用 TransNetV2 检测场景切换（需 pip install transnetv2）。"""
    try:
        from transnetv2 import TransNetV2
    except ImportError as exc:
        raise ImportError(
            "TransNetV2 后端需要安装: pip install git+https://github.com/soCzech/TransNetV2.git"
        ) from exc

    model = TransNetV2()
    _video_frames, single_pred, _all_pred = model.predict_video(video_path)
    scenes = model.predictions_to_scenes(single_pred, threshold=threshold)

    cuts: list[SceneCut] = []
    for _start, end in scenes:
        cuts.append(SceneCut(
            frame_index=int(end),
            timestamp=float(end) / fps if fps > 0 else 0,
            confidence=float(single_pred[min(end, len(single_pred) - 1)]),
        ))
    return cuts


# ---------------------------------------------------------------------------
# 自适应阈值检测
# ---------------------------------------------------------------------------


def _get_target_density(duration: float, cfg: AppConfig) -> tuple[float, float]:
    """根据视频时长返回目标切换密度范围 (min, max) cuts/min。"""
    if duration <= 120:
        return cfg.shot_detection.short_video_density_min, cfg.shot_detection.short_video_density_max
    return cfg.shot_detection.medium_video_density_min, cfg.shot_detection.medium_video_density_max


def detect_shots(
    video_path: str,
    cfg: AppConfig,
    *,
    backend: Optional[str] = None,
    initial_threshold: Optional[float] = None,
) -> ShotDetectionResult:
    """自适应阈值场景切换检测。

    1. 以初始阈值检测切换点
    2. 计算 cuts_per_minute
    3. 若超出目标范围，调整阈值并重新检测（最多 max_iterations 次）

    Args:
        video_path: 视频文件路径。
        cfg: 应用配置。
        backend: "scenedetect" 或 "transnetv2"，默认从配置读取。
        initial_threshold: 初始阈值覆盖。

    Returns:
        ShotDetectionResult 包含切换点列表和最终使用的参数。
    """
    import cv2

    # 获取视频信息
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"无法打开视频: {video_path}")
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps
    cap.release()

    if duration <= 0:
        raise ValueError(f"视频时长为 0: {video_path}")

    backend = backend or cfg.shot_detection.backend
    threshold = initial_threshold or cfg.shot_detection.default_threshold
    step = cfg.shot_detection.threshold_step
    max_iter = cfg.shot_detection.max_iterations

    density_min, density_max = _get_target_density(duration, cfg)
    detect_fn = _detect_with_scenedetect if backend == "scenedetect" else _detect_with_transnetv2

    best_cuts: list[SceneCut] = []
    used_threshold = threshold
    iterations = 0

    for i in range(max_iter):
        iterations = i + 1
        try:
            cuts = detect_fn(video_path, threshold, fps)
        except Exception as exc:
            logger.error("场景检测失败 (backend=%s, threshold=%.2f): %s", backend, threshold, exc)
            break

        cuts_per_min = len(cuts) / (duration / 60.0) if duration > 0 else 0
        logger.info(
            "迭代 %d: threshold=%.3f → %d 切换点, %.1f/min (目标 %.0f-%.0f)",
            iterations, threshold, len(cuts), cuts_per_min, density_min, density_max,
        )

        best_cuts = cuts
        used_threshold = threshold

        if density_min <= cuts_per_min <= density_max:
            break
        elif cuts_per_min > density_max:
            threshold += step  # 降低灵敏度
        elif cuts_per_min < density_min:
            threshold -= step  # 提高灵敏度

        # 阈值边界检查
        threshold = max(0.05, min(threshold, 0.95))

    # 构建场景片段
    segments = _build_segments(best_cuts, total_frames, fps, cfg)

    return ShotDetectionResult(
        cuts=best_cuts,
        segments=segments,
        threshold_used=used_threshold,
        iterations_used=iterations,
        fps=fps,
        total_frames=total_frames,
        duration=duration,
    )


def _build_segments(
    cuts: list[SceneCut],
    total_frames: int,
    fps: float,
    cfg: AppConfig,
) -> list[SceneSegment]:
    """根据切换点划分场景片段，并计算每段的中点帧和终点前偏移帧。"""
    if not cuts:
        # 无切换点：整个视频作为一个片段
        end_offset = max(0, int(total_frames - cfg.social.end_frame_offset_sec * fps))
        return [SceneSegment(
            index=0,
            start_frame=0,
            end_frame=total_frames - 1,
            start_time=0.0,
            end_time=(total_frames - 1) / fps,
            mid_frame=total_frames // 2,
            end_offset_frame=end_offset,
        )]

    # 加入起始点和终点
    boundaries = [0] + [c.frame_index for c in cuts] + [total_frames - 1]
    segments: list[SceneSegment] = []

    for i in range(len(boundaries) - 1):
        start = boundaries[i]
        end = boundaries[i + 1]
        if end <= start:
            continue

        mid = (start + end) // 2
        end_offset = max(start, int(end - cfg.social.end_frame_offset_sec * fps))

        segments.append(SceneSegment(
            index=len(segments),
            start_frame=start,
            end_frame=end,
            start_time=start / fps,
            end_time=end / fps,
            mid_frame=mid,
            end_offset_frame=end_offset,
        ))

    return segments
