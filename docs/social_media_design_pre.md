# 社交媒体学习功能 — 前置设计文档

> 编写时间：2026-04-13  
> 状态：实施前

---

## 一、两项目现状分析

### 1.1 OCRLLM 项目现状

**定位**：基于大语言模型的课程内容识别系统，将 PDF/视频/音频/板书等学习材料转换为结构化 Markdown。

**核心架构**:

| 层级 | 组件 | 说明 |
|------|------|------|
| 入口 | `main.py` (GUI) / `cli.py` (CLI) | 双入口，GUI 基于 PyQt5，支持多窗口 |
| 配置 | `config.py` (`AppConfig`) | 嵌套 dataclass：API / Models / Processing / Concurrency / Video / Imaging |
| 处理器 | `processors/registry.py` | `ProcessorSpec` + `ProcessorRegistry`，按扩展名路由 |
| 处理器实现 | `processors/{pdf,board,video,audio}.py` | 继承 `BaseProcessor`，通过 DI 注入 cfg/llm/reporter/tracker/api_pool |
| 视频流水线 | `processors/video_pipeline.py` | 5 阶段 Phase Chain：音频提取→智能抽帧→预处理→LLM识别→ASR |
| LLM 层 | `core/llm_client.py` + `core/api_pool.py` | OpenAI 兼容 SDK，多 Key 负载均衡，6次指数退避重试 |
| 图像层 | `imaging/` | OCR引擎、PDF渲染、帧预处理、音频提取、扫描检测 |
| 输出层 | `core/incremental_writer.py` + `core/board_merge.py` | 增量乱序写入 + 模糊去重合并 |
| 断点续传 | `core/checkpoint.py` | JSON 检查点持久化，phase 级别恢复 |

**处理能力**:
- PDF：15 并发 LLM，802页 Deep Learning 全书 ~20min
- 视频：5阶段流水线，2.5小时录课 ~15min 抽帧 + LLM 识别
- 音频：短音频(<290s)同步ASR，长音频异步filetrans
- 板书：多图并行识别 + 模糊去重合并

**已有扩展点**:
- `ProcessorRegistry.register()` 支持动态注册新处理器
- `routing.py` 已有 URL 格式识别（`_normalize_path` 检测 http/https）
- `SourceType` 枚举可扩展
- `BaseProcessor` 提供完整的取消/进度/API池基础设施

**局限**:
- 仅支持本地文件输入，不支持 URL 直接处理
- 视频抽帧策略针对录课场景优化（低频切换、大面积板书），不适合短视频快速切换
- 无跨服务 API 暴露（仅 GUI/CLI 入口）

---

### 1.2 STAv2 项目现状

**定位**：本地优先的智能学习工作台，整合课程材料、笔记、任务管理和 AI 能力。

**技术栈**:

| 层级 | 技术 | 说明 |
|------|------|------|
| 前端 | React 19 + TypeScript + Vite + Tailwind CSS | SPA，CodeMirror 编辑器，KaTeX 数学渲染 |
| 后端 | FastAPI + SQLite | 异步 API，单库设计 |
| 运行时 | EventBus + WatcherService + JobRunnerService | 事件驱动，文件监控 + 后台任务队列 |
| 插件 | BasePlugin + PluginManager | 课表标签、每日简报等插件 |
| AI | AgentService | RAG 问答，工具绑定 |

**启动流程**:
```
FastAPI startup → AppContainer 初始化
  ├─ EventBus
  ├─ ChunkerService (订阅 FILE_CREATED/UPDATED/DELETED/MOVED)
  ├─ RuntimeService
  ├─ WatcherService (监控 WORKSPACE/notes, courses, daily)
  ├─ JobRunnerService (后台轮询 job_queue 表)
  └─ PluginManager (TimetableTagger + DailyBriefing)
```

**任务系统**:
- `job_queue` 表：job_id, job_type, scope_type, scope_key, status(pending/running/done/failed), priority
- `JobRunnerService`：后台守护线程，2s/0.2s 轮询，支持重试+指数退避
- `JobWorker`：分派到 `build_file_summary` / `build_day_synthesis` / `build_week_summary` / `build_topology`
- 幂等 Job ID：SHA256(JSON{type, scope_type, scope_key, input_hash})

**媒体处理现状**:
- 文件监控：支持 .mp3/.m4a/.wav/.pdf/.jpg/.png/.mp4 等
- Chunker：为媒体文件生成 `_proxy.md`，包含 `source_anchor` 元数据
- 但**无实际 OCR/转写/识别**能力——目前仅创建空代理文件

**OCRLLM 集成机会**:
- 当 courses/ 下出现 .pdf/.mp4/.mp3 → 触发 FILE_CREATED → 可路由到 OCRLLM 处理
- 处理结果写入 proxy.md → ChunkerService 自动索引 → 进入搜索/Agent 语料库
- Job Queue 可新增 `ocrllm_process` 类型任务

---

## 二、社交媒体学习功能设计

### 2.1 功能概述

新增「社交媒体学习」模块，支持从 Bilibili、YouTube、抖音、小红书、X 等平台获取视频并识别为结构化 Markdown。

分为两条处理路径：
1. **长视频教学路径**（>10min）：B站课程（含分P）、YouTube 教学 → 下载 → 复用现有录课视频 5 阶段 Pipeline
2. **短视频知识路径**（≤10min）：知识短视频 → 下载 → TransNetV2/PySceneDetect 场景切换检测 → 自适应抽帧 → LLM 画面描述 → ASR → 合并输出

### 2.2 下载引擎选型

| 工具 | Stars | 覆盖平台 | Python API | 选型角色 |
|------|-------|----------|-----------|---------|
| **yt-dlp** | 157k | 1000+ 站点（含 B站、YouTube、抖音、X） | ✅ `yt_dlp.YoutubeDL` | 主引擎 |
| **f2** | 2.4k | 抖音/TikTok/小红书/Twitter/微博 | ✅ 异步 CLI+库 | 中国平台辅助 |

- B站分P：yt-dlp `extract_info()` 返回 `entries[]`，每个 entry 对应一个分P
- 字幕/弹幕：yt-dlp `--write-subs --write-comments` 获取
- Cookie：支持 `--cookies-from-browser` 或 `cookies.txt`
- 断点续传：yt-dlp 内置

### 2.3 短视频场景切换检测

**主方案：PySceneDetect**（纯 OpenCV，pip 直装）
- `pip install scenedetect[opencv]`
- `AdaptiveDetector` 基于内容变化自适应检测
- 可控阈值，输出时间码

**增强方案：TransNetV2**（神经网络，更高精度）
- 需 TensorFlow 或 PyTorch
- F1: 77.9-96.2 on benchmark
- 可选安装 `pip install git+https://github.com/soCzech/TransNetV2.git`

**自适应阈值逻辑**:
```
初始阈值 = 0.3
for iteration in range(8):
    scenes = detect(video, threshold)
    cuts_per_min = len(scenes) / (duration_sec / 60)
    if 目标范围内(cuts_per_min, video_type):
        break
    elif cuts_per_min > 上限:
        threshold += 0.05  # 降低灵敏度
    else:
        threshold -= 0.05  # 提高灵敏度
```

目标密度：短视频(≤2min) 10-20/min, 中视频(2-10min) 4-15/min

### 2.4 短视频帧截取策略

每两个切换点之间的片段：
- **中点帧**：`(segment_start + segment_end) / 2`
- **终点前帧**：`segment_end - 0.2s`
- 使用 `cv2.VideoCapture.set(CAP_PROP_POS_FRAMES)` 定位

### 2.5 短视频 LLM 提示词设计

与录课识别不同：
- 不使用记忆系统（`chat_with_images` 而非 `chat_with_images_contextual`）
- 侧重**画面描述**：动画、图像、精确文字、字幕内容
- 仍支持 LaTeX 数学公式，但不假设所有画面都是数学板书
- 每个 batch = 同一片段的 2 帧

### 2.6 STAv2 对接方案

**架构**：OCRLLM 作为独立 FastAPI 服务，STAv2 通过 HTTP 调用

```
STAv2 (React+FastAPI)              OCRLLM API Service
┌──────────┐                       ┌──────────────────┐
│ Frontend │◄──── WebSocket ──────►│                  │
│          │                       │ POST /process    │
│ Backend  │──── HTTP POST ───────►│ GET  /status/:id │
│ EventBus │                       │ GET  /result/:id │
│ JobQueue │                       │ POST /cancel/:id │
└──────────┘                       └──────────────────┘
     │                                      │
     └──── 共享文件系统 (WORKSPACE) ─────────┘
```

**事件流**:
1. STAv2 WatcherService 检测到 courses/ 下新文件或用户提交 URL
2. 新建 `ocrllm_process` Job → job_queue
3. JobWorker HTTP 调用 OCRLLM `/api/ocrllm/process`
4. OCRLLM 后台线程池执行处理
5. STAv2 轮询 `/api/ocrllm/status/{task_id}` 获取进度
6. 完成后 OCRLLM 将 .md 写入指定路径
7. STAv2 WatcherService 检测到新文件 → ChunkerService 索引

---

## 三、实施计划

### 新建文件
| 文件 | 用途 |
|------|------|
| `processors/social/__init__.py` | 社交媒体处理模块 |
| `processors/social/downloader.py` | 统一下载引擎 (yt-dlp + f2) |
| `processors/social/platform_router.py` | URL→平台路由 |
| `processors/social/long_video.py` | 长视频处理器 |
| `processors/social/short_video.py` | 短视频处理器 |
| `imaging/shot_detector.py` | 场景切换检测 + 自适应阈值 |
| `core/short_video_merge.py` | 短视频识别结果合并 |
| `api/__init__.py` + `api/server.py` | OCRLLM FastAPI 服务 |

### 修改文件
| 文件 | 变更 |
|------|------|
| `config.py` | 新增 `SocialConfig` + `ShotDetectionConfig` |
| `prompts.py` | 新增 `SHORT_VIDEO_RECOGNIZE` 模板 |
| `processors/registry.py` | 注册 `social_long` + `social_short` 处理器 |
| `processors/routing.py` | URL 输入路由支持 |
| `core/document_model.py` | 新增 `SourceType.SOCIAL_VIDEO` |
| `requirements.txt` | 新增 yt-dlp, scenedetect, fastapi, uvicorn |
