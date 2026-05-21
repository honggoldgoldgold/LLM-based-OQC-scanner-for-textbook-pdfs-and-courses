# gui/ — PyQt5 图形界面

基于 PyQt5 的课程识别 GUI。

## 文件说明

| 文件 | 说明 |
|------|------|
| `app.py` | **主窗口** (`QCRMainWindow`) — 顶层 GUI 入口。包含 API 设置面板、进度追踪面板（进度条 + 阶段信息）、断点续传提示、4 个处理 Tab、运行日志面板。支持拖放文件自动路由到对应 Tab。 |
| `widgets.py` | **可复用组件** — `FileInput` (支持拖放和扩展名过滤的文件输入框)、`browse_file` / `browse_files` (文件选择对话框辅助函数)。 |
| `worker.py` | **后台任务 Worker** (`GuiWorker`) — QThread 后台执行 + ProgressReporter 协作取消 + Qt 信号桥梁。不使用 `QThread.terminate()`，通过 `CancelledError` 安全退出。定时轮询 `ProgressTracker` 更新人类友好进度。 |

### tabs/ — 选项卡子目录

| 文件 | 说明 |
|------|------|
| `pdf_tab.py` | **PDF Tab** — PDF 文件选择、公式模式开关、页码范围、提示词编辑。 |
| `board_tab.py` | **板书 Tab** — 多图片选择（拖放/对话框）、跳过预处理选项、提示词编辑。 |
| `video_tab.py` | **视频 Tab** — 视频文件选择、5 阶段勾选、提示词编辑。 |
| `audio_tab.py` | **音频 Tab** — 音频文件选择、热词输入（手动/文件导入）、提示词编辑。 |

## 线程安全架构

```
主线程 (GUI)                    工作线程 (QThread)
    │                               │
    ├─ start(task_func)──────→ _WorkerThread.run()
    │                               │
    │  ← progress signal ──── reporter.progress()
    │  ← content signal ───── reporter.content()
    │  ← log signal ────────── reporter.log()
    │                               │
    ├─ cancel() ───→ reporter._cancelled.set()
    │                               │
    │                          check_cancelled() → CancelledError
    │                               │
    │  ← finished_ok signal ── return "完成"
    │  ← finished_err signal ─ raise Exception
    │  ← done signal ─────────(cleanup)
```
