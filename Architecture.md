# OCRLLM 架构文档

> **OCRLLM** - 基于阿里云 DashScope / 百炼（BaiLian）兼容 API 的课程内容识别工具包
> 版本: 2.0.0 | Python 3.10+ | Windows / Linux

## 1. 项目定位

OCRLLM 的目标很直接：把 PDF 课本、讲义图片、板书照片、录课视频、音频文件和社交媒体视频链接，转换成结构清晰的 Markdown。

它针对两类内容做了加强：

- 数学公式密集的 PDF / JPG / PNG 输入，尽量保留公式、表格、标题和段落顺序。
- 长任务场景，支持检查点、增量写入、断点续传和并发控制。

阿里云侧通过 DashScope / 百炼控制台提供 API Key，运行时使用兼容模式接入 Qwen 视觉、文本和 ASR 能力。

### 支持的输入类型

| 类型 | 格式 | 处理器 key | 输出 |
|------|------|------------|------|
| PDF 课本 / 课件 | `.pdf` | `pdf` | Markdown |
| 板书 / 截图 | `.jpg .jpeg .png .bmp .webp .heic .heif .tif .tiff` | `board` | Markdown |
| 录课视频 | `.mp4 .avi .mkv .mov .flv .wmv` | `video` | Markdown + 热词表 |
| 语音文件 | `.wav .mp3 .m4a .aac .flac .ogg .opus .wma` | `audio` | Markdown |
| DOCX / PPTX / DOC / PPT / HTML | `.docx .pptx .doc .ppt .html .htm` | `docx / pptx / doc / ppt / html` | Markdown |
| 社交媒体长视频 | URL | `social_long` | Markdown + 资源目录 |
| 社交媒体短视频 | URL | `social_short` | Markdown + 资源目录 |

HTML 当前仍是实验性占位处理器，其余文档格式主要做文本抽取，不依赖 API Key。

## 2. 代码入口

### main.py

PyQt5 GUI 入口。支持 `--spawn N` 启动多个独立窗口进程，适合多个任务窗口并行工作。

### cli.py

命令行入口。它不再用硬编码分支，而是读取处理器注册表生成子命令和参数约束，并支持 `auto` 自动路由。

### api/server.py

FastAPI 服务层。它把 OCRLLM 处理能力包装成有界后台任务，供外部系统调用。

## 3. 配置与模型目录

### AppConfig

配置采用嵌套 dataclass：

- `api`：DashScope API Key、base URL、付费模式和多 key 列表。
- `models`：视觉、文本、长音频、短音频模型名。
- `processing`：批大小、DPI、图片质量等。
- `concurrency`：渲染、LLM 并行请求、音频拆分、ASR 并发等。
- `paths`：输出目录和临时目录。
- `video`：抽帧、变化检测、pHash 去重、板书 ROI。
- `social`：下载格式、cookie、评论和弹幕抓取、B 站清晰度。
- `shot_detection`：短视频场景切换检测阈值。

运行时通过 `with_updates()` 生成新实例，不修改全局单例状态。

### 模型目录

`core/model_catalog.py` 是视觉和音频模型的单一来源。

- 视觉模型按 `vlm`、`ocr`、`omni`、`general` 分类。
- 音频模型按 `asr_long`、`asr_short`、`omni_audio` 分类。
- 每个 builtin 条目都带有 `free_quota`、`max_images` 或 `max_seconds` 元数据。
- 用户自定义模型会持久化到 `~/.OCRLLM/user_models.json`。

GUI 的模型选择器和模型校验对话框都基于这个目录工作。

## 4. 处理器注册表与路由

### ProcessorSpec

`processors/registry.py` 用 `ProcessorSpec` 统一描述处理器元数据：

- `key`、`display_name`、`module_path`、`class_name`
- `supported_extensions`
- `source_type`、`input_kind`
- `accepts_multiple_files`
- `supports_resume`
- `output_target`
- CLI 帮助文本和可选参数组

### 注册表驱动

注册表现在负责三件事：

1. 自动创建处理器实例。
2. 给 CLI 生成子命令。
3. 给输入路由和 GUI 批处理提供统一能力描述。

内置处理器包括：

- `pdf`
- `board`
- `video`
- `audio`
- `pptx`
- `ppt`
- `docx`
- `doc`
- `html`
- `social_long`
- `social_short`

### 路由规则

`processors/routing.py` 支持本地文件和社交媒体 URL：

- 本地文件按扩展名路由。
- 单个 URL 会先识别是否为社交媒体链接。
- 社交媒体链接会根据平台和时长自动进入 `social_long` 或 `social_short`。
- 多文件输入只允许同类文件混合，且要满足处理器是否支持多文件。

## 5. 核心处理管线

### 5.1 PDF 管线

PDF 处理以 `processors/pdf.py` 为中心，走两条路径：

- OCR 模式：PyMuPDF 并行渲染页面，再用 RapidOCR + TBPU 排版恢复成 Markdown。
- 公式模式：把页面转成图片后走多模态模型识别，适合公式和复杂表格。

关键配套组件：

- `core/incremental_writer.py`：增量写入，支持乱序到达、按序落盘。
- `core/checkpoint.py`：保存批次完成状态和恢复元信息。
- `imaging/pdf_renderer.py`：并行渲染 PDF 页面。
- `imaging/ocr_engine.py`：RapidOCR ONNX Runtime 封装。
- `imaging/tbpu.py`：文本排版恢复。

### 5.2 板书 / 截图管线

`processors/board.py` 用于单张或多张图片输入：

- 先做图像预处理和裁剪。
- 再把多图按上下文顺序送入视觉模型。
- 最终经 `core/board_merge.py` 合并去重，减少重复行和重复段落。

这一条管线最适合手拍板书、课堂投屏截图、题目页照片。

### 5.3 录课视频管线

`processors/video.py` 和 `processors/video_pipeline.py` 定义了五阶段流程：

1. 音频提取。
2. 智能抽帧和变化检测。
3. 帧预处理。
4. 板书 / 课件视觉识别。
5. 语音识别。

抽帧阶段会结合变化阈值、漂移阈值、pHash 去重和目标帧率调节，避免纯均匀采样浪费成本。

### 5.4 社交媒体视频管线

`processors/social/` 是新增的上层链路，覆盖短视频和长视频 URL：

- `downloader.py` 负责平台识别、下载和元数据收集。
- `platform_router.py` 负责长短视频分类。
- `short_video.py` 负责短视频场景切换检测、画面描述和 ASR。
- `long_video.py` 复用录课视频的长管线做下载后处理。

这条链路是对短视频内容和课程分享链接的补充，不是单纯的视频文件识别。

### 5.5 音频管线

`processors/audio.py` 会根据时长选择：

- 短音频：同步 ASR。
- 长音频：DashScope filetrans 异步任务。

这条路径支持热词，并在长音频失败时预留回退策略。

### 5.6 文档抽取管线

`processors/future_formats.py` 覆盖 DOCX / PPTX / DOC / PPT / HTML 文本抽取。

这些处理器主要用于把文本提出来，不参与图像或多模态识别链路。

## 6. GUI 架构

GUI 以 `gui/app.py` 为主窗口，围绕四个处理 Tab 展开：PDF、板书、视频、音频。

### 批处理

`gui/batch_tasks.py` 负责同类型多文件并行执行：

- PDF、图片、视频、音频都能批量跑。
- 并发预算会按任务数分摊。
- 批任务会共享一个缩减后的配置，避免把 LLM 并发和渲染线程挤爆。

### 模型选择

`gui/model_picker.py` 和 `gui/model_validator.py` 解决大模型数量变多后的选择问题：

- 支持搜索和类型过滤。
- 支持自定义模型测试通过后写入用户清单。
- 视觉模型用本地样图探测。
- 音频模型按短音频或长音频场景走不同校验路径。

### 后台执行

`gui/worker.py` 提供 QThread 后台执行、协作取消和 Qt 信号回传。

整个 GUI 不直接阻塞主线程，进度和内容输出都走 `ProgressReporter`。

## 7. FastAPI 服务

`api/server.py` 暴露了这组接口：

| 路径 | 作用 |
|------|------|
| `/api/health` | 健康检查 |
| `/api/ocrllm/process` | 提交任务 |
| `/api/ocrllm/status/{task_id}` | 查询状态 |
| `/api/ocrllm/result/{task_id}` | 获取结果 |
| `/api/ocrllm/cancel/{task_id}` | 取消任务 |
| `/api/ocrllm/tasks` | 列出任务 |

这个服务层是有界的：

- 有最大并发任务数。
- 有任务保留时长和历史长度限制。
- 会把全局并发预算按任务数量切分。

## 8. 数据流与目录

### 输出目录

默认输出和临时目录由 `config.py` 初始化，通常是：

- `output/`
- `temp/`
- `.checkpoints/`（具体文件随处理器而定）

### 产物形态

- PDF / 图片 / 视频 / 音频通常都会产出 Markdown。
- 视频和社交视频通常还会额外保存热词表、帧信息和中间资源目录。
- 自定义模型清单保存在用户主目录下，不污染仓库本体。

## 9. 外部依赖

| 依赖 | 用途 |
|------|------|
| `openai` | DashScope 兼容 API 客户端 |
| `dashscope` | 阿里云百炼 / DashScope 相关能力 |
| `httpx` | 底层 HTTP 客户端 |
| `PyMuPDF` | PDF 渲染 |
| `rapidocr_onnxruntime` | 本地 OCR |
| `onnxruntime` | OCR 推理后端 |
| `opencv-python` | 图像处理、抽帧、检测 |
| `numpy` | 数组处理 |
| `PyQt5` | GUI |
| `imageio-ffmpeg` | ffmpeg 拉取与调用 |
| `pydub` | 音频辅助处理 |
| `yt-dlp`、`curl_cffi` | 社交媒体下载 |
| `fastapi`、`uvicorn` | API 服务 |

## 10. 运行方式

```bash
# GUI
python -m OCRLLM.main

# CLI
python -m OCRLLM.cli pdf input.pdf --formula
python -m OCRLLM.cli board img1.jpg img2.jpg
python -m OCRLLM.cli video lecture.mp4 --phases 1 2 3 4 5
python -m OCRLLM.cli audio lecture.mp3 --hotwords "矩阵,sigma"
python -m OCRLLM.cli auto input_file

# API
uvicorn OCRLLM.api.server:app --host 0.0.0.0 --port 8000
```

## 11. 这版架构的关键变化

- 模型选择已经从单个下拉框演化成模型目录 + 校验机制。
- CLI 和路由已经由注册表驱动，不再依赖写死分支。
- 视频处理已拆成可恢复的阶段管线。
- 社交视频 URL 已成为正式输入类型。
- API 层从简单调用包装成有界任务服务。
- GUI 批处理和后台 worker 已经成为独立模块，而不是主窗口里的附属逻辑。
