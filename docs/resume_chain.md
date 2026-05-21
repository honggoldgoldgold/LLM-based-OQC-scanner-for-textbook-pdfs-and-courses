# Resume Chain

本文只说明 OCRLLM 当前的断点续传链条，目标是把“谁保存状态、谁验证状态、谁清理失效产物、谁发起恢复”说清楚。

## 入口

- GUI 启动时通过 CheckpointManager.list_incomplete 扫描输出目录下的 .checkpoints。
- GUI 点击继续任务时，不再自己拼恢复参数，而是调用处理器的 resume_options_from_checkpoint。
- PDF 恢复入口在 PDFProcessor._process_with_llm。
- Video 恢复入口在 VideoProcessor.process 和 VideoPhase.run。

## 统一规则

1. checkpoint 只表示“某个阶段或批次被声明完成”，不单独证明产物一定可恢复。
2. 恢复前必须同时验证两类东西：
   - checkpoint 与当前任务参数兼容
   - 对应产物仍然存在且满足最小有效性条件
3. 一旦发现某个已完成阶段无法恢复，必须同时做三件事：
   - 从内存 completed 集中移除该阶段及其下游阶段
   - 删除这些失效阶段的下游产物
   - 立刻把裁剪后的 completed 集重新写回 checkpoint

## PDF 链条

### PDF 保存什么

- Checkpoint.extra 保存 page_range、page_offset、batch_size、prompt_template。
- 每个批次只有在 LLM 结果被判定 success 后才调用 save_incremental。
- IncrementalMDWriter 负责把批次结果按槽位写入输出文件。

### 如何恢复

1. 读取 checkpoint。
2. 用 total_items、output_path、extra 做兼容性校验。
3. 从现有输出 Markdown 中按 Page 标题恢复已完成批次内容。
4. 只有既在 checkpoint.completed_indices 中、又能从输出文件恢复出完整内容的批次，才会被真正跳过。
5. 缺内容的已完成批次会重新识别。

### PDF 当前不变量

- checkpoint 不能单独决定跳过，输出内容也必须可恢复。
- GUI 恢复必须带回原 page_range 和 prompt_template，否则会被视为不兼容任务。

## Video 链条

### Video 保存什么

- Checkpoint.extra 保存 stem、phases、skip_audio、prompt_template。
- 每个 phase 在 execute 成功后，才通过 save_incremental 标记完成。

### 阶段恢复判定

- Phase 1: 音频文件存在且非空。
- Phase 2: frame_info.json 可读，且其中引用的抽帧文件都存在。
- Phase 3: manifest 可读、数量匹配、source_path 匹配、processed_path 都存在。
- Phase 4: 板书 Markdown 存在且非空，且能解析出与抽帧结果一一对应的帧标题；热词表缺失时允许从板书内容回推。
- Phase 5: 转写 Markdown 存在且非空。

### 失效处理

如果某个已完成 phase 的 can_resume 返回 False：

1. VideoPhase.run 会把当前 phase 及其下游 phase 从 completed 集中移除。
2. VideoProcessor._clear_invalidated_phase_artifacts 会删除对应下游产物：
   - Phase 3: processed_frames 和 manifest
   - Phase 4: 板书 MD、合并 MD、热词表
   - Phase 5: 语音转写 MD
3. 新的 completed 集会立刻保存回 checkpoint。
4. 然后从当前失效阶段重新执行。

### Video 当前不变量

- 上游阶段重跑时，下游产物不能继续留在输出目录里冒充有效结果。
- GUI 恢复必须带回原 phases、skip_audio、prompt_template，否则会触发 checkpoint 不兼容并重新开始。

## 代码定位

- core/checkpoint.py: Checkpoint、CheckpointManager
- core/incremental_writer.py: PDF 增量内容落盘
- processors/pdf.py: PDF checkpoint 契约、批次恢复、输出恢复
- processors/video.py: Video checkpoint 契约、下游产物清理
- processors/video_pipeline.py: phase 级恢复、失效裁剪和重跑
- gui/app.py: GUI 恢复入口

## 仍然刻意保留的现实约束

- Phase 4 仍不要求合并板书 MD 一定存在；合并结果被视为可重建的派生产物，但原始板书 MD 必须保持可解析帧结构。
- GUI 只展示最近更新的一条未完成任务；如果存在多条 checkpoint，优先显示 updated_at 最新的那条。
- 如果 prompt_template 或 page_range 与原任务不一致，系统优先判定为不兼容并重新开始，而不是冒险复用旧状态。
