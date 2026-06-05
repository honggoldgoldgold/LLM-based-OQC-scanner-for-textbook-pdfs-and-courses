"""
API / 模型设置独立弹窗 — 替代原主窗口内嵌的可展开设置面板。

包含:
  · DashScope API Key / Base URL
  · 视觉独立 Provider（OpenAI 兼容）
  · 视觉模型 / 音频模型选择
  · LLM 并发 / 错峰参数
  · 付费模式 / API 池
"""

from __future__ import annotations

from typing import Optional

from PyQt5.QtWidgets import (
    QCheckBox, QDialog, QDoubleSpinBox, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QMessageBox,
    QPushButton, QScrollArea, QSpinBox, QVBoxLayout,
    QWidget, QFrame,
)
from PyQt5.QtCore import QSettings, Qt

from OCRLLM.config import AppConfig
from OCRLLM.core import model_catalog

SETTINGS_ORG = "OCRLLM"
SETTINGS_APP = "QCR"


class SettingsDialog(QDialog):
    """API / 模型设置弹窗。读取 QSettings 和当前 AppConfig，确认后回写。"""

    def __init__(self, parent: QWidget, cfg: AppConfig):
        super().__init__(parent)
        self._cfg = cfg
        self._settings = QSettings(SETTINGS_ORG, SETTINGS_APP)

        self._pending_vision_model: str = cfg.models.vision_model
        self._pending_audio_model: str = cfg.models.asr_model

        self._init_ui()
        self._restore_from_settings()

    # ---- public ----

    def apply_config(self) -> AppConfig:
        """返回更新后的 AppConfig（不修改原实例）。"""
        updates, _info = self._read_overrides()
        return self._cfg.with_updates(**updates)

    # ---- UI ----

    def _init_ui(self):
        self.setWindowTitle("API / 模型设置")
        self.setMinimumSize(700, 520)
        self.resize(750, 580)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        body = QWidget()
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(0, 0, 0, 0)

        # ---- DashScope ----
        dash_group = QGroupBox("DashScope 主 API")
        dash_layout = QVBoxLayout(dash_group)

        row1 = QHBoxLayout()
        row1.addWidget(QLabel("API Key:"))
        self._api_key_input = QLineEdit()
        self._api_key_input.setEchoMode(QLineEdit.Password)
        row1.addWidget(self._api_key_input, stretch=1)
        self._api_key_toggle = QPushButton("显示")
        self._api_key_toggle.setFixedWidth(50)
        self._api_key_toggle.setCheckable(True)
        self._api_key_toggle.toggled.connect(
            lambda c: self._api_key_input.setEchoMode(
                QLineEdit.Normal if c else QLineEdit.Password))
        row1.addWidget(self._api_key_toggle)
        dash_layout.addLayout(row1)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Base URL:"))
        self._base_url_input = QLineEdit()
        self._base_url_input.setPlaceholderText("https://dashscope.aliyuncs.com/compatible-mode/v1")
        row2.addWidget(self._base_url_input, stretch=1)
        dash_layout.addLayout(row2)

        body_layout.addWidget(dash_group)

        # ---- 视觉 Provider ----
        vis_group = QGroupBox("视觉模型独立 Provider（OpenAI 兼容）")
        vis_layout = QVBoxLayout(vis_group)

        vis_toggle_row = QHBoxLayout()
        self._vision_enabled_cb = QCheckBox("启用独立视觉 Provider")
        vis_toggle_row.addWidget(self._vision_enabled_cb)
        vis_toggle_row.addStretch()
        vis_layout.addLayout(vis_toggle_row)

        vis_row1 = QHBoxLayout()
        vis_row1.addWidget(QLabel("Provider 名称:"))
        self._vision_provider_input = QLineEdit()
        self._vision_provider_input.setPlaceholderText("如 ioasis / mozheyu")
        vis_row1.addWidget(self._vision_provider_input)
        vis_row1.addWidget(QLabel("Wire API:"))
        self._vision_wire_input = QLineEdit("chat")
        self._vision_wire_input.setPlaceholderText("chat 或 responses")
        vis_row1.addWidget(self._vision_wire_input)
        vis_layout.addLayout(vis_row1)

        vis_row2 = QHBoxLayout()
        vis_row2.addWidget(QLabel("API Key:"))
        self._vision_key_input = QLineEdit()
        self._vision_key_input.setEchoMode(QLineEdit.Password)
        vis_row2.addWidget(self._vision_key_input, stretch=1)
        vis_layout.addLayout(vis_row2)

        vis_row3 = QHBoxLayout()
        vis_row3.addWidget(QLabel("Base URL:"))
        self._vision_url_input = QLineEdit()
        self._vision_url_input.setPlaceholderText("https://ai-api.mozheyu.fun/v1")
        vis_row3.addWidget(self._vision_url_input, stretch=1)
        vis_layout.addLayout(vis_row3)

        vis_row4 = QHBoxLayout()
        vis_row4.addWidget(QLabel("Reasoning effort:"))
        self._vision_reasoning_input = QLineEdit()
        self._vision_reasoning_input.setPlaceholderText("留空或 high")
        vis_row4.addWidget(self._vision_reasoning_input)
        self._vision_network_cb = QCheckBox("network_access")
        vis_row4.addWidget(self._vision_network_cb)
        self._vision_no_store_cb = QCheckBox("disable_response_storage")
        vis_row4.addWidget(self._vision_no_store_cb)
        vis_layout.addLayout(vis_row4)

        body_layout.addWidget(vis_group)

        # ---- 模型选择 ----
        model_group = QGroupBox("模型选择")
        model_layout = QVBoxLayout(model_group)

        vis_model_row = QHBoxLayout()
        vis_model_row.addWidget(QLabel("视觉模型 ID:"))
        self._vision_model_input = QLineEdit()
        self._vision_model_input.setPlaceholderText("如 kimi-k2.5 / qwen-vl-max")
        vis_model_row.addWidget(self._vision_model_input, stretch=1)
        btn_pick_vision = QPushButton("选择模型...")
        btn_pick_vision.clicked.connect(self._open_vision_picker)
        vis_model_row.addWidget(btn_pick_vision)
        model_layout.addLayout(vis_model_row)

        audio_model_row = QHBoxLayout()
        audio_model_row.addWidget(QLabel("音频模型:"))
        self._audio_model_label = QLabel()
        self._audio_model_label.setStyleSheet("font-weight: bold; padding: 2px 8px;")
        audio_model_row.addWidget(self._audio_model_label, stretch=1)
        btn_pick_audio = QPushButton("选择模型...")
        btn_pick_audio.clicked.connect(self._open_audio_picker)
        audio_model_row.addWidget(btn_pick_audio)
        model_layout.addLayout(audio_model_row)

        self._refresh_model_labels()
        body_layout.addWidget(model_group)

        # ---- 并发 ----
        conc_group = QGroupBox("并发 & 性能")
        conc_layout = QVBoxLayout(conc_group)

        conc_row = QHBoxLayout()
        conc_row.addWidget(QLabel("LLM 并发数:"))
        self._llm_parallel_input = QSpinBox()
        self._llm_parallel_input.setRange(0, 100)
        self._llm_parallel_input.setToolTip("0 = 自动")
        conc_row.addWidget(self._llm_parallel_input)
        conc_row.addWidget(QLabel("错峰间隔(秒):"))
        self._llm_stagger_input = QDoubleSpinBox()
        self._llm_stagger_input.setRange(0.0, 10.0)
        self._llm_stagger_input.setDecimals(1)
        self._llm_stagger_input.setSingleStep(0.1)
        conc_row.addWidget(self._llm_stagger_input)
        conc_row.addStretch()
        conc_layout.addLayout(conc_row)

        batch_row = QHBoxLayout()
        batch_row.addWidget(QLabel("每批图片数 (PDF/板书):"))
        self._processing_batch_input = QSpinBox()
        self._processing_batch_input.setRange(1, 50)
        self._processing_batch_input.setValue(self._cfg.processing.batch_size)
        self._processing_batch_input.setToolTip("每批发给视觉模型的图片数量；越大越快但 token 消耗越高")
        batch_row.addWidget(self._processing_batch_input)
        batch_row.addWidget(QLabel("视频帧批大小:"))
        self._video_batch_input = QSpinBox()
        self._video_batch_input.setRange(1, 50)
        self._video_batch_input.setValue(self._cfg.video.batch_size)
        self._video_batch_input.setToolTip("视频帧每批发送数；kimi-k2.5 实测支持 20 张")
        batch_row.addWidget(self._video_batch_input)
        batch_row.addStretch()
        conc_layout.addLayout(batch_row)

        body_layout.addWidget(conc_group)

        # ---- API 池 ----
        pool_group = QGroupBox("API 池 / 付费模式")
        pool_layout = QVBoxLayout(pool_group)

        pool_row = QHBoxLayout()
        self._paid_mode_cb = QCheckBox("付费模式（启用 API 池加速）")
        self._paid_mode_cb.setToolTip("启用后多个 API Key 并行工作")
        pool_row.addWidget(self._paid_mode_cb)
        pool_row.addWidget(QLabel("额外 API Key (逗号分隔):"))
        self._extra_keys_input = QLineEdit()
        self._extra_keys_input.setPlaceholderText("sk-xxx, sk-yyy, ...")
        self._extra_keys_input.setEchoMode(QLineEdit.Password)
        pool_row.addWidget(self._extra_keys_input, stretch=1)
        pool_layout.addLayout(pool_row)

        body_layout.addWidget(pool_group)

        body_layout.addStretch()
        scroll.setWidget(body)
        layout.addWidget(scroll, stretch=1)

        # ---- 底部按钮 ----
        bottom_row = QHBoxLayout()
        bottom_row.addStretch()
        ok_btn = QPushButton("应用设置")
        ok_btn.setDefault(True)
        ok_btn.clicked.connect(self._on_apply)
        bottom_row.addWidget(ok_btn)
        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(self.reject)
        bottom_row.addWidget(cancel_btn)
        layout.addLayout(bottom_row)

    # ---- QSettings 持久化 ----

    def _restore_from_settings(self):
        if self._settings.contains("ui/api_key"):
            self._api_key_input.setText(self._settings.value("ui/api_key", type=str) or "")
        if self._settings.contains("ui/base_url"):
            self._base_url_input.setText(self._settings.value("ui/base_url", type=str) or "")
        if self._settings.contains("ui/vision_api_enabled"):
            self._vision_enabled_cb.setChecked(self._settings.value("ui/vision_api_enabled", type=bool))
        if self._settings.contains("ui/vision_provider"):
            self._vision_provider_input.setText(self._settings.value("ui/vision_provider", type=str) or "")
        if self._settings.contains("ui/vision_api_key"):
            self._vision_key_input.setText(self._settings.value("ui/vision_api_key", type=str) or "")
        if self._settings.contains("ui/vision_base_url"):
            self._vision_url_input.setText(self._settings.value("ui/vision_base_url", type=str) or "")
        if self._settings.contains("ui/vision_wire_api"):
            self._vision_wire_input.setText(self._settings.value("ui/vision_wire_api", type=str) or "")
        if self._settings.contains("ui/vision_reasoning_effort"):
            self._vision_reasoning_input.setText(self._settings.value("ui/vision_reasoning_effort", type=str) or "")
        if self._settings.contains("ui/vision_network_access"):
            self._vision_network_cb.setChecked(self._settings.value("ui/vision_network_access", type=bool))
        if self._settings.contains("ui/vision_disable_response_storage"):
            self._vision_no_store_cb.setChecked(self._settings.value("ui/vision_disable_response_storage", type=bool))
        if self._settings.contains("ui/vision_model"):
            saved = self._settings.value("ui/vision_model", type=str) or ""
            if saved:
                self._pending_vision_model = saved
                self._vision_model_input.setText(saved)
        if self._settings.contains("ui/audio_model"):
            self._pending_audio_model = self._settings.value("ui/audio_model", type=str) or ""
        self._refresh_model_labels()
        if self._settings.contains("ui/llm_parallel_requests"):
            self._llm_parallel_input.setValue(int(self._settings.value("ui/llm_parallel_requests")))
        if self._settings.contains("ui/llm_request_stagger_seconds"):
            self._llm_stagger_input.setValue(float(self._settings.value("ui/llm_request_stagger_seconds")))
        if self._settings.contains("ui/paid_mode"):
            self._paid_mode_cb.setChecked(self._settings.value("ui/paid_mode", type=bool))
        if self._settings.contains("ui/extra_api_keys"):
            self._extra_keys_input.setText(self._settings.value("ui/extra_api_keys", type=str) or "")
        if self._settings.contains("ui/processing_batch_size"):
            self._processing_batch_input.setValue(int(self._settings.value("ui/processing_batch_size")))
        if self._settings.contains("ui/video_batch_size"):
            self._video_batch_input.setValue(int(self._settings.value("ui/video_batch_size")))

    def _persist_to_settings(self):
        self._settings.setValue("ui/api_key", self._api_key_input.text())
        self._settings.setValue("ui/base_url", self._base_url_input.text())
        self._settings.setValue("ui/vision_api_enabled", self._vision_enabled_cb.isChecked())
        self._settings.setValue("ui/vision_provider", self._vision_provider_input.text())
        self._settings.setValue("ui/vision_api_key", self._vision_key_input.text())
        self._settings.setValue("ui/vision_base_url", self._vision_url_input.text())
        self._settings.setValue("ui/vision_wire_api", self._vision_wire_input.text())
        self._settings.setValue("ui/vision_reasoning_effort", self._vision_reasoning_input.text())
        self._settings.setValue("ui/vision_network_access", self._vision_network_cb.isChecked())
        self._settings.setValue("ui/vision_disable_response_storage", self._vision_no_store_cb.isChecked())
        self._settings.setValue("ui/vision_model", self._pending_vision_model)
        self._settings.setValue("ui/audio_model", self._pending_audio_model)
        self._settings.setValue("ui/llm_parallel_requests", self._llm_parallel_input.value())
        self._settings.setValue("ui/llm_request_stagger_seconds", self._llm_stagger_input.value())
        self._settings.setValue("ui/paid_mode", self._paid_mode_cb.isChecked())
        self._settings.setValue("ui/extra_api_keys", self._extra_keys_input.text())
        self._settings.setValue("ui/processing_batch_size", self._processing_batch_input.value())
        self._settings.setValue("ui/video_batch_size", self._video_batch_input.value())
        self._settings.sync()

    # ---- 模型选择 ----

    def _open_vision_picker(self):
        from OCRLLM.gui.model_picker import ModelPickerDialog

        def _validate_custom(name: str) -> bool:
            from OCRLLM.gui.model_validator import _validate_vision
            from OCRLLM.core.llm_client import LLMClient
            updates, info = self._read_overrides()
            if not info["new_key"] and not info["vision_api_key"]:
                QMessageBox.warning(self, "缺少 API Key", "请先填入 API Key 再测试自定义模型。")
                return False
            temp_cfg = self._cfg.with_updates(**updates)
            client = LLMClient(cfg=temp_cfg)
            return _validate_vision(self, client, name)

        dlg = ModelPickerDialog(self, kind="vision",
                                current_name=self._pending_vision_model,
                                on_validate_custom=_validate_custom)
        if dlg.exec_() == ModelPickerDialog.Accepted:
            self._pending_vision_model = dlg.selected_model_name
            self._vision_model_input.setText(dlg.selected_model_name)
            self._refresh_model_labels()

    def _open_audio_picker(self):
        from OCRLLM.gui.model_picker import ModelPickerDialog

        def _validate_custom(name: str) -> bool:
            from OCRLLM.gui.model_validator import _validate_audio
            from OCRLLM.core.llm_client import LLMClient
            api_key = self._api_key_input.text().strip()
            if not api_key:
                QMessageBox.warning(self, "缺少 API Key", "请先填入 API Key 再测试自定义模型。")
                return False
            temp_cfg = self._cfg.with_updates(
                api={"api_key": api_key,
                     "base_url": self._base_url_input.text().strip() or self._cfg.api.base_url})
            client = LLMClient(cfg=temp_cfg)
            return _validate_audio(self, client, name)

        dlg = ModelPickerDialog(self, kind="audio",
                                current_name=self._pending_audio_model,
                                on_validate_custom=_validate_custom)
        if dlg.exec_() == ModelPickerDialog.Accepted:
            self._pending_audio_model = dlg.selected_model_name
            self._refresh_model_labels()

    def _refresh_model_labels(self):
        a = self._pending_audio_model or "—"
        meta_a = model_catalog.find_audio_model(self._pending_audio_model)
        if meta_a:
            a = model_catalog.display_label(meta_a)
        self._audio_model_label.setText(a)

    # ---- 读取 / 应用 ----

    def _read_overrides(self) -> tuple[dict, dict]:
        new_key = self._api_key_input.text().strip()
        new_url = self._base_url_input.text().strip()
        vis_enabled = self._vision_enabled_cb.isChecked()
        vis_provider = self._vision_provider_input.text().strip()
        vis_key = self._vision_key_input.text().strip()
        vis_url = self._vision_url_input.text().strip()
        vis_wire = (self._vision_wire_input.text().strip() or "chat").lower()
        vis_reasoning = self._vision_reasoning_input.text().strip()
        vis_network = self._vision_network_cb.isChecked()
        vis_no_store = self._vision_no_store_cb.isChecked()
        vision_model = self._pending_vision_model
        audio_model = self._pending_audio_model
        new_parallel = self._llm_parallel_input.value()
        new_stagger = self._llm_stagger_input.value()
        processing_batch = self._processing_batch_input.value()
        video_batch = self._video_batch_input.value()
        paid_mode = self._paid_mode_cb.isChecked()
        extra_keys_text = self._extra_keys_input.text().strip()

        api_keys = [new_key] if new_key else []
        if extra_keys_text:
            for k in extra_keys_text.split(","):
                k = k.strip()
                if k and k != new_key:
                    api_keys.append(k)

        models_update: dict = {}
        if vision_model:
            models_update["vision_model"] = vision_model
            if not vis_enabled:
                models_update["text_model"] = vision_model
        if audio_model:
            models_update["asr_model"] = audio_model
            audio_meta = model_catalog.find_audio_model(audio_model)
            if audio_meta and audio_meta.kind == "asr_long":
                models_update["asr_short_model"] = "qwen3-asr-flash"
            else:
                models_update["asr_short_model"] = audio_model

        updates = {
            "api": {
                "api_key": new_key,
                "paid_mode": paid_mode,
                "api_keys": api_keys if paid_mode else [],
            },
            "vision_api": {
                "enabled": vis_enabled,
                "provider": vis_provider,
                "api_key": vis_key,
                "base_url": vis_url,
                "wire_api": vis_wire,
                "model_reasoning_effort": vis_reasoning,
                "network_access": vis_network,
                "disable_response_storage": vis_no_store,
            },
            "concurrency": {
                "llm_parallel_requests": new_parallel,
                "llm_request_stagger_seconds": new_stagger,
            },
            "processing": {
                "batch_size": processing_batch,
            },
            "video": {
                "batch_size": video_batch,
            },
        }
        if new_url:
            updates["api"]["base_url"] = new_url
        if models_update:
            updates["models"] = models_update

        info = {
            "new_key": new_key, "new_url": new_url,
            "vision_model": vision_model, "audio_model": audio_model,
            "vision_api_enabled": vis_enabled,
            "vision_api_key": vis_key,
            "vision_wire_api": vis_wire,
            "new_parallel": new_parallel, "new_stagger": new_stagger,
            "paid_mode": paid_mode, "api_keys": api_keys,
        }
        return updates, info

    def _on_apply(self):
        _updates, info = self._read_overrides()

        if not info["new_key"]:
            QMessageBox.warning(self, "提示", "API Key 不能为空")
            return

        if info["vision_api_enabled"]:
            if info["vision_wire_api"] not in {"chat", "responses"}:
                QMessageBox.warning(self, "提示", "视觉 Wire API 只能是 chat 或 responses")
                return
            if not info["vision_api_key"] or not self._vision_url_input.text().strip():
                QMessageBox.warning(self, "提示", "启用视觉独立 Provider 时，视觉 API Key 和 Base URL 不能为空")
                return

        self._persist_to_settings()
        self.accept()
