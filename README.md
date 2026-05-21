# OCRLLM

OCRLLM 是一个面向课程场景的多模态识别工具包，重点针对 PDF 课本、讲义图片和板书照片输出高保真 Markdown。它使用阿里云 DashScope / 百炼（BaiLian）控制台对应的兼容 API 与 Qwen 系列模型，把公式、表格、标题层级和阅读顺序尽量稳定地还原出来，尤其适合数学内容密集的 PDF 和 JPG / PNG 输入。

它同时提供 GUI、CLI 和 FastAPI 服务，适合本地批量处理，也适合被外部系统调用。

## 精准输出

| 输入类型 | 典型格式 | 主要输出 | 说明 |
|---|---|---|---|
| PDF 课本 / 讲义 | `.pdf` | Markdown | 支持 OCR 模式和公式模式；公式、表格和段落顺序尽量保留 |
| 讲义照片 / 板书截图 | `.jpg .jpeg .png .bmp .webp .heic .heif .tif .tiff` | Markdown | 支持多图上下文、预处理和合并去重，适合手拍板书与截图 |
| 录课视频 | `.mp4 .avi .mkv .mov .flv .wmv` | Markdown + 热词表 | 抽帧、板书识别和语音转写会同时输出 |
| 音频文件 | `.wav .mp3 .m4a .aac .flac .ogg .opus .wma` | Markdown | 短音频走同步 ASR，长音频走异步 filetrans |

对 PDF 和图片场景，项目会尽量把表格保持成 Markdown 表格，把公式保持成可读的数学标记，而不是只返回一大段打散文本。

## 新工具

- 统一模型目录 `core/model_catalog.py`，把视觉 / 音频模型、免费额度标记和自定义模型持久化集中管理。
- GUI 模型选择器支持搜索、分类过滤和“测试并添加”，自定义模型通过真实样本验证后写入 `~/.OCRLLM/user_models.json`。
- GUI 批处理模块支持 PDF、图片、视频和音频的多文件并行执行。
- CLI 由处理器注册表驱动，支持 `auto` 自动路由和严格参数校验。
- FastAPI 服务暴露健康检查、任务提交、任务状态、结果获取、取消和任务列表接口。
- 社交媒体下载链路支持短视频和长视频 URL 的识别、下载和后续内容整理。
- 检查点恢复和增量写入机制用于长任务断点续跑。

## 设计特点

- 处理器注册表驱动的路由与 CLI 参数生成。
- 增量写入与检查点机制，适合长任务中断后恢复。
- GUI、CLI、API 共用同一套处理器与配置系统。
- 支持多 API Key 负载均衡、并发控制和任务限流。
- 支持短视频 / 社交平台链接下载后再识别。

## 安装

推荐使用 Conda 环境。

```bash
conda env create -f environment.yml
conda activate OCRLLM
```

如果你不用 Conda，也可以直接安装依赖：

```bash
pip install -r requirements.txt
```

## 配置

最少需要设置阿里云百炼控制台里生成的 DashScope API Key：

```bash
set DASHSCOPE_API_KEY=your_key_here
```

常用环境变量还包括：

- `DASHSCOPE_BASE_URL`
- `DASHSCOPE_API_KEY`
- `OCRLLM_MAX_CONCURRENT_TASKS`
- `OCRLLM_TASK_RETENTION_SECONDS`
- `OCRLLM_TASK_MAX_HISTORY`

默认输出目录和临时目录由 `config.py` 管理，默认会写到仓库内的 `output/` 和 `temp/`。

## 运行

说明：仓库根目录本身就是 Python 包 `OCRLLM`。下面所有 `python -m OCRLLM...` 命令，都要在“包含 OCRLLM 文件夹的上一级目录”里执行。

### GUI

在 Windows 上最简单的方式是直接运行：

```bash
start.bat
```

或者在仓库根目录执行：

```bash
python main.py
```

### CLI

```bash
python -m OCRLLM.cli pdf input.pdf --formula
python -m OCRLLM.cli board img1.jpg img2.png
python -m OCRLLM.cli video lecture.mp4 --phases 1 2 3 4 5
python -m OCRLLM.cli audio lecture.mp3 --hotwords "矩阵,sigma"
python -m OCRLLM.cli auto input_file
```

### FastAPI 服务

```bash
uvicorn OCRLLM.api.server:app --host 0.0.0.0 --port 8000
```

## 目录结构

- `cli.py`：命令行入口，按文件类型自动路由到对应处理器。
- `main.py`：PyQt5 图形界面入口。
- `api/`：FastAPI 服务层，供外部系统调用。
- `core/`：LLM 客户端、进度追踪、检查点、增量写入等基础设施。
- `imaging/`：PDF 渲染、OCR、预处理、音频提取等底层能力。
- `processors/`：PDF、板书、视频、音频和文档格式处理器。
- `gui/`：GUI 主窗口、组件和各个处理 Tab。

更细的说明可以看：

- [Architecture.md](Architecture.md)
- [core/README_for_core.md](core/README_for_core.md)
- [gui/README_for_gui.md](gui/README_for_gui.md)
- [imaging/README_for_imaging.md](imaging/README_for_imaging.md)
- [processors/README_for_processors.md](processors/README_for_processors.md)

## 版本

当前版本：`2.0.0`

## 维护

当前维护者：honggoldgoldgold
