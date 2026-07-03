import os
import tempfile
import unittest
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QApplication, QMessageBox

from OCRLLM.config import AppConfig
from OCRLLM.gui.app import QCRMainWindow
from OCRLLM.gui.settings_dialog import SettingsDialog


class GoogleSettingsDialogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._app = QApplication.instance() or QApplication([])

    def setUp(self):
        settings = QSettings("OCRLLM", "QCR")
        settings.clear()
        settings.sync()

    def test_google_mode_applies_without_dashscope_key_and_is_independent_from_openai_provider(self):
        with tempfile.TemporaryDirectory() as tmp:
            cfg = AppConfig().with_updates(paths={"output_dir": tmp, "temp_dir": tmp})
            dlg = SettingsDialog(None, cfg)
            dlg._api_key_input.setText("")
            dlg._google_enabled_cb.setChecked(True)
            dlg._google_key_input.setText("AIza-test")
            dlg._google_vision_model_combo.setCurrentText("gemini-2.5-flash-image-preview")
            dlg._google_audio_model_combo.setCurrentText("gemini-3.5-flash")
            dlg._vision_enabled_cb.setChecked(True)
            dlg._vision_key_input.setText("openai-compatible-key")
            dlg._vision_url_input.setText("https://vision.example/v1")

            with patch.object(SettingsDialog, "_validate_google_environment_if_needed", return_value=True), \
                    patch.object(SettingsDialog, "accept") as accept, \
                    patch.object(QMessageBox, "warning") as warning:
                dlg._on_apply()

            accept.assert_called_once()
            warning.assert_not_called()
            applied = dlg.apply_config()

            self.assertTrue(applied.google_api.enabled)
            self.assertEqual(applied.google_api.api_key, "AIza-test")
            self.assertEqual(applied.google_api.vision_model, "gemini-2.5-flash-image-preview")
            self.assertEqual(applied.google_api.audio_model, "gemini-3.5-flash")
            self.assertTrue(applied.vision_api.enabled)
            self.assertEqual(applied.vision_api.api_key, "openai-compatible-key")
            dlg.deleteLater()
            self._app.processEvents()

    def test_google_parallel_delay_and_batch_settings_are_saved_to_google_config(self):
        cfg = AppConfig()
        dlg = SettingsDialog(None, cfg)
        dlg._google_enabled_cb.setChecked(True)
        dlg._google_key_input.setText("AIza-test")
        dlg._google_parallel_input.setValue(33)
        dlg._google_stagger_input.setValue(45.5)
        dlg._google_vision_batch_input.setValue(44)
        dlg._google_video_batch_input.setValue(55)

        applied = dlg.apply_config()

        self.assertEqual(applied.google_api.parallel_requests, 33)
        self.assertEqual(applied.google_api.request_stagger_seconds, 45.5)
        self.assertEqual(applied.google_api.vision_batch_size, 44)
        self.assertEqual(applied.google_api.video_frame_batch_size, 55)
        dlg.deleteLater()
        self._app.processEvents()

    def test_google_mode_toggle_runs_network_and_model_check_when_key_is_present(self):
        cfg = AppConfig()
        dlg = SettingsDialog(None, cfg)
        dlg._google_key_input.setText("AIza-test")

        with patch.object(dlg, "_refresh_google_models", return_value=True) as refresh:
            dlg._google_enabled_cb.setChecked(True)

        refresh.assert_called_once_with(force=False, notify=True)
        dlg.deleteLater()
        self._app.processEvents()

    def test_settings_dialog_prefills_api_fields_from_current_config_when_no_saved_settings(self):
        cfg = AppConfig().with_updates(
            api={"api_key": "dash-key", "base_url": "https://dash.example/v1"},
            google_api={
                "enabled": True,
                "api_key": "google-key",
                "vision_model": "gemini-vision",
                "audio_model": "gemini-audio",
            },
            vision_api={
                "enabled": True,
                "provider": "ioasis",
                "api_key": "vision-key",
                "base_url": "https://vision.example/v1",
            },
        )

        dlg = SettingsDialog(None, cfg)

        self.assertEqual(dlg._api_key_input.text(), "dash-key")
        self.assertEqual(dlg._base_url_input.text(), "https://dash.example/v1")
        self.assertTrue(dlg._google_enabled_cb.isChecked())
        self.assertEqual(dlg._google_key_input.text(), "google-key")
        self.assertEqual(dlg._google_vision_model_combo.currentText(), "gemini-vision")
        self.assertEqual(dlg._google_audio_model_combo.currentText(), "gemini-audio")
        self.assertTrue(dlg._vision_enabled_cb.isChecked())
        self.assertEqual(dlg._vision_provider_input.text(), "ioasis")
        self.assertEqual(dlg._vision_key_input.text(), "vision-key")
        self.assertEqual(dlg._vision_url_input.text(), "https://vision.example/v1")
        dlg.deleteLater()
        self._app.processEvents()

    def test_main_window_does_not_clear_config_api_values_when_qsettings_are_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            cfg = AppConfig().with_updates(
                paths={"output_dir": tmp, "temp_dir": tmp},
                api={"api_key": "dash-key", "base_url": "https://dash.example/v1"},
                google_api={
                    "enabled": True,
                    "api_key": "google-key",
                    "vision_model": "gemini-vision",
                    "audio_model": "gemini-audio",
                },
                vision_api={
                    "enabled": True,
                    "provider": "ioasis",
                    "api_key": "vision-key",
                    "base_url": "https://vision.example/v1",
                },
            )

            window = QCRMainWindow(cfg=cfg)

            self.assertEqual(window._cfg.api.api_key, "dash-key")
            self.assertEqual(window._cfg.api.base_url, "https://dash.example/v1")
            self.assertTrue(window._cfg.google_api.enabled)
            self.assertEqual(window._cfg.google_api.api_key, "google-key")
            self.assertEqual(window._cfg.google_api.vision_model, "gemini-vision")
            self.assertEqual(window._cfg.google_api.audio_model, "gemini-audio")
            self.assertTrue(window._cfg.vision_api.enabled)
            self.assertEqual(window._cfg.vision_api.api_key, "vision-key")
            window.deleteLater()
            self._app.processEvents()

    def test_applied_api_inputs_are_restored_by_next_settings_dialog(self):
        cfg = AppConfig()
        first = SettingsDialog(None, cfg)
        first._api_key_input.setText("dash-key")
        first._base_url_input.setText("https://dash.example/v1")
        first._google_enabled_cb.setChecked(True)
        first._google_key_input.setText("google-key")
        first._google_vision_model_combo.setCurrentText("gemini-vision")
        first._google_audio_model_combo.setCurrentText("gemini-audio")
        first._vision_enabled_cb.setChecked(True)
        first._vision_provider_input.setText("ioasis")
        first._vision_key_input.setText("vision-key")
        first._vision_url_input.setText("https://vision.example/v1")

        with patch.object(SettingsDialog, "_validate_google_environment_if_needed", return_value=True), \
                patch.object(SettingsDialog, "accept"):
            first._on_apply()

        second = SettingsDialog(None, AppConfig())

        self.assertEqual(second._api_key_input.text(), "dash-key")
        self.assertEqual(second._base_url_input.text(), "https://dash.example/v1")
        self.assertTrue(second._google_enabled_cb.isChecked())
        self.assertEqual(second._google_key_input.text(), "google-key")
        self.assertEqual(second._google_vision_model_combo.currentText(), "gemini-vision")
        self.assertEqual(second._google_audio_model_combo.currentText(), "gemini-audio")
        self.assertEqual(second._vision_provider_input.text(), "ioasis")
        self.assertEqual(second._vision_key_input.text(), "vision-key")
        self.assertEqual(second._vision_url_input.text(), "https://vision.example/v1")
        first.deleteLater()
        second.deleteLater()
        self._app.processEvents()


if __name__ == "__main__":
    unittest.main()
