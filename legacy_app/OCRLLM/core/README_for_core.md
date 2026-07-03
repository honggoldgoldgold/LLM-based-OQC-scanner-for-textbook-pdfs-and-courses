# core/ — 核心基础设施

与具体文件格式无关的底层服务模块。所有处理器共用这些基础组件。

## 文件说明

| 文件 | 说明 |
|------|------|
| `api_pool.py` | **API 池** — 多 API Key 负载均衡，付费模式下 N 个 key 并行工作。线程安全的 acquire/release 模型。 |
| `board_merge.py` | **板书合并** — 对录课视频多帧识别结果进行保守去重合并。使用精确匹配 + SequenceMatcher 模糊匹配，按时间 gap 分段。 |
| `checkpoint.py` | **断点续传** — JSON 文件持久化任务进度（已完成批次索引）。支持 PDF 和视频两种长任务的中断恢复。 |
| `document_model.py` | **统一文档模型** — `UnifiedDocument` / `Section` / `Block` / `Asset` 四层结构，将不同输入格式归一到统一中间表示。 |
| `incremental_writer.py` | **增量写入器** — 线程安全的 Markdown 写入器，支持乱序插入（slot-based），原子性全量 flush。 |
| `llm_client.py` | **LLM 客户端** — OpenAI 兼容接口封装。支持文本、图像、短音频三种模态。内置流式/非流式回退、指数退避重试、协作取消。 |
| `progress_tracker.py` | **进度追踪器** — 线程安全的多阶段进度管理。GUI 定时轮询获取人类友好的状态消息和百分比。 |
| `task_runner.py` | **任务执行器** — `ProgressReporter` 提供进度回调和协作式取消 (`CancelledError`)。连接处理器与 GUI/CLI。 |
| `utils.py` | **工具函数** — 无状态纯函数集：目录创建、图片缩放、列表分批、Markdown 清理、ffmpeg 查找、子进程管理等。 |

## 依赖关系

```
task_runner.py (无外部依赖)
    ↑
llm_client.py → openai, httpx
    ↑
api_pool.py → llm_client
    ↑
checkpoint.py (无外部依赖)
incremental_writer.py (无外部依赖)
progress_tracker.py (无外部依赖)
utils.py → PIL, subprocess
board_merge.py → difflib
document_model.py (纯数据类)
```
