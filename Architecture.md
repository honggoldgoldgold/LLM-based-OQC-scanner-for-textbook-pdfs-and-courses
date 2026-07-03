# OCRLLM v3 — 纯 Rust 核心 + PyO3 Python 模块

> **状态**: 设计阶段，尚未实现
> **上一版**: v2.0.0（纯 Python，PyQt5 GUI，见 git 历史 `master` 分支）
> **目标**: 全部处理逻辑用 Rust 实现，通过 PyO3/maturin 编译为 Python 原生扩展。
>         零 Python 逻辑代码。Python 侧仅做 import 转发。

---

## 0. 设计约束与前置决策

### 0.1 失忆症友好的代码组织

开发者的工作模式是间断的：每次续写都需要重读之前写的代码。因此：

- **每个 `.rs` 文件目标 80–250 行**，绝对上限 400 行。
- **文件名即模块职责**：无需跳转即可从路径推断内容。
- **每个模块顶部 3–5 行注释，标注"依赖谁、被谁依赖"**。
- **trait 先于实现**：公开接口定义在独立的 trait 块或 `*_trait.rs` 中，
  实现放在同文件 impl 块或 `*_impl.rs` 中。读代码时先读 trait，再读 impl。
- **`#[cfg(test)] mod tests` 与模块同文件**，不需要跨文件追踪测试。
- **每个模块只暴露 1–3 个公开类型/函数**。私有辅助函数不超过 5 个。

### 0.2 明确砍掉的功能

| 砍掉 | 原因 |
|------|------|
| GUI（PyQt5） | 纯库，无 UI |
| 设置对话框 | 配置走 env + `Config` 结构体 |
| 社交媒体下载（全部） | yt-dlp 是 Python 专有，且与核心识别无关 |
| FastAPI 服务层 | 调用方自己包装（太简单，不值得进核心） |
| HTML 处理器 | v2 中已是实验性占位 |
| 批处理 GUI | 库使用者自己写循环 |

**保留的处理器**：PDF、Board（板书/截图）、Video、Audio、Office（DOCX/PPTX/DOC/PPT）。

### 0.3 PDF 渲染 — Rust 原生

PDF → 图片的渲染在 Rust 侧完成，默认基于 `mupdf` crate（libmupdf 的 Rust FFI 绑定，
与 PyMuPDF 使用同一个 C 引擎）。

定义 `PageRenderer` trait 做依赖反转：PDF 处理器只依赖 trait，不依赖具体渲染器。
用户可以替换为自研的低清晰度渲染器或 `pdfium-render` crate。

**默认实现**：`src/pdf/render.rs`，约 150 行，封装 mupdf 的页面渲染 + 并行线程池。

---

## 1. 模块全景图

```text
ocrllm/                              # Python 包根目录（仅 facade，无逻辑）
│
├── pyproject.toml                   # maturin 构建配置
├── Cargo.toml                       # Rust workspace
├── Cargo.lock                       # 精确依赖锁定
│
├── src/                             # ─── 全部 Rust 源码 ───
│   ├── lib.rs                       # PyO3 入口：把 Rust 类型/函数暴露给 Python
│   ├── error.rs                     # Error enum (thiserror)
│   ├── config.rs                    # Config 结构体 (serde + envy)
│   │
│   ├── catalog/                     # 模型目录
│   │   ├── mod.rs                   #   合并查询：list_vision / list_audio
│   │   ├── model.rs                 #   VisionModel / AudioModel 类型
│   │   ├── builtin.rs               #   内置模型常量（~22 视觉 + ~9 音频）
│   │   └── cache.rs                 #   模型快照缓存 (~/.cache/ocrllm/)
│   │
│   ├── api/                         # LLM API 客户端（纯 reqwest，无 Python SDK）
│   │   ├── mod.rs                   #   模块入口 + 工厂函数
│   │   ├── provider.rs              #   LlmProvider trait
│   │   ├── dashscope.rs             #   百炼/DashScope 实现
│   │   ├── openai_compat.rs         #   通用 OpenAI-compatible 实现
│   │   ├── google.rs                #   Google Gemini REST 实现
│   │   ├── retry.rs                 #   重试/退避/免费额度 fallback 链
│   │   └── pool.rs                  #   多 Key 池化
│   │
│   ├── imaging/                     # 图像处理（纯函数）
│   │   ├── mod.rs
│   │   ├── resize.rs                #   等比缩放 + JPEG 编码
│   │   ├── preprocess.rs            #   Canny 边缘 + 自动裁剪 + HEIC 转换
│   │   └── ocr.rs                   #   ONNX OCR 封装 (ort crate)
│   │
│   ├── media/                       # 音视频处理
│   │   ├── mod.rs
│   │   ├── ffmpeg.rs                #   ffmpeg/ffprobe 查找 + 子进程调用
│   │   ├── audio_split.rs           #   音频切片 + fallback 窗口
│   │   ├── video_frame.rs           #   抽帧 + 变化检测 + pHash 去重
│   │   └── extract_audio.rs         #   视频音轨提取
│   │
│   ├── pipeline/                    # 处理器管线
│   │   ├── mod.rs                   #   模块入口 + route_input()
│   │   ├── processor.rs             #   Processor trait + ProcessInput/Output
│   │   ├── registry.rs              #   处理器注册表
│   │   ├── pdf.rs                   #   PDF 处理器 (OCR / VLM 双模式)
│   │   ├── board.rs                 #   板书/截图处理器
│   │   ├── video/                   #   视频处理器（5 阶段）
│   │   │   ├── mod.rs               #     VideoProcessor + process()
│   │   │   ├── phase.rs             #     VideoPhase trait
│   │   │   ├── phase1_audio.rs
│   │   │   ├── phase2_frames.rs
│   │   │   ├── phase3_preprocess.rs
│   │   │   ├── phase4_llm.rs
│   │   │   └── phase5_asr.rs
│   │   ├── audio.rs                 #   音频处理器
│   │   └── office.rs               #   DOCX/PPTX/DOC/PPT 文本抽取
│   │
│   ├── pdf/                         # PDF 渲染（独立子系统）
│   │   ├── mod.rs                   #   PageRenderer trait 定义
│   │   └── render.rs                #   mupdf 默认实现
│   │
│   └── util/                        # 工具
│       ├── mod.rs
│       ├── checkpoint.rs            #   检查点持久化
│       ├── writer.rs                #   增量 Markdown 写入器（槽位乱序写入）
│       ├── board_merge.rs           #   板书去重合并
│       ├── progress.rs              #   ProgressSink trait + 默认实现
│       └── markdown.rs              #   Markdown 围栏清理 + 页标记标准化
│
├── python/                          # ─── Python 层（只有 facade，零逻辑）───
│   └── ocrllm/
│       ├── __init__.py              # from _core import recognize, Config, ...
│       └── py.typed                 # PEP 561 marker
│
└── tests/                           # ─── 测试 ───
    ├── rust/                        # Rust 集成测试
    └── python/                      # Python 端 import 冒烟测试
```

**总行数估算**：Rust ~6500–7500 行，Python ~20 行（仅 `__init__.py` 的 re-export）。

---

## 2. 依赖关系（严格单向，无循环）

```text
                       ┌─────────────────┐
                       │   src/lib.rs    │  ← PyO3 绑定（唯一的 Python 边界）
                       └───────┬─────────┘
                               │
           ┌───────────────────┼───────────────────┐
           │                   │                   │
   ┌───────▼──────┐   ┌───────▼──────┐   ┌───────▼──────┐
   │   pipeline/  │   │    api/      │   │   catalog/   │
   │  (处理器)    │   │ (LLM 客户端) │   │ (模型目录)   │
   └───┬──┬──┬────┘   └──────┬───────┘   └──────┬───────┘
       │  │  │               │                  │
       │  │  │  ┌────────────┘                  │
       │  │  └──┤                               │
   ┌───▼──▼──┐  │                    ┌──────────▼───────┐
   │ imaging │  │                    │  config.rs       │
   │ media/  │  │                    │  error.rs        │
   │ pdf/    │  │                    │  (零依赖底层)     │
   └───┬─────┘  │                    └──────────────────┘
       │        │
   ┌───▼────────▼──────┐
   │     util/         │
   │ (工具：checkpoint, │
   │  writer, merge,   │
   │  progress, md)    │
   └───────────────────┘
```

**规则**：
- 下层不能 `use` 上层。`util` 不知道 `pipeline` 的存在。
- `error.rs` 和 `config.rs` 不依赖任何项目内模块（零依赖）。
- `catalog` 只依赖 `config` + `error`。
- `api` 依赖 `catalog` + `config` + `error` + `util`（retry 逻辑用 progress sink）。
- `imaging`、`media`、`pdf` 只依赖 `error` + `util`。
- `pipeline` 依赖 `api` + `imaging` + `media` + `pdf` + `util` + `catalog` + `config` + `error`。
- `lib.rs` 是唯一聚合层，依赖 `pipeline` + `config` + `catalog` + `api` + `error`。

---

## 3. 核心 trait 设计

### 3.1 `LlmProvider` — 统一 LLM 客户端接口

```rust
// src/api/provider.rs
// 依赖: error.rs, catalog/model.rs

#[async_trait]
pub trait LlmProvider: Send + Sync {
    /// 图片+文本多模态识别
    async fn chat_with_images(
        &self,
        model: &str,
        prompt: &str,
        image_paths: &[PathBuf],
    ) -> Result<String>;

    /// 纯文本对话
    async fn chat_text(
        &self,
        model: &str,
        prompt: &str,
        system_prompt: Option<&str>,
    ) -> Result<String>;

    /// 短音频同步 ASR（≤5 分钟）
    async fn transcribe_short(
        &self,
        model: &str,
        audio_path: &Path,
        hotwords: &[String],
    ) -> Result<String>;

    /// 长音频异步 filetrans（提交 + 轮询）
    async fn transcribe_long(
        &self,
        model: &str,
        audio_url: &str,
        hotwords: &[String],
    ) -> Result<String>;

    /// 模型可用性探测
    async fn probe_vision(&self, model: &str, image: &Path) -> Result<ProbeResult>;
    async fn probe_audio(&self, model: &str, audio: &Path) -> Result<ProbeResult>;

    /// 该 provider 的免费模型 fallback 链
    fn free_chain(&self, kind: ModelKind) -> Vec<String>;
}
```

三种实现，各一个文件（≤300 行），共享 `retry.rs` 的重试逻辑。
`retry.rs` 约 120 行：指数退避 + 免费额度探测 + 自动切换下一模型。

### 3.2 `Processor` — 统一处理器接口

```rust
// src/pipeline/processor.rs
// 依赖: error.rs, api/provider.rs, util/progress.rs

pub struct ProcessInput {
    pub paths: Vec<PathBuf>,
    pub output_dir: Option<PathBuf>,
    pub params: ProcessParams,      // 处理器特定参数（公式模式、页码范围等）
}

pub struct ProcessOutput {
    pub markdown: String,
    pub output_path: PathBuf,
    pub hotwords: Vec<String>,
    pub metadata: HashMap<String, String>,
}

#[async_trait]
pub trait Processor: Send + Sync {
    fn spec(&self) -> &'static ProcessorSpec;

    async fn process(
        &self,
        input: ProcessInput,
        provider: &dyn LlmProvider,
        sink: &dyn ProgressSink,
    ) -> Result<ProcessOutput>;
}

// ProcessorSpec 是编译期常量，不在运行时注册
pub struct ProcessorSpec {
    pub key: &'static str,
    pub display_name: &'static str,
    pub extensions: &'static [&'static str],
    pub accepts_multiple: bool,
    pub supports_resume: bool,
}
```

**与 v2 的关键区别**：v2 的 `ProcessorSpec` 是 Python dataclass，运行时动态注册。
v3 的 `ProcessorSpec` 是编译期常量，不需要反射和 `importlib`。
注册表是 `[&'static dyn Processor]` 静态数组，不需要单例锁。

### 3.3 `PageRenderer` — PDF 渲染（Rust 原生）

```rust
// src/pdf/mod.rs
// 依赖: error.rs

#[async_trait]
pub trait PageRenderer: Send + Sync {
    /// 渲染页面范围，返回图片路径列表
    async fn render(
        &self,
        pdf_path: &Path,
        pages: Range<u32>,
        dpi: u32,
        output_dir: &Path,
    ) -> Result<Vec<PathBuf>>;

    /// PDF 总页数
    fn page_count(&self, pdf_path: &Path) -> Result<u32>;
}
```

默认实现 `MupdfRenderer` 在 `src/pdf/render.rs`（约 150 行），
使用 `mupdf` crate 做并行页面渲染。

**为什么独立成 `src/pdf/` 子目录而不是放进 `imaging/`**：
PDF 渲染涉及 C 库链接（libmupdf），是项目中最重的编译依赖。
独立目录方便 feature-gate（未来可 `#[cfg(feature = "pdf-render")]` 条件编译）。

### 3.4 `ProgressSink` — 进度报告通道

```rust
// src/util/progress.rs
// 依赖: 无（纯 trait）

pub trait ProgressSink: Send + Sync {
    fn report(&self, current: u32, total: u32, message: &str);
    fn content(&self, text: &str, label: &str);
    fn is_cancelled(&self) -> bool;
}
```

三种实现：
- `ConsoleSink`：打印到 stdout（CLI 用）
- `PyCallbackSink`：通过 PyO3 回调传给 Python（库模式用）
- `NullSink`：不报告（批量测试用）

`is_cancelled()` 被所有长任务在循环中检查，替代 v2 的 `CancelledError` 异常机制。

---

## 4. 配置

### 4.1 原则

- **默认值即生产可用**。改变默认值需要 benchmark 数据支撑。
- **环境变量覆盖**：`OCRLLM_API_KEY`、`OCRLLM_MODEL` 等，与 v2 兼容。
- **代码覆盖**：`Config { model: "...".into(), ..Config::from_env() }`。
- **密钥不进磁盘**：api_key 来自 env 或参数，只在内存中。

### 4.2 `Config` 结构体

```rust
// src/config.rs (~200 行)
// 依赖: error.rs, serde, envy

#[derive(Debug, Clone, Deserialize)]
#[serde(default)]
pub struct Config {
    // ── 必填（有 env fallback）──
    pub api_key: String,             // DASHSCOPE_API_KEY
    pub base_url: String,            // 默认 dashscope.aliyuncs.com
    pub provider: String,            // "dashscope" | "openai_compat" | "google"

    // ── 模型选择 ──
    pub vision_model: String,        // 默认 "qwen-vl-max"
    pub asr_model: String,           // 默认 "qwen3-asr-flash-filetrans"
    pub asr_short_model: String,     // 默认 "qwen3-asr-flash"

    // ── 并发（有稳定默认值）──
    pub parallel_requests: u32,      // 15
    pub request_stagger_ms: u64,     // 500

    // ── 图像处理 ──
    pub image_max_side: u32,         // 2048
    pub image_quality: u8,           // 90

    // ── 视觉批处理 ──
    pub batch_size: u32,             // 10
    pub video_frame_batch: u32,      // 4

    // ── PDF ──
    pub pdf_dpi: u32,                // 200
    pub pdf_render_workers: u32,     // 0 = auto

    // ── 视频抽帧 ──
    pub video_frame_interval: f64,   // 5.0
    pub video_change_threshold: f64, // 0.15
    pub video_phash_threshold: u32,  // 3

    // ── 音频切片 ──
    pub audio_chunk_seconds: u32,    // 1740
    pub audio_overlap_seconds: u32,  // 30
    pub audio_asr_parallel: u32,     // 4

    // ── Google（仅 provider="google" 时生效）──
    pub google_api_key: Option<String>,
    pub google_vision_model: Option<String>,
    pub google_audio_model: Option<String>,

    // ── 付费多 Key ──
    pub extra_api_keys: Vec<String>,

    // ── 路径 ──
    pub output_dir: Option<PathBuf>,
    pub temp_dir: Option<PathBuf>,
}

impl Config {
    pub fn from_env() -> Result<Self> { /* envy::from_env() */ }
    pub fn with_model(self, model: &str) -> Self { /* builder */ }
    pub fn with_output(self, dir: &Path) -> Self { /* builder */ }
}

impl Default for Config {
    fn default() -> Self { /* 所有稳定默认值 */ }
}
```

**v2 对比**：v2 的 `config.py` 有 380 行 + 12 个嵌套 dataclass。
v3 用 `serde(default)` 自动填默认值，`envy` crate 自动从环境变量填充，
消除 v2 中 150 行的手写 `_env_bool` / `_env_int` / `_env_float` 样板。

---

## 5. 错误处理

```rust
// src/error.rs (~80 行)
// 依赖: thiserror, reqwest (for Network variant)

pub type Result<T> = std::result::Result<T, Error>;

#[derive(Debug, thiserror::Error)]
pub enum Error {
    #[error("配置: {0}")]
    Config(String),

    #[error("API [{provider}] model={model}: {message}")]
    Api { provider: String, model: String, message: String },

    #[error("免费额度耗尽: {model}")]
    QuotaExhausted { model: String },

    #[error("空响应: {model}")]
    EmptyResponse { model: String },

    #[error("网络: {0}")]
    Network(#[from] reqwest::Error),

    #[error("IO: {0}")]
    Io(#[from] std::io::Error),

    #[error("ffmpeg: {0}")]
    Ffmpeg(String),

    #[error("格式不支持: {0}")]
    UnsupportedFormat(String),

    #[error("任务已取消")]
    Cancelled,

    #[error("检查点: {0}")]
    Checkpoint(String),

    #[error("PDF 渲染: {0}")]
    PdfRender(String),

    #[error("序列化: {0}")]
    Serialization(#[from] serde_json::Error),
}
```

整个项目只使用这一个 `Error` 类型。没有 `anyhow` 在核心库中（`anyhow` 仅用于临时 bin/test）。
调用方用 `match` 精确处理每种错误，不存在 v2 的 `except Exception: pass`。

PyO3 侧提供 `Error::to_pyerr()` 方法，把 Rust 错误映射到 Python 异常类型。

---

## 6. Python API（极简 facade）

```python
# python/ocrllm/__init__.py
# 这是项目中唯一的 Python 文件。它不做任何逻辑，只做 re-export。

from ocrllm._core import (
    Config,
    ProcessOutput,
    ModelInfo,
    recognize,
    list_models,
    probe_model,
)

__version__ = "3.0.0"
```

使用：

```python
from ocrllm import recognize, Config

# 最简：自动路由 + 默认模型 + 默认参数
result = recognize("lecture.mp4")

# 带配置
cfg = Config(api_key="sk-xxx", vision_model="qwen3-vl-plus")
result = recognize("textbook.pdf", config=cfg, output_dir="./out")

# 多图板书
result = recognize(["board1.jpg", "board2.jpg", "board3.jpg"])

# 查模型
from ocrllm import list_models, probe_model
models = list_models("vision")       # -> list[ModelInfo]
ok, msg = probe_model("qwen3-vl-flash", "vision")  # -> (True, "识别成功: Hello World")
```

**API 目标**：3 个函数覆盖所有场景。不需要读文档。

---

## 7. 关键差异：v2 (纯 Python) → v3 (纯 Rust)

### 7.1 缓存管理

| 项目 | v2 | v3 |
|------|----|----|
| 模型缓存 | `~/.OCRLLM/` 下 3 个 JSON 文件，手动读写 | `dirs::cache_dir()/ocrllm/` 一个 JSON，带 expires_at |
| 检查点 | `output/.checkpoints/` 手动 JSON | 同位置，`serde_json` + 原子写入（write temp → rename） |
| 临时文件 | `temp/` 目录手动清理，历史上膨胀严重 | `tempfile::TempDir`，Drop 时自动删除 |
| ffmpeg 查找 | 遍历 15 个硬编码路径 | 同逻辑，但封装在 `media/ffmpeg.rs` 中（~80 行） |

### 7.2 打包与分发

v2：`git clone` → `pip install -r requirements.txt` → 50+ 个 Python 包，部分有 C 扩展需编译。

v3：

```bash
# 用户侧：直接 pip install（有预编译 wheel 时）
pip install ocrllm

# 开发侧：需要 Rust 工具链
cargo build --release
maturin develop
```

**CI 产出**：GitHub Actions 在 3 个平台 × 4 个 Python 版本上编译 12 个 wheel。
用户 `pip install ocrllm` 自动选择匹配的 wheel，无需 Rust。

**关键简化**：v3 的 `pip install ocrllm` 安装一个 `.pyd`/`.so` 文件 + 一个 `__init__.py`。
总安装体积从 ~500MB（含 PyQt5、opencv、onnxruntime）降到 ~30MB（Rust 静态链接 + mupdf）。

### 7.3 API Key 处理

v3 不持久化密钥。来源优先级：
1. `Config.api_key` 显式传入
2. 环境变量 `DASHSCOPE_API_KEY`
3. 环境变量 `OCRLLM_API_KEY`
4. 都没有 → `Error::Config("未设置 API Key")`

Google API Key 同理：参数 → `GOOGLE_API_KEY` env → 报错。

### 7.4 结构可持续性

| 维度 | v2 | v3 |
|------|----|----|
| 类型安全 | `AttributeError` at runtime | 编译期拒绝 |
| 错误可见性 | 85 处 `except Exception`，部分静默吞错 | 每个错误路径显式 `match` |
| 并发正确性 | GIL + 锁，数据竞争靠 discipline | `Send + Sync` 编译期验证 |
| 重构风险 | 改 `audio.py:1855` 不敢动 | 每个文件 ≤400 行，改动影响面窄 |
| 依赖版本 | `requirements.txt` 无 lock | `Cargo.lock` 精确可复现 |
| 死代码 | `VISION_MODEL_OPTIONS` legacy tuple 残留 | Rust 编译器警告 unused，CI 拒绝 warning |
| 零成本抽象 | N/A（Python 无此概念） | trait 静态分发，运行时开销等于手写 |

---

## 8. PDF 渲染决策

### 8.1 为什么默认用 mupdf crate

- `mupdf` 是 `libmupdf` 的 Rust FFI 包装。libmupdf 是 PyMuPDF 的底层引擎，成熟度极高。
- 支持并行页面渲染（线程安全，mupdf 1.23+ 支持多 context）。
- 输出格式灵活：RGB pixmap → PNG/JPEG/PPM。

### 8.2 替代路径

| 方案 | 依赖 | 性能 | 质量 | 适用场景 |
|------|------|------|------|----------|
| A: mupdf crate | libmupdf C 库 | 高 | 高 | 默认方案 |
| B: pdfium-render | libpdfium (Chrome) | 很高 | 高 | A 的平替 |
| C: 自研简化渲染 | `pdf` crate + `image` | 极高 | 中 | 需要极致速度 |
| D: 纯 OCR 模式 | 无渲染库 | — | — | 扫描版 PDF 免渲染 |

方案 C 和 D 是用户已明确关注的。架构通过 `PageRenderer` trait 支持热切换：

```rust
let renderer: Box<dyn PageRenderer> = if fast_mode {
    Box::new(FastRenderer::new(150))   // 低 DPI，灰度输出
} else {
    Box::new(MupdfRenderer::new(200))  // 标准 DPI，彩色输出
};
let processor = PdfProcessor::new(renderer);
```

### 8.3 低清晰度渲染的 tradeoff 量化

这是一个需要实验验证的参数，不是写死在架构里的：

- 100 页 PDF @ 200 DPI 彩色：~30 秒渲染 + ~15 MB×100 图片 = 1.5 GB 临时磁盘
- 100 页 PDF @ 120 DPI 灰度：~8 秒渲染   + ~3 MB×100 图片  = 300 MB 临时磁盘
- 视觉模型对 120 DPI 灰度的公式识别是否退化？**需要跑 benchmark**。

---

## 9. 实施计划

### 9.0 失忆症工作流

每次续写只需理解"当前模块 + 依赖模块的 trait 签名"：

```text
1. 切到功能分支 (feat/xxx)
2. 打开 Architecture.md → 找到该模块的章节 → 读 trait 定义
3. 打开依赖模块的 trait 文件（只看 trait 不看 impl），确认调用契约
4. 写代码 + 同文件 #[cfg(test)] mod tests
5. cargo test → 通过
6. commit + push
```

**单个模块的认知范围**：2–3 个 trait 文件 + 当前模块 = ~500 行阅读量，一小时内可完成。

### 9.1 十阶段（按依赖排序，不可并行）

```
Phase 1   ██ 项目骨架 (0.5 天)
          Cargo.toml + pyproject.toml + src/lib.rs（空壳 PyO3 模块）
          产出：maturin develop 成功，Python 能 import ocrllm

Phase 2   ██ 基础类型 (1 天)
          error.rs + config.rs
          产出：Config::from_env() 可用，所有模块共享 Error 类型

Phase 3   ██ 工具模块 (1 天)
          util/progress.rs + util/writer.rs + util/checkpoint.rs + util/markdown.rs + util/board_merge.rs
          产出：ProgressSink、IncrementalWriter、CheckpointManager 就位

Phase 4   ██ 模型目录 (1 天)
          catalog/model.rs + catalog/builtin.rs + catalog/cache.rs
          产出：list_vision_models() / list_audio_models()

Phase 5   ██ API 客户端 (2 天)
          api/provider.rs (trait) + api/retry.rs + api/dashscope.rs
          产出：DashscopeProvider 可独立调通一次真实 vision API

Phase 6   ██ API 客户端续 (1.5 天)
          api/openai_compat.rs + api/google.rs + api/pool.rs
          产出：3 个 provider + 免费额度 fallback 全部可用

Phase 7   ██ 图像 + 音视频 (2 天)
          imaging/* + media/* + pdf/render.rs
          产出：resize、preprocess、OCR、音频切片、视频抽帧、PDF 渲染均可独立运行

Phase 8   ██ 处理器 (4 天)
          pipeline/processor.rs → registry.rs → board.rs → audio.rs → office.rs → pdf.rs → video/
          产出：每个处理器可独立 cargo test，用 mock provider

Phase 9   ██ PyO3 绑定 + Python facade (1.5 天)
          lib.rs 注册所有 PyO3 类/函数，python/ocrllm/__init__.py
          产出：pip install -e . 后 Python 完整可用

Phase 10  ██ CI + 多平台 wheel (1.5 天)
          GitHub Actions workflows，pytest 集成测试，readme
          产出：PR merge 自动发布 wheel 到 PyPI
```

### 9.2 工期

| Phase | 工作日 |
|-------|--------|
| 1 | 0.5 |
| 2 | 1 |
| 3 | 1 |
| 4 | 1 |
| 5 | 2 |
| 6 | 1.5 |
| 7 | 2 |
| 8 | 4 |
| 9 | 1.5 |
| 10 | 1.5 |
| **合计** | **16 天** |

全职 3 周，业余时间 6–8 周。

---

## 10. 依赖清单

### 10.1 Rust (Cargo.toml)

```toml
[package]
name = "ocrllm-core"
version = "3.0.0"
edition = "2024"

[lib]
name = "_core"
crate-type = ["cdylib"]

[dependencies]
# Python 绑定
pyo3 = { version = "0.23", features = ["extension-module"] }

# 序列化 + 配置
serde = { version = "1", features = ["derive"] }
serde_json = "1"
envy = "0.4"                         # env var → Config struct 自动映射

# 错误处理
thiserror = "2"

# HTTP
reqwest = { version = "0.12", features = ["json", "rustls-tls"], default-features = false }
tokio = { version = "1", features = ["rt-multi-thread", "macros", "sync", "time"] }
async-trait = "0.1"

# 图像处理
image = { version = "0.25", features = ["jpeg", "png", "webp"] }

# PDF 渲染
mupdf = "0.4"                        # libmupdf Rust binding

# ONNX OCR
ort = { version = "2", features = ["load-dynamic"] }

# 工具
dirs = "6"                           # 跨平台 XDG 目录
tempfile = "3"                       # 自动清理临时文件/目录
sha2 = "0.10"                        # 文件哈希（pHash 去重 + 检查点）
regex = "1"                          # Markdown 清理 + 页标记解析
uuid = { version = "1", features = ["v4"] }  # 检查点 ID

# 日志
log = "0.4"
env_logger = "0.11"                  # CLI 用；库不强制日志后端

[dev-dependencies]
tokio-test = "0.4"

[profile.release]
opt-level = 3
lto = true
codegen-units = 1
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
dependencies = []   # ← 零 Python 依赖

[project.optional-dependencies]
# 无。核心库不依赖任何 Python 包。
# 用户如需 PDF 渲染的 Python 侧替代实现，自行 pip install PyMuPDF。

[tool.maturin]
features = ["pyo3/extension-module"]
python-source = "python"
```

核心包 `ocrllm` 的依赖树：

```text
ocrllm
  └── _core.pyd/.so   (Rust 静态链接了 mupdf + ort + reqwest + tokio + image)
```

没有 Python 二级依赖。不会有 pip 依赖冲突。

---

## 11. 从 v2 保留的正确决策

以下 v2 的架构决策经验证有效，v3 保留并 Rust 化：

1. **处理器注册表 + 路由** → v3: `registry.rs` 的静态 `&[ProcessorSpec]` + `route_input()`
2. **不可变 Config + builder** → v3: `Config` 上 `fn with_*(self, ...) -> Self`
3. **VideoPhase 阶段链** → v3: `phase.rs` trait + 5 个 phase 文件，每个 ≤200 行
4. **IncrementalMDWriter 槽位乱序写入** → v3: `util/writer.rs`，用 `Vec<Option<String>>` + `Mutex`
5. **检查点增量保存** → v3: `util/checkpoint.rs`，JSON 原子写入
6. **免费额度 fallback 链** → v3: `api/retry.rs`，`Vec<String>` 线性尝试
7. **协作式取消** → v3: `ProgressSink::is_cancelled()` 在循环中检查
8. **Markdown 围栏清理 + 页标记标准化** → v3: `util/markdown.rs`，纯函数

---

## 12. 版本路线

| 版本 | 内容 |
|------|------|
| v3.0 | 核心管线：Board + Audio + PDF + Video + Office，DashScope provider |
| v3.1 | Google Gemini + OpenAI-compatible provider |
| v3.2 | 低清晰度 PDF 渲染器（自研）+ benchmark 报告 |
| v3.3 | 性能 pass：rayon 并行抽帧、SIMD 图像缩放、批量 API 请求 pipeline |
| v3.4+ | 命令行工具（clap）、本地模型支持（llama.cpp binding，如有需求） |

---

> **架构是活的。如果 Phase 2 写完发现 trait 画错了，改 trait。**
> **如果 mupdf crate 在 Phase 7 被证明不够稳定，切 pdfium-render。**
> **这个文档告诉你"去哪里"，不是"必须走这条精确的路"。**
