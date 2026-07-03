# OCRLLM v3 — Rust 核心 + Python 模块 架构设计

> **状态**: 设计阶段，尚未实现
> **上一版**: v2.0.0（纯 Python，PyQt5 GUI，见 git 历史 `master` 分支）
> **目标**: 将核心管线迁入 Rust，通过 PyO3/maturin 编译为 Python 原生扩展；
>         剥离 GUI 和设置页，保留极简 Python API。

---

## 0. 设计约束与前置决策

### 0.1 失忆症友好的代码组织

开发者的工作模式是间断的：每次续写都需要重读之前写的代码。因此：

- **每个 `.rs` 文件目标 80–250 行**，绝对上限 400 行。
- **文件名即模块职责**：无需跳转即可从路径推断内容。
- **每个模块顶部有 3–5 行注释说明"我依赖谁、我被谁依赖"**。
- **trait 先于实现**：所有公开接口定义在独立的 `*_trait.rs` 或模块顶部的 trait 块中，
  实现放在 `*_impl.rs` 中。读代码时先读 trait，再读 impl。
- **测试和模块同文件**（Rust 的 `#[cfg(test)] mod tests`），不需要跨文件追踪测试。
- **最小认知负荷**：每个模块只暴露 1–3 个公开类型/函数。私有辅助函数不超过 5 个。

### 0.2 明确不做的事

| 不做的事 | 原因 |
|----------|------|
| GUI（PyQt5 窗口） | 纯库，无 UI |
| 设置对话框 | 配置走 env + 代码参数 |
| 社交媒体下载 | 暂不迁移，预留 Python 侧扩展点 |
| FastAPI 服务层 | 调用方自己包装（太简单，不值得进核心） |
| HTML 处理器 | v2 中已是实验性占位，v3 删除 |
| 批处理 GUI 逻辑 | 库使用者自己写循环 |

### 0.3 PDF 渲染的独立化

PDF 渲染器不作为核心库的一部分。原因：
- PyMuPDF 是 C 库的 Python binding，Rust 侧没有同等成熟的替代。
- 用户可能自研高效/低清晰度渲染器。
- PDF → 图片 这一步本质上是一个**外部依赖的独立问题**。

**架构决策**：定义 `PageRenderer` trait，PDF 处理器依赖 trait 而非具体实现。
默认提供一个基于 `mupdf` crate 的参考实现。用户可以替换为自己的渲染器。

---

## 1. 模块全景图

```text
ocrllm/                          # Python 包根目录
│
├── pyproject.toml               # maturin 构建配置
├── Cargo.toml                   # Rust 依赖
│
├── src/                         # ─── Rust 源码 ───
│   ├── lib.rs                   # PyO3 入口，注册 Python 可调用的类/函数
│   ├── error.rs                 # 统一错误类型 (thiserror)
│   ├── config.rs                # 配置结构体 (serde)
│   │
│   ├── catalog/                 # 模型目录
│   │   ├── mod.rs               #   模块入口 + 合并查询
│   │   ├── model.rs             #   VisionModel / AudioModel 类型
│   │   ├── builtin.rs           #   内置模型常量
│   │   └── cache.rs             #   模型缓存持久化 (~/.ocrllm/)
│   │
│   ├── api/                     # LLM API 客户端
│   │   ├── mod.rs               #   模块入口
│   │   ├── provider.rs          #   LlmProvider trait（统一接口）
│   │   ├── dashscope.rs         #   百炼/DashScope 实现
│   │   ├── openai_compat.rs     #   OpenAI 兼容 Provider 实现
│   │   ├── google.rs            #   Google Gemini REST 实现
│   │   ├── retry.rs             #   重试/退避/免费额度 fallback
│   │   └── pool.rs              #   多 Key 池化（付费模式）
│   │
│   ├── imaging/                 # 图像处理（纯函数，无 IO）
│   │   ├── mod.rs               #   模块入口
│   │   ├── resize.rs            #   等比缩放
│   │   ├── preprocess.rs        #   Canny 边缘 + 自动裁剪
│   │   └── ocr.rs               #   ONNX OCR 引擎封装 (ort crate)
│   │
│   ├── media/                   # 音视频处理
│   │   ├── mod.rs               #   模块入口
│   │   ├── ffmpeg.rs            #   ffmpeg/ffprobe 查找与调用
│   │   ├── audio_split.rs       #   音频切片与窗口构建
│   │   ├── video_frame.rs       #   视频抽帧 + 变化检测 + pHash
│   │   └── extract_audio.rs     #   从视频提取音轨
│   │
│   ├── pipeline/                # 处理器管线
│   │   ├── mod.rs               #   模块入口 + 路由
│   │   ├── processor.rs         #   Processor trait（统一接口）
│   │   ├── registry.rs          #   处理器注册表
│   │   ├── pdf.rs               #   PDF 处理器
│   │   ├── board.rs             #   板书/截图处理器
│   │   ├── video/               #   视频处理器（5 阶段）
│   │   │   ├── mod.rs           #     模块入口 + VideoProcessor
│   │   │   ├── phase.rs         #     VideoPhase trait
│   │   │   ├── phase1_extract_audio.rs
│   │   │   ├── phase2_extract_frames.rs
│   │   │   ├── phase3_preprocess.rs
│   │   │   ├── phase4_llm_recognize.rs
│   │   │   └── phase5_asr.rs
│   │   ├── audio.rs             #   音频处理器
│   │   └── office.rs            #   DOCX/PPTX 文本抽取
│   │
│   └── util/                    # 工具模块
│       ├── mod.rs               #   模块入口
│       ├── checkpoint.rs        #   检查点持久化
│       ├── writer.rs            #   增量 Markdown 写入器
│       ├── board_merge.rs       #   板书去重合并
│       ├── progress.rs          #   进度报告通道
│       └── md_fence.rs          #   Markdown 清理（去围栏、标准化）
│
├── python/                      # ─── 纯 Python 层 ───
│   └── ocrllm/
│       ├── __init__.py          # 顶层 facade: recognize(), list_models()
│       ├── py.typed             # PEP 561 marker
│       └── pdf_render.py        # PageRenderer 的 Python 参考实现 (PyMuPDF)
│
└── tests/                       # ─── 测试 ───
    ├── rust/                    # Rust 集成测试 (Cargo test)
    └── python/                  # Python 端测试 (pytest)
```text

**总行数估算**：Rust ~6000–7000 行，Python ~300 行（仅 facade + pdf_render）。

---

## 2. 依赖关系图（严格分层）

```text
                  ┌─────────────────────────┐
                  │     python/ocrllm/      │  ← 纯 Python facade
                  │   __init__.py           │
                  └───────────┬─────────────┘
                              │ import (PyO3)
                  ┌───────────▼─────────────┐
                  │     src/lib.rs          │  ← PyO3 绑定层
                  └───────────┬─────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
  ┌───────▼──────┐   ┌───────▼──────┐   ┌───────▼──────┐
  │   pipeline/  │   │    api/      │   │   catalog/   │
  │ (处理器)     │   │ (LLM 客户端) │   │ (模型目录)   │
  └───────┬──────┘   └──────────────┘   └──────────────┘
          │
  ┌───────┼───────┐
  │       │       │
  │ ┌─────▼──┐ ┌──▼──────┐
  │ │imaging/│ │ media/  │
  │ │(图像)  │ │(音视频) │
  │ └────────┘ └─────────┘
  │
  ┌▼──────────┐
  │  util/    │
  │ (工具)    │
  └───────────┘
```

**规则**：
- 下层不能 import 上层（`util` 不知道 `pipeline` 的存在）
- `pipeline` 依赖 `api` + `imaging` + `media` + `util`
- `api` 只依赖 `catalog` + `config` + `error`
- `imaging` 和 `media` 只依赖 `util` + `error`
- `catalog` 只依赖 `config` + `error`

---

## 3. 核心 trait 设计

### 3.1 `LlmProvider` — 统一 LLM 接口

```rust
// src/api/provider.rs

#[async_trait]
pub trait LlmProvider: Send + Sync {
    /// 发送图片+文本多模态请求，返回识别文本
    async fn chat_with_images(
        &self,
        model: &str,
        prompt: &str,
        image_paths: &[PathBuf],
    ) -> Result<String, Error>;

    /// 发送纯文本请求
    async fn chat_text(
        &self,
        model: &str,
        prompt: &str,
        system_prompt: Option<&str>,
    ) -> Result<String, Error>;

    /// 短音频 ASR（同步，≤5 分钟）
    async fn transcribe_short(
        &self,
        model: &str,
        audio_path: &Path,
        hotwords: &[String],
    ) -> Result<String, Error>;

    /// 长音频 ASR（异步 filetrans 提交+轮询）
    async fn transcribe_long(
        &self,
        model: &str,
        audio_url: &str,
        hotwords: &[String],
    ) -> Result<String, Error>;

    /// 探测模型可用性
    async fn probe_vision(&self, model: &str, image_path: &Path) -> Result<ProbeResult, Error>;
    async fn probe_audio(&self, model: &str, audio_path: &Path) -> Result<ProbeResult, Error>;
}
```

三种实现：`DashscopeProvider`、`OpenAiCompatProvider`、`GoogleProvider`。
每个实现在自己的文件中（≤300 行），共享 `retry.rs` 的重试逻辑。

### 3.2 `Processor` — 统一处理器接口

```rust
// src/pipeline/processor.rs

pub struct ProcessInput {
    pub paths: Vec<PathBuf>,
    pub output_dir: Option<PathBuf>,
    pub config: ProcessConfig,  // 处理器特定参数
}

pub struct ProcessOutput {
    pub markdown: String,
    pub output_path: PathBuf,
    pub hotwords: Vec<String>,
    pub metadata: HashMap<String, String>,
}

#[async_trait]
pub trait Processor: Send + Sync {
    /// 处理器标识 key（如 "pdf"、"video"）
    fn key(&self) -> &'static str;

    /// 支持的扩展名
    fn extensions(&self) -> &'static [&'static str];

    /// 是否支持多文件输入
    fn accepts_multiple(&self) -> bool;

    /// 是否支持断点续传
    fn supports_resume(&self) -> bool;

    /// 执行处理，返回结果
    async fn process(
        &self,
        input: ProcessInput,
        provider: &dyn LlmProvider,
        progress: &dyn ProgressSink,
    ) -> Result<ProcessOutput, Error>;
}
```

### 3.3 `PageRenderer` — PDF 渲染抽象

```rust
// src/pipeline/pdf.rs 顶部

/// 将 PDF 页面渲染为图片。独立 trait，便于替换实现。
#[async_trait]
pub trait PageRenderer: Send + Sync {
    /// 渲染指定页面范围，返回图片路径列表
    async fn render_pages(
        &self,
        pdf_path: &Path,
        pages: Range<u32>,
        dpi: u32,
        output_dir: &Path,
    ) -> Result<Vec<PathBuf>, Error>;

    /// 返回 PDF 总页数
    fn page_count(&self, pdf_path: &Path) -> Result<u32, Error>;
}
```

默认实现放在 `python/ocrllm/pdf_render.py`（通过 PyO3 回调），用户可替换。

### 3.4 `ProgressSink` — 进度报告

```rust
// src/util/progress.rs

pub trait ProgressSink: Send + Sync {
    fn report(&self, current: u32, total: u32, message: &str);
    fn report_content(&self, text: &str, label: &str);
    fn is_cancelled(&self) -> bool;
}
```

CLI 用打印版实现，Python 侧用回调版实现（PyO3 把信号传回 Python）。

---

## 4. 配置设计

### 4.1 原则

- **默认值即生产可用**：80% 用户不需要改任何配置。
- **环境变量覆盖**：`OCRLLM_API_KEY`、`OCRLLM_MODEL` 等。
- **代码覆盖**：`recognize(path, config=Config { model: "...", ..Default::default() })`。
- **不持久化密钥到文件**：密钥只在内存中，来自 env 或参数。

### 4.2 Config 结构体

```rust
// src/config.rs

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Config {
    /// API 提供商：dashscope / openai_compat / google
    #[serde(default = "default_provider")]
    pub provider: String,  // "dashscope"

    /// DashScope / 百炼 API Key
    pub api_key: String,   // 来自 DASHSCOPE_API_KEY env

    /// DashScope Base URL
    #[serde(default = "default_dashscope_url")]
    pub base_url: String,

    /// 视觉模型 ID
    #[serde(default = "default_vision_model")]
    pub vision_model: String,

    /// 长音频 ASR 模型 ID
    #[serde(default = "default_asr_model")]
    pub asr_model: String,

    /// 短音频 ASR 模型 ID
    #[serde(default = "default_asr_short_model")]
    pub asr_short_model: String,

    // ── 以下参数有稳定默认值，极少需要修改 ──

    /// 并行 LLM 请求数
    #[serde(default = "default_parallel")]
    pub parallel_requests: u32,  // 15

    /// 图片最大边长（超限自动缩放）
    #[serde(default = "default_max_side")]
    pub image_max_side: u32,     // 2048

    /// 视觉批大小（一次请求送几张图）
    #[serde(default = "default_batch_size")]
    pub batch_size: u32,         // 10

    /// PDF 渲染 DPI
    #[serde(default = "default_dpi")]
    pub pdf_dpi: u32,            // 200

    /// 输出目录
    pub output_dir: Option<PathBuf>,

    /// 临时目录
    pub temp_dir: Option<PathBuf>,

    // ── Google Gemini 相关（仅在 provider="google" 时生效）──
    pub google_api_key: Option<String>,
    pub google_vision_model: Option<String>,
    pub google_audio_model: Option<String>,

    // ── 付费模式多 Key ──
    pub extra_api_keys: Vec<String>,

    // ── 视频抽帧参数（稳定默认值）──
    pub video_frame_interval: f64,     // 5.0 秒
    pub video_change_threshold: f64,   // 0.15
    pub video_max_segment_sec: f64,    // 150.0
    pub video_phash_threshold: u32,    // 3

    // ── 音频切片参数 ──
    pub audio_chunk_seconds: u32,      // 1740 (29 分钟)
    pub audio_overlap_seconds: u32,    // 30
    pub audio_asr_parallel: u32,       // 4
}
```

**注意**：config.rs 约 200 行，包含 `Default` 实现、env 加载、以及 `with_*` builder 方法。
不会膨胀成 v2 的 380 行——因为没有 `from_env` 的逐个字段复制样板（serde + envy crate 替代）。

---

## 5. 错误处理

```rust
// src/error.rs

#[derive(Debug, thiserror::Error)]
pub enum Error {
    #[error("配置错误: {0}")]
    Config(String),

    #[error("API 错误 (provider={provider}, model={model}): {message}")]
    Api {
        provider: String,
        model: String,
        message: String,
        #[source]
        source: Option<Box<dyn std::error::Error + Send + Sync>>,
    },

    #[error("免费额度耗尽 (provider={provider}, model={model})")]
    QuotaExhausted { provider: String, model: String },

    #[error("模型返回空响应 (model={model})")]
    EmptyResponse { model: String },

    #[error("网络错误: {0}")]
    Network(#[from] reqwest::Error),

    #[error("IO 错误: {0}")]
    Io(#[from] std::io::Error),

    #[error("ffmpeg 不可用: {0}")]
    Ffmpeg(String),

    #[error("文件格式不支持: {0}")]
    UnsupportedFormat(String),

    #[error("任务已取消")]
    Cancelled,

    #[error("检查点损坏: {0}")]
    Checkpoint(String),

    #[error("{0}")]
    Other(String),
}
```

**对比 v2**：v2 有 85 处裸 `except Exception`；v3 每个错误都有类型，调用方必须显式处理。

---

## 6. Python 公共 API

### 6.1 顶层 facade

```python
# python/ocrllm/__init__.py

from ocrllm._core import (   # _core 是 Rust 编译出的 .pyd/.so
    Config,
    ProcessInput,
    ProcessOutput,
    recognize,
    list_vision_models,
    list_audio_models,
    probe_vision_model,
    probe_audio_model,
)

__version__ = "3.0.0"

# 便捷函数
def recognize(           # 自动路由，一键处理
    source: str | Path | list[str | Path],
    *,
    config: Config | None = None,
    output_dir: str | Path | None = None,
    model: str | None = None,
) -> ProcessOutput: ...

def list_models(kind: str = "vision") -> list[ModelInfo]: ...

def probe_model(model: str, kind: str = "vision") -> tuple[bool, str]: ...
```

**目标**：Python 用户只需 3 个函数就能完成所有操作。

### 6.2 使用示例

```python
# 最简用法：自动识别文件类型，用默认模型处理
from ocrllm import recognize

result = recognize("lecture.mp4")
print(result.markdown[:500])

# 指定模型和输出目录
result = recognize(
    "textbook.pdf",
    model="qwen3-vl-plus",
    output_dir="./out",
)

# 自定义配置
from ocrllm import Config, recognize

cfg = Config(
    api_key="sk-xxx",
    provider="dashscope",
    vision_model="qwen-vl-max",
    parallel_requests=8,
    batch_size=5,
)
result = recognize("board_shots/", config=cfg)
```

---

## 7. 关键差异：v2 (Python) → v3 (Rust)

### 7.1 缓存管理

| 项目 | v2 (Python) | v3 (Rust) |
|------|------------|-----------|
| 模型清单缓存 | `~/.OCRLLM/user_models.json` 手动读写 | `dirs::cache_dir()/ocrllm/models.json` + 自动过期 |
| 检查点 | `output/.checkpoints/` 手动 JSON | 同位置，但用 `serde_json` + 原子写入 |
| 临时文件 | `temp/` 手动清理 | `tempfile` crate 自动清理（Drop 时删除） |
| 百炼模型快照 | `~/.OCRLLM/bailian_models.json` | 合并到 `models.json`，带 `fetched_at` 自动刷新 |
| Google 模型快照 | `~/.OCRLLM/google_models.json` | 同上 |

**Rust 优势**：`tempfile::TempDir` 在 `Drop` 时自动删除，不会像 v2 的 `temp/` 目录那样无限膨胀。
模型缓存用 `dirs` crate 跨平台（Linux `~/.cache`、macOS `~/Library/Caches`、Windows `%LOCALAPPDATA%`）。

### 7.2 Python 打包

v2 是纯 Python —— 用户 `git clone` 然后 `pip install -r requirements.txt`。

v3 是 Rust 编译的 native extension —— 用户需要**预编译的 wheel**，或者本地有 Rust 工具链。

**maturin 构建流程**：

```bash
# 开发模式（本地 editable install）
pip install maturin
maturin develop

# 构建 wheel
maturin build --release

# 发布到 PyPI
maturin publish
```

**CI/CD 要求**：需要 GitHub Actions 在 Windows / macOS / Linux 上分别编译，
产出平台特定的 wheel（`ocrllm-3.0.0-cp312-cp312-win_amd64.whl` 等）。

**这对用户意味着什么**：
- 用户 `pip install ocrllm` 即可（不需要 Rust 工具链）
- 但你必须为每个平台 + Python 版本组合提供预编译 wheel
- 或者用户需要 `pip install maturin` + Rust 工具链来从源码构建

### 7.3 API Key 存储

v3 **不持久化密钥**。策略：

1. 环境变量：`DASHSCOPE_API_KEY`（与 v2 兼容）
2. 代码传入：`Config { api_key: "sk-xxx".into(), ..Default::default() }`
3. 绝不写入磁盘。

**原因**：v2 的 `AppConfig.from_env()` 已经是从环境变量读取的。
v3 保持这一行为，去掉 GUI 设置页中"填写 key 到文本框"的中间层。
调用方负责 key 的来源（env / vault / .env 文件），OCRLLM 只负责消费。

### 7.4 结构可持续性

| 维度 | v2 (Python) | v3 (Rust) |
|------|------------|-----------|
| 类型安全 | 运行时 `AttributeError` | 编译期捕获 |
| 错误处理 | `except Exception: pass` (85 处) | `Result<T, Error>` 强制处理 |
| 线程安全 | 靠 GIL + 锁，容易出错 | 编译期所有权检查 |
| 重构信心 | 改了不知道哪里会炸 | 编译通过 = 没有类型/借用错误 |
| 依赖管理 | `requirements.txt` 无 lock，冲突手动解 | `Cargo.lock` 精确锁定 |
| 代码腐化 | 容易被塞成 god file (audio.py 1855行) | 模块边界硬约束，超出 400 行编译器不给警告但架构审查会拦住 |
| 新人上手 | Python 易读但难追踪副作用 | Rust 学习曲线陡但代码意图显式 |

---

## 8. 特化决策：PDF 渲染

### 8.1 为什么独立

PDF 渲染的质量/速度权衡是**业务决策**，不是技术决策：

- 课程 PDF 通常不需要 300 DPI 全彩渲染。150 DPI 灰度图就够 OCR/视觉模型看了。
- 特化低清晰度渲染器可以把 100 页 PDF 的渲染时间从 30 秒降到 5 秒。
- 但降低清晰度意味着视觉模型可能漏掉小字公式和上下标。

这是需要实验才能确定的参数，不是写死在架构里的。

### 8.2 架构中的位置

`PageRenderer` trait 有三种可能的实现路径：

| 方案 | 实现位置 | 依赖 | 性能 | 质量 |
|------|---------|------|------|------|
| A: mupdf crate | Rust 侧 | `mupdf` crate | 高 | 高 |
| B: PyMuPDF 回调 | Python 侧 | PyMuPDF | 中 | 高 |
| C: 自研低清晰度 | Rust 侧 | `pdf` crate + `image` | 极高 | 中 |

推荐先走方案 A（Rust mupdf crate），因为它与核心库在同一语言中，避免了 PyO3 回调开销。
如果后续确认需要极致性能，再实现方案 C。

**PDF 处理器代码中只依赖 `dyn PageRenderer`，不依赖具体实现。**
这就是依赖反转——PDF 管线已经写好了，渲染器以后再说。

---

## 9. 实施计划

### 9.0 关键约束

**开发者有失忆症。每次续写必须能快速进入状态。**

对策：
- 每完成一个模块，写一个 3–5 行的 `MODULE_DONE.md` 片段记录"这个模块做了什么、为什么这样做"。
  这些片段由 Claude Code 自动写入 `memory/`。
- 工作分支按模块切分：`feat/config` → `feat/error` → `feat/api-dashscope` → ...
  每个分支只改 200–400 行，一条命令就能 review 完毕。
- 不跨模块工作。一个分支 = 一个模块。

### 9.1 十个阶段（按依赖排序）

```
Phase 1  ██ 项目骨架
         Cargo.toml + pyproject.toml + src/lib.rs (空壳)
         产出：maturin develop 成功，Python 能 import ocrllm

Phase 2  ██ 基础类型
         error.rs + config.rs
         产出：Config::from_env() 可用，所有后续模块的 Result<T, Error> 就位

Phase 3  ██ 模型目录
         catalog/model.rs + catalog/builtin.rs + catalog/cache.rs
         产出：list_vision_models() / list_audio_models() 返回正确的模型列表

Phase 4  ██ API 客户端
         api/provider.rs (trait) + api/retry.rs + api/dashscope.rs
         产出：DashscopeProvider 可独立测试（用真实 key 调一次 vision API）

Phase 5  ██ API 客户端（续）
         api/openai_compat.rs + api/google.rs + api/pool.rs
         产出：三个 provider 全部可用，免费额度 fallback 工作

Phase 6  ██ 图像处理
         imaging/resize.rs + imaging/preprocess.rs + imaging/ocr.rs
         产出：纯函数，单元测试全覆盖，无外部依赖（除 ort）

Phase 7  ██ 音视频处理
         media/ffmpeg.rs + media/audio_split.rs + media/video_frame.rs + media/extract_audio.rs
         产出：音频切片和视频抽帧可独立运行

Phase 8  ██ 处理器
         pipeline/processor.rs (trait) + registry.rs + routing
         然后按顺序：board.rs → audio.rs → pdf.rs → video/

         产出：每个处理器可独立测试

Phase 9  ██ Python 绑定
         lib.rs 中注册所有 PyO3 类，python/ocrllm/__init__.py facade
         产出：Python 端 import 即用

Phase 10 ██ 打包与 CI
         GitHub Actions 构建多平台 wheel，pytest 集成测试
         产出：pip install ocrllm 可用
```

### 9.2 工期估算

| Phase | 内容 | 工作日 |
|-------|------|--------|
| 1 | 项目骨架 | 0.5 |
| 2 | error + config | 1 |
| 3 | 模型目录 | 1.5 |
| 4–5 | API 客户端 | 3 |
| 6 | 图像处理 | 1.5 |
| 7 | 音视频处理 | 2 |
| 8 | 处理器管线 | 4 |
| 9 | Python 绑定 | 1.5 |
| 10 | 打包 CI | 1 |
| **合计** | | **16 天**（~3 周工作日） |

这是一个人全职的估算。业余时间翻倍。

### 9.3 每条分支的工作流程（失忆症适配）

```
1. 切到对应分支 (feat/xxx)
2. 读该模块的 MODULE_DONE.md（如果有）或 Architecture.md 中对应章节
3. 读依赖模块的 trait 定义（不读实现，只看接口）
4. 写代码 + 同文件单元测试
5. cargo test 通过
6. 写 MODULE_DONE.md 片段
7. commit + push
```

每次只需理解 **当前模块的 trait + 依赖模块的 trait**，不需要把整个项目装进脑子。

---

## 10. 依赖清单

### 10.1 Rust (Cargo.toml)

```toml
[dependencies]
# PyO3
pyo3 = { version = "0.23", features = ["extension-module"] }

# 序列化
serde = { version = "1", features = ["derive"] }
serde_json = "1"

# 错误处理
thiserror = "2"
anyhow = "1"  # 仅在 bin/test 中使用

# HTTP
reqwest = { version = "0.12", features = ["json", "stream"] }
tokio = { version = "1", features = ["full"] }

# 图像
image = "0.25"

# 音视频
ffmpeg-next = "7"   # ffmpeg 绑定

# ONNX OCR
ort = "2"           # ONNX Runtime

# 工具
dirs = "6"          # 跨平台缓存/配置目录
tempfile = "3"      # 自动清理临时文件
sha2 = "0.10"       # 文件哈希（检查点去重）
regex = "1"         # Markdown 清理

# PDF 渲染（可选，PageRenderer 默认实现）
mupdf = { version = "0.4", optional = true }

# 异步运行时
async-trait = "0.1"

[features]
default = []
pdf-render = ["mupdf"]  # 启用默认 PDF 渲染器

[lib]
name = "_core"
crate-type = ["cdylib"]
```

### 10.2 Python (pyproject.toml)

```toml
[build-system]
requires = ["maturin>=1.7,<2.0"]
build-backend = "maturin"

[project]
name = "ocrllm"
version = "3.0.0"
requires-python = ">=3.10"
dependencies = []  # 核心无 Python 依赖！

[project.optional-dependencies]
pdf = ["PyMuPDF>=1.27"]  # Python 侧 PageRenderer 参考实现
```

**关键点**：核心 `ocrllm` 包**零 Python 依赖**。全部逻辑在 Rust .pyd/.so 中。
PyMuPDF 只在用户需要 Python 侧 PDF 渲染时按需安装。

---

## 11. 从 v2 保留的设计决策

以下 v2 的架构决策证明有效，v3 保留：

1. **ProcessorRegistry + ProcessorSpec** → v3: `registry.rs` + `Processor` trait
2. **不可变 Config + with_updates()** → v3: `Config` 的 builder 模式（`config.with_model("...")`）
3. **路由系统** → v3: `pipeline/mod.rs` 中的 `route_input()`
4. **VideoPhase 阶段链** → v3: `video/phase.rs` + 各 phase 文件
5. **IncrementalMDWriter** → v3: `util/writer.rs`
6. **CheckpointManager** → v3: `util/checkpoint.rs`
7. **免费额度 fallback** → v3: `api/retry.rs` 中的 `with_free_tier_fallback()`
8. **协作式取消** → v3: `util/progress.rs` 中的 `ProgressSink::is_cancelled()`

---

## 12. 版本目标

| 阶段 | 内容 |
|------|------|
| v3.0 | 核心管线完成：PDF/Board/Video/Audio + DashScope，Python API 可用 |
| v3.1 | Google Gemini provider + OpenAI-compatible provider |
| v3.2 | PageRenderer 自研/选定 + PDF 公式模式 |
| v3.3 | 性能优化：并行抽帧、批量图像预处理 |
| v3.x | 社交下载（Python 侧扩展点）、更多 provider |

---

> **架构不是一成不变的。如果发现某个 trait 抽象过度、或某个模块边界画错了，改。**
> **这个文档是活的地图，不是死的规定。**
