import os
import tempfile
import unittest
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QApplication, QMessageBox

from OCRLLM.config import AppConfig
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


if __name__ == "__main__":
    unittest.main()
