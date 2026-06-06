# 社交媒体学习功能 — 实施后文档

> 编写时间：2026-04-13  
> 状态：实施完成  
> 对应前置文档：`social_media_design_pre.md`

---

## 一、实施概览

本次实施为 OCRLLM 新增三大能力：

1. **社交媒体视频下载与识别** — 支持 Bilibili / YouTube / 抖音 / 小红书 / X 平台 URL 直接输入
2. **短视频知识提取流水线** — 基于 PySceneDetect 的场景切换检测 + 自适应阈值 + LLM 画面描述
3. **FastAPI 服务层** — 对外暴露 HTTP API，为 STAv2 集成提供接口

---

## 二、文件清单

### 2.1 新建文件（10 个）

| 文件 | 行数 | 用途 |
|------|------|------|
| `processors/social/__init__.py` | 1 | 社交媒体处理子模块标记 |
| `processors/social/downloader.py` | 375 | 基于 yt-dlp 的统一下载引擎，支持 6 个平台、B站分P、Cookie、字幕提取 |
| `processors/social/platform_router.py` | 97 | URL→平台识别 + 长/短视频分类（探测时长，>10min→长） |
| `processors/social/short_video.py` | 255 | 短视频处理器（5阶段：检测→抽帧→LLM→ASR→合并） |
| `processors/social/long_video.py` | 144 | 长视频处理器（下载→委派 VideoProcessor 5阶段 Pipeline） |
| `imaging/shot_detector.py` | 265 | 场景切换边界检测 + 自适应阈值循环 |
| `core/short_video_merge.py` | 156 | 短视频场景描述与 ASR 文本按时间对齐合并 |
| `api/__init__.py` | 1 | API 服务子模块标记 |
| `api/server.py` | 391 | FastAPI 服务：任务提交/状态/结果/取消/列表 端点 |
| `api/sta_bridge.py` | 264 | STAv2 集成接口定义 + OcrllmApiClient 参考实现 |

**合计**：~1,949 行新代码

### 2.2 修改文件（6 个）

| 文件 | 变更内容 |
|------|---------|
| `config.py` | 新增 `ShotDetectionConfig` 和 `SocialConfig` 两个 dataclass，注册到 `AppConfig._SECTION_NAMES` |
| `requirements.txt` | 新增 3 个依赖分类：`yt-dlp`、`scenedetect[opencv]`、`fastapi` + `uvicorn[standard]` |
| `core/document_model.py` | `SourceType` 枚举新增 `SOCIAL_VIDEO = "social_video"` |
| `prompts.py` | 新增 `SHORT_VIDEO_RECOGNIZE` 模板（画面描述导向，非板书识别导向） |
| `processors/registry.py` | 注册 `social_long`（SocialLongVideoProcessor）和 `social_short`（ShortVideoProcessor） |
| `processors/routing.py` | 新增 `_is_url()` / `_route_social_url()` / `route_social_url()`，`route_input_paths()` 支持 URL 输入 |

---

## 三、架构决策记录

### 3.1 下载引擎：仅 yt-dlp

前置设计中计划以 f2 作为中国平台辅助。实施中决定**仅使用 yt-dlp**：
- yt-dlp 已原生支持 Bilibili、抖音、小红书、X、YouTube
- 减少依赖复杂度
- f2 可在未来按需以 fallback 形式补充

### 3.2 场景检测：仅 PySceneDetect

前置设计中 TransNetV2 作为增强方案。实施中：
- `imaging/shot_detector.py` 预留了 `_detect_with_transnetv2()` 接口
- 默认使用 `scenedetect.AdaptiveDetector`（纯 OpenCV，无 GPU 依赖）
- 配置中 `backend` 字段支持切换：`"scenedetect"` (默认) 或 `"transnetv2"`

### 3.3 OCRLLM ↔ STAv2 解耦

采用 **HTTP API 解耦**，不在 import 层耦合：
- OCRLLM 以独立 `uvicorn` 服务运行（端口 8100）
- STAv2 通过 `OcrllmApiClient` 发起 HTTP 请求
- 共享文件系统传递输出（OCRLLM 写入 .md → STAv2 WatcherService 检测）

### 3.4 短视频不使用记忆系统

长视频录课识别使用 `chat_with_images_contextual`（跨帧记忆去重）；短视频识别使用 `chat_with_images`（无记忆），原因：
- 短视频场景间关联性弱，记忆去重反而会丢失重复出现的关键内容
- 每个场景独立识别，并行友好

---

## 四、核心组件详述

### 4.1 下载引擎 (`processors/social/downloader.py`)

```python
# 关键数据结构
@dataclass
class DownloadResult:
    platform: str          # bilibili / youtube / douyin / ...
    title: str
    video_path: str        # 下载后视频文件绝对路径
    audio_path: str        # 分离的音频路径（如有）
    subtitle_path: str     # 字幕文件路径（如有）
    duration: float        # 视频时长（秒）
    parts: list[DownloadPart]  # B站分P列表

# 关键函数
detect_platform(url: str) -> str      # 正则匹配6个平台
is_social_url(url: str) -> bool       # 是否为已知社交媒体URL
download_media(url, output_dir, cfg)  # 统一入口（自动识别B站分P）
probe_video_info(url, cfg)            # 不下载仅探测信息
```

**B站分P处理**：`download_playlist()` 检测 `entries[]`，每个 part 下载到独立子目录 `Part_{idx}_{title}/`。

**Cookie 支持**：`SocialConfig.cookies_from_browser`（默认 `"chrome"`）或 `cookies_file` 路径。

### 4.2 场景检测 (`imaging/shot_detector.py`)

```python
# 关键数据结构
@dataclass(frozen=True)
class SceneCut:        # 单个切换点
    frame_num: int
    timecode: float

@dataclass(frozen=True)
class SceneSegment:    # 两个切换点之间的片段
    start_frame: int
    end_frame: int
    start_time: float
    end_time: float
    mid_frame: int           # 中点帧号
    end_offset_frame: int    # 终点前 0.2s 帧号

@dataclass
class ShotDetectionResult:
    cuts: list[SceneCut]
    segments: list[SceneSegment]
    threshold_used: float
    iterations: int

# 核心函数
detect_shots(video_path, cfg) -> ShotDetectionResult
```

**自适应阈值**：
```
初始阈值 = 0.3 (ShotDetectionConfig.default_threshold)
循环最多 8 次 (max_iterations):
    检测 → 计算 cuts/min
    短视频(≤2min): 目标 10-20/min
    中视频(2-10min): 目标 4-15/min
    过多 → threshold += 0.05
    过少 → threshold -= 0.05
```

### 4.3 短视频处理器 (`processors/social/short_video.py`)

5 个阶段：

| 阶段 | 内容 | 说明 |
|------|------|------|
| Phase 1 | `detect_shots()` | 场景切换边界检测 + 自适应阈值 |
| Phase 2 | `_extract_frames()` | OpenCV 定位提取中点帧 + 终点前帧 |
| Phase 3 | `_recognize_scenes()` | 并行 LLM `chat_with_images`，使用 `SHORT_VIDEO_RECOGNIZE` 提示词 |
| Phase 4 | `AudioProcessor.process()` | 复用现有音频处理器的 ASR 能力 |
| Phase 5 | `merge_scenes_and_asr()` | 按时间对齐合并场景描述与语音内容 |

**输出格式**：`{video_stem}_识别.md`

### 4.4 长视频处理器 (`processors/social/long_video.py`)

流程简洁：下载 → 委派给现有 `VideoProcessor`。

- 单视频：直接调用 `VideoProcessor.process(local_video_path)`
- B站分P：每个 part 创建独立 `VideoProcessor` 实例，各自输出到独立子目录

### 4.5 短视频合并 (`core/short_video_merge.py`)

```python
merge_scenes_and_asr(scene_md: str, asr_text: str, title: str) -> str
```

- 解析场景描述中的 `<!-- meta:scene id=X time=MM:SS~MM:SS -->` 标记
- 解析 ASR 文本中的 `<!-- meta:segment ... -->` 标记
- 按时间重叠率匹配 ASR 段到对应场景
- ASR 内容以 blockquote 格式附加：`> **语音内容：**`

### 4.6 FastAPI 服务 (`api/server.py`)

**端点**：

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/health` | 健康检查 |
| POST | `/api/ocrllm/process` | 提交处理任务（返回 task_id） |
| GET | `/api/ocrllm/status/{task_id}` | 查询任务进度 |
| GET | `/api/ocrllm/result/{task_id}` | 获取识别结果（<5MB 直返，否则路径） |
| POST | `/api/ocrllm/cancel/{task_id}` | 发送取消信号 |
| GET | `/api/ocrllm/tasks` | 列出所有任务 |

**任务提交请求体**：
```json
{
  "type": "social_short | social_long | auto | pdf | video | audio | board",
  "source": "https://www.bilibili.com/video/BVxxxxx 或 /path/to/file.pdf",
  "output_dir": "可选，输出目录",
  "options": {}
}
```

**执行模型**：`ThreadPoolExecutor(max_workers=3)` 后台执行，协作式取消（`cancel_event`）。

**启动命令**：
```bash
uvicorn OCRLLM.api.server:app --host 0.0.0.0 --port 8100
```

### 4.7 STAv2 集成桥接 (`api/sta_bridge.py`)

提供两个组件：

1. **`OcrllmApiClient`** — HTTP 客户端类，封装对 OCRLLM API 的调用：
   ```python
   client = OcrllmApiClient(base_url="http://localhost:8100")
   task_id = client.submit("social_short", url)
   status = client.get_status(task_id)
   result = client.get_result(task_id)
   client.cancel(task_id)
   ```

2. **`OcrllmBridgePlugin`** — 参考实现，展示 STAv2 插件如何：
   - 订阅 `FILE_CREATED` 事件
   - 识别媒体文件类型 → 自动提交 OCRLLM 任务
   - 发布 `OCRLLM_TASK_SUBMITTED` / `PROGRESS` / `COMPLETED` / `FAILED` 事件

---

## 五、配置新增项

### 5.1 `ShotDetectionConfig`

```python
@dataclass
class ShotDetectionConfig:
    backend: str = "scenedetect"     # "scenedetect" 或 "transnetv2"
    default_threshold: float = 0.3
    threshold_step: float = 0.05
    max_iterations: int = 8
    short_video_density_min: float = 10.0   # cuts/min
    short_video_density_max: float = 20.0
    medium_video_density_min: float = 4.0
    medium_video_density_max: float = 15.0
```

### 5.2 `SocialConfig`

```python
@dataclass
class SocialConfig:
    download_format: str = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
    cookies_file: str = ""                # cookies.txt 文件路径
    cookies_from_browser: str = "chrome"  # 浏览器名称
    long_short_boundary_sec: float = 600.0  # 长/短视频分界 (10分钟)
    end_frame_offset_sec: float = 0.2      # 终点前帧偏移量
    short_video_batch_size: int = 2        # LLM 每批帧数
```

---

## 六、新增依赖

```
# requirements.txt 新增
yt-dlp>=2025.3.17
scenedetect[opencv]>=0.6.7
fastapi>=0.135.0
uvicorn[standard]>=0.44.0
```

安装验证（已通过）：
```
yt-dlp: 2026.03.17 ✓
scenedetect: 0.6.7.1 ✓
fastapi: 0.135.3 ✓
uvicorn: 0.44.0 ✓
```

---

## 七、验证结果

### 7.1 配置加载

```
AppConfig() → SocialConfig + ShotDetectionConfig 正确实例化 ✓
```

### 7.2 处理器注册

```
ProcessorRegistry.all() → 包含 social_long, social_short ✓
注册总数: 11 个处理器
```

### 7.3 平台识别

```
bilibili.com      → bilibili  ✓
b23.tv             → bilibili  ✓
youtube.com        → youtube   ✓
douyin.com         → douyin    ✓
xiaohongshu.com    → xiaohongshu ✓
twitter.com / x.com → x        ✓
other.com          → unknown   ✓
```

### 7.4 URL 路由

```
社交媒体 URL → 默认路由到 social_short ✓
指定 category='long' → 路由到 social_long ✓
本地文件 .pdf → 路由到 pdf（不受影响） ✓
```

### 7.5 合并逻辑

```
场景描述 + ASR 文本 → 按时间对齐合并 → 正确输出带 blockquote 的 Markdown ✓
```

### 7.6 FastAPI 端点

```
GET  /api/health               → 200 ✓
POST /api/ocrllm/process       → 200 (task_id 返回) ✓
GET  /api/ocrllm/status/{id}   → 200 (进度快照) ✓
POST /api/ocrllm/cancel/{id}   → 200 (取消信号发送) ✓
GET  /api/ocrllm/tasks         → 200 (空列表) ✓
```

---

## 八、已知限制与后续计划

### 8.1 当前限制

| 限制 | 说明 |
|------|------|
| 抖音/小红书需要 Cookie | 无登录态时部分视频无法下载（yt-dlp 限制） |
| TransNetV2 未集成 | `shot_detector.py` 预留了接口但未实现 `_detect_with_transnetv2()` |
| f2 未集成 | 仅以 yt-dlp 覆盖所有平台 |
| GUI 社交媒体 Tab 未实现 | 当前仅支持 CLI (`cli.py`) 和 API (`api/server.py`) 入口 |
| STAv2 插件未部署 | `sta_bridge.py` 为参考实现，需在 STAv2 侧实际注册 |
| 弹幕/评论未利用 | 下载时可获取但暂未作为热词或上下文使用 |

### 8.2 后续迭代方向

1. **GUI 集成**：在 `gui/tabs/` 新增 `social_tab.py`，提供 URL 粘贴框 + 长/短切换 + 批量导入
2. **Cookie 管理 UI**：在 GUI 中提供 Cookie 导入/浏览器选择界面
3. **TransNetV2 可选安装**：`pip install OCRLLM[transnetv2]` extras_require
4. **弹幕作为热词**：B站弹幕 → 高频词提取 → 作为 ASR 热词表
5. **字幕优先**：检测到视频已有字幕时，跳过 ASR 阶段
6. **STAv2 正式集成**：将 `OcrllmBridgePlugin` 部署到 STAv2 的 `PluginManager`
7. **f2 fallback**：对 yt-dlp 下载失败的中国平台 URL，自动降级到 f2

---

## 九、项目结构变更总览

```
OCRLLM/
├── api/                        ← 新增模块
│   ├── __init__.py
│   ├── server.py               ← FastAPI 服务 (391行)
│   └── sta_bridge.py           ← STAv2 集成桥接 (264行)
├── core/
│   ├── short_video_merge.py    ← 新增：场景+ASR合并 (156行)
│   └── document_model.py       ← 修改：新增 SourceType.SOCIAL_VIDEO
├── imaging/
│   └── shot_detector.py        ← 新增：场景切换检测 (265行)
├── processors/
│   ├── social/                 ← 新增模块
│   │   ├── __init__.py
│   │   ├── downloader.py       ← 下载引擎 (375行)
│   │   ├── platform_router.py  ← 平台路由 (97行)
│   │   ├── short_video.py      ← 短视频处理器 (255行)
│   │   └── long_video.py       ← 长视频处理器 (144行)
│   ├── registry.py             ← 修改：注册 social_long/social_short
│   └── routing.py              ← 修改：URL 输入路由
├── config.py                   ← 修改：新增 ShotDetectionConfig + SocialConfig
├── prompts.py                  ← 修改：新增 SHORT_VIDEO_RECOGNIZE
├── requirements.txt            ← 修改：新增 4 个依赖
└── docs/
    ├── social_media_design_pre.md   ← 前置设计文档
    └── social_media_design_post.md  ← 本文档
```
