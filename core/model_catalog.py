"""
模型目录 — OCRLLM 单一来源的模型清单。

将"哪些模型可选"与"如何标记免费额度/分类"集中维护，
GUI 与 CLI 通过 list_vision_models()/list_audio_models() 读取。

设计目标：
  1. 视觉与音频两组互不混淆。
  2. 每个 builtin 条目带有 free_quota 元数据（GUI 显示加粗"【免费额度】"）。
  3. 用户在 GUI 输入新模型名且通过测试后，会写入 user_models.json
     永久追加到清单中（builtin 之后），下次启动仍可用。

模型来源：通过 `client.models.list()` (OpenAI 兼容) + DashScope 原生 filetrans 枚举，
每个条目都用 LLMClient.probe_* 实测过：
  · 视觉模型：发一张含字符的小图，要求 OCR 出来；
  · 长音频模型：调 DashScope 异步 filetrans，看任务能否被受理。
失败 / 未激活的不放入 builtin，请通过 GUI 自定义+测试加入。

音频模型类型说明：
  - kind="asr_long"   长录音异步识别 (DashScope 原生 filetrans)，可处理 >>5min，录课首选
  - kind="asr_short"  短录音同步识别（OpenAI 兼容），≤5min
  - kind="omni_audio" 全模态音频聊天，仅适合短音频问答，不适合长录课
"""

from __future__ import annotations

import json
import logging
import os
import time
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Literal, Optional

from openai import OpenAI

logger = logging.getLogger(__name__)


VisionKind = Literal["vlm", "ocr", "omni", "general"]
AudioKind = Literal["asr_long", "asr_short", "omni_audio"]


@dataclass(frozen=True)
class VisionModel:
    """视觉模型条目。"""
    name: str                     # API 模型 ID
    label: str                    # 简短描述（不含【免费额度】后缀）
    kind: VisionKind              # vlm = 通用视觉, ocr = 专门 OCR, omni = 全模态, general = 通用大模型(支持图)
    free_quota: bool = False
    max_images: Optional[int] = None     # 单次请求最多图片张数（None = 未知/不限）
    note: str = ""


@dataclass(frozen=True)
class AudioModel:
    """音频识别模型条目。"""
    name: str
    label: str
    kind: AudioKind
    free_quota: bool = False
    max_seconds: Optional[int] = None    # 单次最长音频时长 (秒)
    note: str = ""

    @property
    def is_long_capable(self) -> bool:
        return self.kind == "asr_long"


@dataclass(frozen=True)
class BailianModelDiscovery:
    """Result of a real Alibaba Bailian/DashScope model list fetch."""

    raw_count: int
    vision: tuple[VisionModel, ...]
    audio: tuple[AudioModel, ...]
    raw_model_ids: tuple[str, ...]
    fetched_at: float


# ====================================================================
# Builtin 清单 — 全部经过实测可用 (sk-...839 在 2026-05-04 验证)
# ====================================================================
#
# 张数 / 时长说明（保守值，超过会被 API 拒绝）：
#   Qwen2.5-VL 系列   : ≤10 张图
#   Qwen3-VL 系列     : ≤10 张图
#   Qwen-VL-OCR       : ≤1  张图（按文档描述）
#   Qwen-Omni         : 视频/音频 ≤30s, 图 ≤10
#   Qwen3-Omni-Flash  : 总时长 ≤150s
#   Qwen3.5-Omni      : 音频 ≤3 小时, 视频 ≤1 小时
#   Qwen3.5/3.6 通用  : 同 VL 系列
#   Qwen ASR Filetrans: ≤12 小时, ≤2GB
#   Paraformer-v2/v1  : 长录音异步, 2GB
#   SenseVoice-v1     : 长录音异步
#   Fun-ASR           : 长录音异步
#

BUILTIN_VISION_MODELS: tuple[VisionModel, ...] = (
    # ---- Qwen2.5-VL（成熟稳定，OCR/图表/文档识别强） ----
    VisionModel("qwen-vl-max",        "Qwen2.5-VL Max — 通用最强视觉",          "vlm",     True, max_images=10),
    VisionModel("qwen-vl-max-latest", "Qwen2.5-VL Max（latest 快照）",            "vlm",     True, max_images=10),
    VisionModel("qwen-vl-plus",       "Qwen2.5-VL Plus — 平衡速度成本",          "vlm",     True, max_images=10),
    VisionModel("qwen-vl-plus-latest","Qwen2.5-VL Plus（latest 快照）",           "vlm",     True, max_images=10),
    # ---- Qwen-VL-OCR（专门 OCR） ----
    VisionModel("qwen-vl-ocr",        "Qwen-VL-OCR — 专门 OCR (文档/票据/手写)", "ocr",     True, max_images=1),
    VisionModel("qwen-vl-ocr-latest", "Qwen-VL-OCR（latest）",                    "ocr",     True, max_images=1),
    # ---- Qwen3-VL（新一代视觉，3D/长视频/agent） ----
    VisionModel("qwen3-vl-plus",      "Qwen3-VL Plus — 新一代视觉",              "vlm",     True, max_images=10),
    VisionModel("qwen3-vl-flash",     "Qwen3-VL Flash — 高性价比",                "vlm",     True, max_images=10),
    # ---- Qwen3.5 通用大模型，附带视觉 ----
    VisionModel("qwen3.5-plus",       "Qwen3.5 Plus — 通用最强 (含视觉)",        "general", True, max_images=10),
    VisionModel("qwen3.5-flash",      "Qwen3.5 Flash — 通用快 (含视觉)",         "general", True, max_images=10),
    # ---- Qwen3.6 通用大模型 ----
    VisionModel("qwen3.6-plus",       "Qwen3.6 Plus — 最新通用 (含视觉)",        "general", True, max_images=10),
    VisionModel("qwen3.6-flash",      "Qwen3.6 Flash — 最新通用快 (含视觉)",     "general", True, max_images=10),
    # ---- Qwen-Omni 全模态（图+音+视频） ----
    VisionModel("qwen-omni-turbo",    "Qwen-Omni Turbo — 全模态 (图/音/视频)",   "omni",    True, max_images=10,
                note="历史模型，已停止更新；总时长限制 40s"),
    VisionModel("qwen3-omni-flash",   "Qwen3-Omni Flash — 全模态",                "omni",    True, max_images=10,
                note="总时长 ≤150s；适合短视频/截图"),
    VisionModel("qwen3.5-omni-plus",  "Qwen3.5-Omni Plus — 全模态最强",          "omni",    True, max_images=10,
                note="音频 ≤3 小时, 视频 ≤1 小时"),
    VisionModel("qwen3.5-omni-flash", "Qwen3.5-Omni Flash — 全模态高性价比",     "omni",    True, max_images=10),
    # ---- 第三方 (Kimi) ----
    VisionModel("kimi-k2.5",          "Kimi K2.5 (Moonshot, 第三方)",             "general", True, max_images=10),
    VisionModel("kimi-k2.6",          "Kimi K2.6 (Moonshot, 第三方)",             "general", True, max_images=10),
)


BUILTIN_AUDIO_MODELS: tuple[AudioModel, ...] = (
    # ---- 长录音异步识别 (filetrans) — 录课首选 ----
    AudioModel("qwen3-asr-flash-filetrans", "Qwen3-ASR Flash Filetrans — 长录音异步 (≤12小时)",
               "asr_long",  True, max_seconds=12*3600,
               note="录课首选；DashScope 原生异步 API；支持中英多语种、热词 corpus"),
    AudioModel("paraformer-v2",             "Paraformer v2 — 经典长录音异步",
               "asr_long",  True, max_seconds=12*3600,
               note="阿里老牌 ASR；中英日韩德法俄等；带时间戳"),
    AudioModel("paraformer-v1",             "Paraformer v1 — 长录音异步 (旧版)",
               "asr_long",  True, max_seconds=12*3600,
               note="老版 paraformer，部分场景比 v2 更鲁棒"),
    AudioModel("sensevoice-v1",             "SenseVoice v1 — 长录音异步",
               "asr_long",  True, max_seconds=12*3600,
               note="SenseVoice 多语种 ASR；含情绪/事件标注"),
    AudioModel("fun-asr",                   "Fun-ASR — 长录音异步",
               "asr_long",  True, max_seconds=12*3600,
               note="Fun-ASR 系列；多语种支持"),
    # ---- 短录音同步识别 (OpenAI 兼容) ----
    AudioModel("qwen3-asr-flash-2026-02-10", "Qwen3-ASR Flash — 短音频同步 (≤5分钟)",
               "asr_short", True, max_seconds=300,
               note="短音频快速识别；不适合录课长音频"),
    # ---- Omni 全模态（仅适合短问答音频，不适合长录课） ----
    AudioModel("qwen-omni-turbo",            "Qwen-Omni Turbo — 全模态 (短音频聊天 ≤40s)",
               "omni_audio", True, max_seconds=40,
               note="历史 omni；非常短音频；不推荐用于录课"),
    AudioModel("qwen3-omni-flash",           "Qwen3-Omni Flash — 全模态 (≤150秒)",
               "omni_audio", True, max_seconds=150,
               note="新 omni；仍然不适合录课长音频"),
    AudioModel("qwen3.5-omni-plus",          "Qwen3.5-Omni Plus — 全模态 (≤3小时音频)",
               "omni_audio", True, max_seconds=3*3600,
               note="omni 中音频上下文最长，但价格贵；录课优先选 asr_long"),
)


# ====================================================================
# 用户自定义模型持久化
# ====================================================================

def user_models_path() -> Path:
    return Path.home() / ".OCRLLM" / "user_models.json"


def bailian_models_path() -> Path:
    return Path.home() / ".OCRLLM" / "bailian_models.json"


def is_dashscope_base_url(base_url: str) -> bool:
    marker = (base_url or "").lower()
    return "dashscope" in marker or "aliyuncs.com" in marker or "maas.aliyuncs.com" in marker


def _normalize_openai_base_url(base_url: str) -> str:
    normalized = (base_url or "").strip().rstrip("/")
    if not normalized:
        return normalized
    # Bailian console snippets use compatible-mode/v1. If the user enters a
    # regional host root, keep discovery usable by adding the compatible path.
    if normalized.endswith("/compatible-mode/v1") or normalized.endswith("/v1"):
        return normalized
    return f"{normalized}/compatible-mode/v1"


def _model_id_from_openai_item(item) -> str:
    if isinstance(item, dict):
        return str(item.get("id") or item.get("name") or "").strip()
    return str(getattr(item, "id", "") or getattr(item, "name", "") or "").strip()


def _fetch_openai_compatible_model_ids(base_url: str, api_key: str, timeout: float = 20.0) -> list[str]:
    normalized_url = _normalize_openai_base_url(base_url)
    if not normalized_url:
        raise ValueError("Base URL 为空，无法获取百炼模型列表")
    if not api_key:
        raise ValueError("API Key 为空，无法获取百炼模型列表")

    try:
        client = OpenAI(api_key=api_key, base_url=normalized_url, timeout=timeout, max_retries=0)
        models = client.models.list()
        ids = [_model_id_from_openai_item(item) for item in getattr(models, "data", []) or []]
        ids = [mid for mid in ids if mid]
        if ids:
            return sorted(dict.fromkeys(ids))
    except Exception as exc:
        logger.warning("[MODELS] OpenAI SDK 获取百炼模型列表失败，尝试 HTTP /models: %s", exc)

    req = urllib.request.Request(
        normalized_url.rstrip("/") + "/models",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = json.loads(resp.read().decode("utf-8"))
    if isinstance(body, dict) and isinstance(body.get("data"), list):
        raw = body["data"]
    elif isinstance(body, dict) and isinstance(body.get("models"), list):
        raw = body["models"]
    else:
        raw = []
    ids = [_model_id_from_openai_item(item) for item in raw]
    ids = [mid for mid in ids if mid]
    if not ids:
        raise RuntimeError("百炼 /models 返回成功，但没有可用模型 ID")
    return sorted(dict.fromkeys(ids))


def _classify_bailian_vision_model(model_id: str) -> VisionModel | None:
    name = model_id.strip()
    lowered = name.lower()
    if not name:
        return None
    if "asr" in lowered or lowered.startswith(("paraformer", "sensevoice", "fun-asr")):
        return None
    if "vl-ocr" in lowered or lowered.endswith("-ocr") or "-ocr-" in lowered:
        kind: VisionKind = "ocr"
        label = f"{name} — 百炼实时获取 OCR"
    elif "omni" in lowered:
        kind = "omni"
        label = f"{name} — 百炼实时获取全模态"
    elif "vl" in lowered:
        kind = "vlm"
        label = f"{name} — 百炼实时获取视觉"
    elif lowered.startswith(("qwen3.5", "qwen3.6")):
        kind = "general"
        label = f"{name} — 百炼实时获取通用模型"
    else:
        return None
    return VisionModel(name=name, label=label, kind=kind, free_quota=False, max_images=None, note="百炼 /models 实时获取")


def _classify_bailian_audio_model(model_id: str) -> AudioModel | None:
    name = model_id.strip()
    lowered = name.lower()
    if not name:
        return None
    if "filetrans" in lowered or lowered.startswith(("paraformer", "sensevoice", "fun-asr")):
        return AudioModel(
            name=name,
            label=f"{name} — 百炼实时获取长录音",
            kind="asr_long",
            free_quota=False,
            max_seconds=None,
            note="百炼 /models 实时获取",
        )
    if "asr" in lowered:
        return AudioModel(
            name=name,
            label=f"{name} — 百炼实时获取短音频",
            kind="asr_short",
            free_quota=False,
            max_seconds=None,
            note="百炼 /models 实时获取",
        )
    if "omni" in lowered:
        return AudioModel(
            name=name,
            label=f"{name} — 百炼实时获取全模态音频",
            kind="omni_audio",
            free_quota=False,
            max_seconds=None,
            note="百炼 /models 实时获取",
        )
    return None


def _save_bailian_models_raw(data: dict) -> None:
    path = bailian_models_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, path)


def _load_bailian_models_raw() -> dict:
    path = bailian_models_path()
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8")) or {}
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning("[MODELS] 百炼模型缓存读取失败 (%s)，按空处理", exc)
        return {}


def _vision_from_raw_items(items: list[dict]) -> tuple[VisionModel, ...]:
    out: list[VisionModel] = []
    for item in items:
        try:
            out.append(VisionModel(
                name=item["name"],
                label=item.get("label") or f"{item['name']} — 百炼实时获取",
                kind=item.get("kind", "vlm"),
                free_quota=bool(item.get("free_quota", False)),
                max_images=item.get("max_images"),
                note=item.get("note", "百炼 /models 实时获取"),
            ))
        except KeyError:
            continue
    return tuple(out)


def _audio_from_raw_items(items: list[dict]) -> tuple[AudioModel, ...]:
    out: list[AudioModel] = []
    for item in items:
        try:
            out.append(AudioModel(
                name=item["name"],
                label=item.get("label") or f"{item['name']} — 百炼实时获取",
                kind=item.get("kind", "asr_long"),
                free_quota=bool(item.get("free_quota", False)),
                max_seconds=item.get("max_seconds"),
                note=item.get("note", "百炼 /models 实时获取"),
            ))
        except KeyError:
            continue
    return tuple(out)


def load_bailian_vision_models() -> tuple[VisionModel, ...]:
    return _vision_from_raw_items(_load_bailian_models_raw().get("vision", []))


def load_bailian_audio_models() -> tuple[AudioModel, ...]:
    return _audio_from_raw_items(_load_bailian_models_raw().get("audio", []))


def bailian_model_cache_is_stale(max_age_seconds: float = 24 * 3600) -> bool:
    raw = _load_bailian_models_raw()
    fetched_at = raw.get("fetched_at")
    if not isinstance(fetched_at, (int, float)):
        return True
    return time.time() - float(fetched_at) > max_age_seconds


def refresh_bailian_models(base_url: str, api_key: str, timeout: float = 20.0) -> BailianModelDiscovery:
    """Fetch the actual Bailian model list and cache classified OCRLLM entries."""
    model_ids = _fetch_openai_compatible_model_ids(base_url, api_key, timeout=timeout)
    vision = tuple(m for mid in model_ids if (m := _classify_bailian_vision_model(mid)) is not None)
    audio = tuple(m for mid in model_ids if (m := _classify_bailian_audio_model(mid)) is not None)
    fetched_at = time.time()
    _save_bailian_models_raw({
        "source": "bailian-openai-compatible-models",
        "base_url": _normalize_openai_base_url(base_url),
        "fetched_at": fetched_at,
        "raw_model_ids": model_ids,
        "vision": [
            {
                "name": m.name,
                "label": m.label,
                "kind": m.kind,
                "free_quota": m.free_quota,
                "max_images": m.max_images,
                "note": m.note,
            }
            for m in vision
        ],
        "audio": [
            {
                "name": m.name,
                "label": m.label,
                "kind": m.kind,
                "free_quota": m.free_quota,
                "max_seconds": m.max_seconds,
                "note": m.note,
            }
            for m in audio
        ],
    })
    logger.info("[MODELS] 百炼模型刷新完成: raw=%d, vision=%d, audio=%d", len(model_ids), len(vision), len(audio))
    return BailianModelDiscovery(
        raw_count=len(model_ids),
        vision=vision,
        audio=audio,
        raw_model_ids=tuple(model_ids),
        fetched_at=fetched_at,
    )


def _load_user_models_raw() -> dict:
    path = user_models_path()
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8")) or {}
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning("[MODELS] 用户模型清单读取失败 (%s)，按空处理", exc)
        return {}


def _save_user_models_raw(data: dict) -> None:
    path = user_models_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, path)


def load_user_vision_models() -> tuple[VisionModel, ...]:
    raw = _load_user_models_raw().get("vision", [])
    out: list[VisionModel] = []
    for item in raw:
        try:
            out.append(VisionModel(
                name=item["name"],
                label=item.get("label") or f"{item['name']} — 用户自定义",
                kind=item.get("kind", "vlm"),
                free_quota=bool(item.get("free_quota", False)),
                max_images=item.get("max_images"),
                note=item.get("note", "用户自定义并通过测试"),
            ))
        except KeyError:
            continue
    return tuple(out)


def load_user_audio_models() -> tuple[AudioModel, ...]:
    raw = _load_user_models_raw().get("audio", [])
    out: list[AudioModel] = []
    for item in raw:
        try:
            out.append(AudioModel(
                name=item["name"],
                label=item.get("label") or f"{item['name']} — 用户自定义",
                kind=item.get("kind", "asr_long"),
                free_quota=bool(item.get("free_quota", False)),
                max_seconds=item.get("max_seconds"),
                note=item.get("note", "用户自定义并通过测试"),
            ))
        except KeyError:
            continue
    return tuple(out)


def save_user_vision_model(model: VisionModel) -> None:
    data = _load_user_models_raw()
    arr = [m for m in data.get("vision", []) if m.get("name") != model.name]
    arr.append({
        "name": model.name, "label": model.label, "kind": model.kind,
        "free_quota": model.free_quota, "max_images": model.max_images,
        "note": model.note,
    })
    data["vision"] = arr
    _save_user_models_raw(data)
    logger.info("[MODELS] 已保存用户视觉模型: %s", model.name)


def save_user_audio_model(model: AudioModel) -> None:
    data = _load_user_models_raw()
    arr = [m for m in data.get("audio", []) if m.get("name") != model.name]
    arr.append({
        "name": model.name, "label": model.label, "kind": model.kind,
        "free_quota": model.free_quota, "max_seconds": model.max_seconds,
        "note": model.note,
    })
    data["audio"] = arr
    _save_user_models_raw(data)
    logger.info("[MODELS] 已保存用户音频模型: %s", model.name)


def remove_user_vision_model(name: str) -> bool:
    data = _load_user_models_raw()
    arr = data.get("vision", [])
    new_arr = [m for m in arr if m.get("name") != name]
    if len(new_arr) == len(arr):
        return False
    data["vision"] = new_arr
    _save_user_models_raw(data)
    return True


def remove_user_audio_model(name: str) -> bool:
    data = _load_user_models_raw()
    arr = data.get("audio", [])
    new_arr = [m for m in arr if m.get("name") != name]
    if len(new_arr) == len(arr):
        return False
    data["audio"] = new_arr
    _save_user_models_raw(data)
    return True


# ====================================================================
# 合并 builtin + user
# ====================================================================

def list_vision_models() -> tuple[VisionModel, ...]:
    seen: dict[str, VisionModel] = {}
    for m in BUILTIN_VISION_MODELS:
        seen.setdefault(m.name, m)
    for m in load_bailian_vision_models():
        seen.setdefault(m.name, m)
    for m in load_user_vision_models():
        seen.setdefault(m.name, m)
    return tuple(seen.values())


def list_audio_models() -> tuple[AudioModel, ...]:
    seen: dict[str, AudioModel] = {}
    for m in BUILTIN_AUDIO_MODELS:
        seen.setdefault(m.name, m)
    for m in load_bailian_audio_models():
        seen.setdefault(m.name, m)
    for m in load_user_audio_models():
        seen.setdefault(m.name, m)
    return tuple(seen.values())


def find_vision_model(name: str) -> VisionModel | None:
    if not name:
        return None
    for m in list_vision_models():
        if m.name == name:
            return m
    return None


def find_audio_model(name: str) -> AudioModel | None:
    if not name:
        return None
    for m in list_audio_models():
        if m.name == name:
            return m
    return None


# ====================================================================
# 免费额度回退链
# ====================================================================

def free_vision_chain() -> list[str]:
    """免费额度视觉模型链，按 catalog 出现顺序。"""
    return [m.name for m in list_vision_models() if m.free_quota]


def free_audio_chain(kind: AudioKind | None = None) -> list[str]:
    """免费额度音频模型链。kind 可指定 asr_long / asr_short / omni_audio。"""
    return [m.name for m in list_audio_models() if m.free_quota and (kind is None or m.kind == kind)]


# ====================================================================
# 显示工具
# ====================================================================

def display_label(model: VisionModel | AudioModel) -> str:
    """构造统一的显示文本。GUI 用于列表/标签。"""
    suffix = "  【免费额度】" if model.free_quota else ""
    extra = ""
    if isinstance(model, VisionModel) and model.max_images:
        extra = f"（≤{model.max_images} 张图）"
    elif isinstance(model, AudioModel) and model.max_seconds:
        if model.max_seconds >= 3600:
            extra = f"（≤{model.max_seconds // 3600} 小时）"
        elif model.max_seconds >= 60:
            extra = f"（≤{model.max_seconds // 60} 分钟）"
        else:
            extra = f"（≤{model.max_seconds} 秒）"
    return f"{model.name} — {model.label.split('— ', 1)[-1] if '— ' in model.label else model.label}{extra}{suffix}"


def parse_model_name_from_display(text: str) -> str:
    if not text:
        return ""
    text = text.strip()
    if " — " in text:
        return text.split(" — ", 1)[0].strip()
    if "  " in text:
        return text.split("  ", 1)[0].strip()
    return text
