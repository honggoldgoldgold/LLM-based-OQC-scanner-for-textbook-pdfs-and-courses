"""
录课视频处理选项卡。
"""

from __future__ import annotations

import os

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QCheckBox, QMessageBox,
)

from OCRLLM import prompts
from OCRLLM.gui.batch_tasks import BatchFileTask, run_batch_tasks
from OCRLLM.gui.widgets import FileInput, PromptButton, browse_files, join_paths_text, split_paths_text


class VideoTab(QWidget):
    """录课视频处理选项卡 GUI。"""
    def __init__(self, get_cfg, start_worker, get_tracker=None, get_output_in_place=None, parent=None):
        super().__init__(parent)
        self._get_cfg = get_cfg
        self._start_worker = start_worker
        self._get_tracker = get_tracker
        self._get_output_in_place = get_output_in_place or (lambda: False)
        self._build_ui()

    def _build_ui(self):
        vbox = QVBoxLayout(self)

        self._video_path = FileInput(
            accept_exts=['mp4', 'avi', 'mkv', 'mov', 'flv', 'wmv'],
            multi=True,
            placeholder="选择或拖入视频文件（支持多选，; 分隔）")
        from OCRLLM.gui.tabs.pdf_tab import _file_row
        vbox.addLayout(_file_row(
            "视频文件:", self._video_path, "选择多份",
            lambda: browse_files(self, "选择视频文件",
                                "视频文件 (*.mp4 *.avi *.mkv *.mov *.flv *.wmv);;所有文件 (*)",
                                self._video_path)))

        # 阶段选择
        phase_row = QHBoxLayout()
        phase_row.addWidget(QLabel("执行阶段:"))
        self._phases: dict[int, QCheckBox] = {}
        for p, name in [(1, "音频提取"), (2, "智能抽帧"), (3, "裁剪缩放"),
                        (4, "大模型识别"), (5, "语音识别")]:
            cb = QCheckBox(f"{p}.{name}")
            cb.setChecked(True)
            self._phases[p] = cb
            phase_row.addWidget(cb)
        phase_row.addStretch()
        vbox.addLayout(phase_row)

        from OCRLLM.gui.app import make_action_buttons
        self._board_prompt = PromptButton("录课板书/课件识别", "video_board", prompts.BOARD_WITH_HOTWORDS, self)
        self._audio_prompt = PromptButton("录课语音识别", "video_audio_transcribe", prompts.AUDIO_TRANSCRIBE, self)
        vbox.addLayout(make_action_buttons(
            "▶ 开始处理视频", self._run,
            self._reset_prompts_to_default,
            extra_widgets=[self._board_prompt, self._audio_prompt]))

    def _reset_prompts_to_default(self):
        self._board_prompt.reset_to_default()
        self._audio_prompt.reset_to_default()

    def set_input_paths(self, paths: list[str] | tuple[str, ...]):
        """从外部设置视频文件路径（如拖放）。

        Args:
            paths: 文件路径列表。
        """
        if not paths:
            self._video_path.clear()
            return
        self._video_path.setText(join_paths_text(list(paths)))

    def _run(self):
        video_paths = split_paths_text(self._video_path.text())
        if not video_paths:
            QMessageBox.warning(self, "提示", "请先选择视频文件"); return
        missing = [video_path for video_path in video_paths if not os.path.isfile(video_path)]
        if missing:
            QMessageBox.warning(self, "提示", "文件不存在:\n" + "\n".join(missing[:10])); return

        phases = [p for p, cb in self._phases.items() if cb.isChecked()]
        skip_audio = 5 not in phases
        prompt_text = self._board_prompt.prompt_text()
        audio_prompt_text = self._audio_prompt.prompt_text()

        # 在原位置输出：输出目录放在视频文件同级目录
        def _output_dir_for(video_path: str) -> str | None:
            if not self._get_output_in_place():
                return None
            from pathlib import Path
            src_dir = os.path.dirname(os.path.abspath(video_path))
            return os.path.join(src_dir, Path(video_path).stem)

        if len(video_paths) == 1:
            video_path = video_paths[0]
            output_dir = _output_dir_for(video_path)

            def task(reporter):
                from OCRLLM.processors.video import VideoProcessor
                cfg = self._get_cfg()
                tracker = self._get_tracker() if self._get_tracker else None
                proc = VideoProcessor(cfg=cfg, reporter=reporter, tracker=tracker)
                result = proc.process(
                    video_path=video_path, output_dir=output_dir,
                    phases=phases, skip_audio=skip_audio,
                    prompt_template=prompt_text or None,
                    audio_prompt_template=audio_prompt_text or None,
                )

                md_path = result.get("board_md", "")
                md_size = f"{os.path.getsize(md_path)/1024:.1f}KB" if md_path and os.path.exists(md_path) else "无"
                frames_dir = result.get("frames_dir", "")
                n = len([f for f in os.listdir(frames_dir) if f.endswith(".jpg")]) if frames_dir and os.path.isdir(frames_dir) else 0
                return f"视频处理完成!\n帧数: {n}\nMD: {md_size}\n输出: {result.get('output_dir', '')}"

            if self._start_worker(task):
                self._board_prompt.consume_temporary()
                self._audio_prompt.consume_temporary()
            return

        def task(reporter):
            from OCRLLM.processors.video import VideoProcessor
            cfg = self._get_cfg()
            tasks = []
            for video_path in video_paths:
                output_dir = _output_dir_for(video_path)

                def _run_one(task_cfg, child_reporter, *, path=video_path, out=output_dir):
                    proc = VideoProcessor(cfg=task_cfg, reporter=child_reporter)
                    result = proc.process(
                        video_path=path,
                        output_dir=out,
                        phases=phases,
                        skip_audio=skip_audio,
                        prompt_template=prompt_text or None,
                        audio_prompt_template=audio_prompt_text or None,
                    )
                    return result.get("output_dir", "")

                tasks.append(BatchFileTask(
                    source_path=video_path,
                    display_name=os.path.basename(video_path),
                    run=_run_one,
                ))
            return run_batch_tasks(task_kind="video", task_label="视频", cfg=cfg, reporter=reporter, tasks=tasks)

        if self._start_worker(task):
            self._board_prompt.consume_temporary()
            self._audio_prompt.consume_temporary()
