# OCRLLM v3

> **策略**: contract-first strangler。先冻结 Python API → 用 Python 跑通首个处理器 →
> golden test → 逐个用 Rust 替换引擎。Rust 是实现细节，API 是第一原则。

---

## 0. 架构决策

### 0.1 Contract-first

API 先冻结，引擎后实现。调用方不感知引擎是 Python 还是 Rust。

### 0.2 Strangler

不是重写后切换，是逐个替换引擎。每替换一个，golden test 通过才合并。

### 0.3 Board-first

首个处理器选 board（板书/截图）。依赖链最短：图片 resize → HTTP 请求 → markdown 清理。
不依赖 PDF 渲染、ffmpeg、ONNX OCR。零阻塞性外部依赖。

### 0.4 PDF 渲染

默认引擎: `pdfium-render`（BSD 许可，Chrome 同款，预编译二进制）。
定义 `PageRenderer` trait 做依赖反转。如果编译失败或体积不可接受，换实现不改处理器代码。

### 0.5 砍掉

- 社交媒体下载（全体）
- DOC/PPT 二进制格式（保留 DOCX/PPTX 的 ZIP+XML 解析）
- GUI / 设置页 / API 服务层 / HTML 处理器

---

## 1. 公共 API（冻结）

```python
from ocrllm import recognize, recognize_batch, Config, RecognitionResult

# 单文件
result = recognize("board.jpg")
result = recognize("lecture.mp4", config=Config(model="qwen3-vl-plus"))

# 多文件同类型
result = recognize(["img1.jpg", "img2.jpg"])

# 批量混合类型
results = recognize_batch(["a.pdf", "b.jpg", "c.mp4"])

# 配置
cfg = Config(api_key="sk-xxx", model="qwen-vl-max", output_dir="./out")
cfg = Config()  # 全部默认，api_key 从 DASHSCOPE_API_KEY env 读
```

### RecognitionResult

`.markdown: str` / `.output_path: Path` / `.source_type: str` / `.hotwords: list[str]`

### 异常

`ConfigError` / `QuotaExhausted` / `UnsupportedFormat` / `Cancelled`

---

## 2. 模块骨架

```
src/
├── lib.rs              PyO3 入口，唯一 Python 边界
├── error.rs            Error enum (thiserror)
├── config.rs           Config + env 加载 (serde + envy)
├── catalog/            模型清单
├── api/                LLM 客户端 (reqwest, 纯 HTTP)
│   ├── provider.rs     LlmProvider trait
│   ├── retry.rs        两层: 单模型重试 + 免费额度回退链
│   └── pool.rs         多 Key 轮转
├── imaging/            图像（纯函数）
├── media/              音视频
├── pipeline/           处理器
│   ├── processor.rs    Processor trait
│   ├── registry.rs     静态注册表
│   ├── board.rs / audio.rs / office.rs / pdf.rs
│   └── video/          5 阶段拆为独立文件
├── pdf/                PageRenderer trait + pdfium 实现
└── util/
    ├── progress.rs     ProgressSink trait
    ├── writer.rs       槽位 MD 写入（文件即检查点）
    ├── markdown.rs     MD 清理
    └── board_merge.rs  板书去重
```

Python 侧仅 `ocrllm/__init__.py`（re-export）。

---

## 3. 关键设计决策

### 断点续传

MD 输出文件即检查点。初始全部槽位 `<!-- ocrllm:slot N status=pending -->`，完成后替换为
`status=done` + 实际内容。续传时解析 MD 找 pending 槽位。不保留独立 JSON 检查点文件。
文件写槽位时加独占锁，先写 `.tmp` 再 rename。

### 重试与回退

两层。单模型重试：指数退避，只重试网络/5xx/空响应。回退链：模型 A 免费额度耗尽 →
模型 B → 模型 C。错误分类基于 `Error` enum 的模式匹配。

### API Key

不持久化。来源：参数 > `DASHSCOPE_API_KEY` env > `OCRLLM_API_KEY` env > 报错。

### 文件大小

每个 `.rs` ≤ 250 行，极限 400。模块顶部 1-2 行注释标注依赖。

### 依赖方向

```
error ← config ← util ← catalog ← api ← pipeline ← lib.rs
                   util ← imaging / media / pdf
```

下层不知道上层存在。

---

## 4. 预留 trait（插座）

| trait           | 作用                               |
|-----------------|------------------------------------|
| `LlmProvider`   | 换 LLM 后端不动处理器              |
| `Processor`     | 新增输入类型不动路由               |
| `PageRenderer`  | 换 PDF 引擎不动处理器              |
| `ProgressSink`  | CLI / Python 回调 / 测试 mock 三实现 |

---

## 5. Phase 0 — API 合约 + 首个处理器

**Done criteria**:

- [ ] `pip install -e .` 在当前环境成功
- [ ] `import ocrllm` 从任意 cwd 可用
- [ ] API 全部可用: `Config`, `RecognitionResult`, `recognize`, `recognize_batch`, 异常类
- [ ] `recognize("board.jpg")` 端到端跑通（全部 Python，无 Rust）
- [ ] golden test: ≥3 张代表性板书图片，新旧输出 diff 通过
- [ ] PyO3 spike（独立分支）: Windows wheel 可构建，`_core.pyd` < 30MB，进度回调和取消可用

**Phase 0 栈: 全部 Python。PyO3 spike 只证明编译链，不接入主流程。**

### Phase 1+ — 引擎替换（strangler）

按依赖顺序，一次一个。每次替换后 golden test 通过才合并：

```
1. error + config        (Layer 0)
2. util/*                (Layer 2)
3. catalog/*             (Layer 1)
4. imaging/*             (Layer 4)
5. media/*               (Layer 4)
6. api/*                 (Layer 7-8)
7. pipeline/board.rs     (Layer 9, 首个 Rust 处理器)
8. pipeline/audio.rs → office.rs → pdf.rs → video/
9. lib.rs                (PyO3 绑定)
10. CI + wheel
```

每步认知范围：当前模块 + 下面层的 trait 签名。
