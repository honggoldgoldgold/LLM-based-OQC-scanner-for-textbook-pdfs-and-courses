import os
import tempfile
import unittest
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QApplication, QMessageBox

from OCRLLM.config import AppConfig
from OCRLLM.gui.settings_dialog import SettingsDialog


class CodexSettingsDialogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._app = QApplication.instance() or QApplication([])

    def setUp(self):
        settings = QSettings("OCRLLM", "QCR")
        settings.clear()
        settings.sync()

    def test_codex_toggle_only_swaps_visual_model_and_can_restore(self):
        with tempfile.TemporaryDirectory() as tmp:
            cfg = AppConfig().with_updates(paths={"output_dir": tmp, "temp_dir": tmp})
            dlg = SettingsDialog(None, cfg)
            dlg._vision_provider_input.setText("ioasis")
            dlg._vision_url_input.setText("https://vision.example/v1")
            dlg._vision_model_combo.setCurrentText("qwen-vl-max")
            dlg._pending_vision_model = "qwen-vl-max"

            dlg._codex_enabled_cb.setChecked(True)

            self.assertEqual(dlg._pending_vision_model, "gpt-5.5")
            self.assertEqual(dlg._vision_provider_input.text(), "ioasis")
            self.assertEqual(dlg._vision_url_input.text(), "https://vision.example/v1")

            dlg._codex_enabled_cb.setChecked(False)

            self.assertEqual(dlg._pending_vision_model, "qwen-vl-max")
            self.assertEqual(dlg._vision_provider_input.text(), "ioasis")
            dlg.deleteLater()
            self._app.processEvents()

    def test_codex_mode_apply_does_not_require_api_key_and_runs_first_check(self):
        with tempfile.TemporaryDirectory() as tmp:
            cfg = AppConfig().with_updates(paths={"output_dir": tmp, "temp_dir": tmp})
            dlg = SettingsDialog(None, cfg)
            dlg._api_key_input.setText("")
            dlg._codex_enabled_cb.setChecked(True)
            dlg._codex_reasoning_combo.setCurrentText("medium")

            with patch("OCRLLM.gui.settings_dialog.inspect_codex_cli") as inspect, \
                    patch.object(SettingsDialog, "accept") as accept, \
                    patch.object(QMessageBox, "warning") as warning:
                inspect.return_value.ok = True
                inspect.return_value.message = "ok"
                dlg._on_apply()

            inspect.assert_called_once()
            self.assertEqual(inspect.call_args.args[0].model, "gpt-5.5")
            accept.assert_called_once()
            warning.assert_not_called()
            dlg.deleteLater()
            self._app.processEvents()

    def test_settings_dialog_migrates_stored_codex_mini_default(self):
        settings = QSettings("OCRLLM", "QCR")
        settings.setValue("ui/codex_model", "gpt-5.4-mini")
        settings.sync()

        with tempfile.TemporaryDirectory() as tmp:
            cfg = AppConfig().with_updates(paths={"output_dir": tmp, "temp_dir": tmp})
            dlg = SettingsDialog(None, cfg)

            self.assertEqual(dlg._codex_model_combo.currentText(), "gpt-5.5")
            dlg.deleteLater()
            self._app.processEvents()

    def test_settings_dialog_is_resizable_and_larger_by_default(self):
        cfg = AppConfig()
        dlg = SettingsDialog(None, cfg)

        self.assertTrue(dlg.isSizeGripEnabled())
        self.assertGreaterEqual(dlg.minimumWidth(), 840)
        self.assertGreaterEqual(dlg.minimumHeight(), 640)
        dlg.deleteLater()
        self._app.processEvents()


if __name__ == "__main__":
    unittest.main()
