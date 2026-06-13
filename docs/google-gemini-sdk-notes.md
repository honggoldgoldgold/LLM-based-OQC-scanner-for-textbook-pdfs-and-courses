# Google Gemini SDK 接入调研记录

更新时间：2026-06-13

## 官方入口

- Gemini API 文档：https://ai.google.dev/gemini-api/docs?hl=zh-cn
- Models API：https://ai.google.dev/api/models?hl=zh-cn
- 图片理解：https://ai.google.dev/gemini-api/docs/image-understanding?hl=zh-cn
- 音频理解：https://ai.google.dev/gemini-api/docs/audio?hl=zh-cn
- 视频理解：https://ai.google.dev/gemini-api/docs/video-understanding?hl=zh-cn
- Files API：https://ai.google.dev/gemini-api/docs/files?hl=zh-cn
- 速率限制：https://ai.google.dev/gemini-api/docs/rate-limits?hl=zh-cn
- API key：https://ai.google.dev/gemini-api/docs/api-key?hl=zh-cn

## SDK 调用方式

- Python SDK 使用 `from google import genai`，客户端为 `genai.Client(api_key=...)`。
- 文本和多模态统一走 `client.models.generate_content(model=..., contents=...)`。
- 模型列表走 `client.models.list()`，REST fallback 是 `GET https://generativelanguage.googleapis.com/v1beta/models`。
- 图片小请求可用 `google.genai.types.Part.from_bytes(data=..., mime_type=...)` 内嵌发送。
- 大音频、长视频、大图片应先 `client.files.upload(file=...)`，再把上传对象放入 `contents`。

## 不显而易见的特性

- Google 官方 SDK 会自动读取环境变量，但如果同时存在 `GOOGLE_API_KEY` 和 `GEMINI_API_KEY`，`GOOGLE_API_KEY` 优先。OCRLLM UI 内显式传入用户填写的 key，避免被系统环境变量悄悄覆盖。
- Models API 返回的是 `models/{id}` 形式，实际调用 `generate_content` 时使用去掉 `models/` 后的 id 更符合官方 Python 示例。
- `supportedGenerationMethods` 需要包含 `generateContent` 才适合 OCRLLM 当前识别管线；只支持 `embedContent` 的模型必须过滤掉。
- Files API 文件会自动删除，官方文档写明单文件限制和项目存储限制。OCRLLM 当前只把它当临时上传通道，不把 Google 文件 URI 当长期缓存。
- Google 速率限制按项目计算，不是按 API key 计算。后续做 Google API 池时，不能照搬 DashScope 多 key 提升并发的假设。
- 实验、预览、快照模型通常更容易有严格限流。OCRLLM 将它们放在图片识别优先队列前段，是为了优先消耗免费/不稳定模型；但限流错误仍按同模型重试处理，不直接误判为额度耗尽。
- `RESOURCE_EXHAUSTED` 既可能是 quota，也可能是 rate limit。OCRLLM 分类时先看是否包含 rate limit/RPM/TPM/RPD 等字样；否则才进入“切换下一个免费候选模型”。
- 有些异常会以 JSON 文本形式出现在返回内容里。OCRLLM 会把形如 `{"error": ...}` 的模型文本视为假成功，并重新进入错误分类。
- 长音频转写不是单独 ASR API，而是 Gemini 多模态模型加 Files API 和提示词。当前 Google 模式不做短音频盲切回退。

## OCRLLM 当前策略

- Google 模式独立于 DashScope 千问模式和 OpenAI-compatible 视觉 Provider。
- 启用 Google 模式时，后台识别主路由走 Google provider，千问主链路不参与。
- OpenAI-compatible 视觉 Provider 的配置不清空，用户关闭 Google 模式后仍可继续使用。
- 图片/视频帧模型优先链来自实时模型列表，排序为 image/preview/snapshot/experimental 优先，Gemini 2+ Pro/Flash 长音频候选最后兜底。
- 长音频模型优先链来自实时模型列表，仅保留 Gemini 2+ Pro/Flash 这类多模态长上下文候选。
- 网络错误、限流、并发限制先重试同模型；quota/欠费/404 模型不可用切换下一个候选。
