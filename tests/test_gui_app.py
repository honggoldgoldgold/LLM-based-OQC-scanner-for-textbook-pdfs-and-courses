import os
import tempfile
import unittest
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox

from OCRLLM.config import AppConfig
from OCRLLM.core.checkpoint import Checkpoint
from OCRLLM.gui.app import QCRMainWindow
from OCRLLM.gui.widgets import IncompleteTasksDialog


class _DummyWorker:
    def __init__(self, running=True):
        self.is_running = running
        self.cancel_requested = False

    def request_cancel(self):
        self.cancel_requested = True


class GuiAppCloseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._app = QApplication.instance() or QApplication([])

    def test_close_event_requests_async_cancel_instead_of_blocking(self):
        with tempfile.TemporaryDirectory() as tmp:
            cfg = AppConfig().with_updates(paths={"output_dir": tmp, "temp_dir": tmp})
            window = QCRMainWindow(cfg=cfg)
            window._worker = _DummyWorker(running=True)
            event = QCloseEvent()

            with patch.object(QMessageBox, "question", return_value=QMessageBox.Yes):
                window.closeEvent(event)

            self.assertFalse(event.isAccepted())
            self.assertTrue(window._worker.cancel_requested)
            self.assertTrue(window._close_after_worker)
            self.assertTrue(window._suppress_worker_dialogs)
            window.deleteLater()
            self._app.processEvents()

    def test_incomplete_tasks_dialog_select_all_resumes_multiple_tasks(self):
        checkpoints = [
            Checkpoint("pdf", "/tmp/a.pdf", "/tmp/a.md", 3),
            Checkpoint("video", "/tmp/b.mp4", "/tmp/b", 5),
        ]

        class _FakeManager:
            def list_incomplete(self):
                return checkpoints

        dlg = IncompleteTasksDialog(_FakeManager())
        dlg._select_all()
        dlg._on_resume()

        self.assertEqual(dlg.action, "resume")
        self.assertEqual(dlg.selected_checkpoints, checkpoints)
        self.assertEqual(dlg.selected_checkpoint, checkpoints[0])
        dlg.deleteLater()
        self._app.processEvents()

    def test_manage_tasks_resumes_multiple_selected_tasks_in_one_batch(self):
        checkpoints = [
            Checkpoint("pdf", "/tmp/a.pdf", "/tmp/a.md", 3),
            Checkpoint("video", "/tmp/b.mp4", "/tmp/b", 5),
        ]

        class _FakeDialog:
            Accepted = QDialog.Accepted

            def __init__(self, *_args, **_kwargs):
                self.action = "resume"
                self.selected_checkpoint = checkpoints[0]
                self.selected_checkpoints = checkpoints

            def exec_(self):
                return QDialog.Accepted

        with tempfile.TemporaryDirectory() as tmp:
            cfg = AppConfig().with_updates(paths={"output_dir": tmp, "temp_dir": tmp})
            window = QCRMainWindow(cfg=cfg)

            with patch("OCRLLM.gui.app.CheckpointManager"), \
                    patch("OCRLLM.gui.app.IncompleteTasksDialog", _FakeDialog), \
                    patch.object(window, "_resume_many", create=True) as resume_many, \
                    patch.object(window, "_on_resume_clicked"):
                window._on_manage_tasks()

            resume_many.assert_called_once_with(checkpoints)
            window.deleteLater()
            self._app.processEvents()

    def test_external_vision_provider_uses_pointed_model_instead_of_default_qwen(self):
        with tempfile.TemporaryDirectory() as tmp:
            cfg = AppConfig().with_updates(paths={"output_dir": tmp, "temp_dir": tmp})
            window = QCRMainWindow(cfg=cfg)
            window._api_key_input.setText("dash-key")
            window._vision_api_enabled_cb.setChecked(True)
            window._vision_provider_input.setText("oasis-vision-model")
            window._vision_api_key_input.setText("oasis-key")
            window._vision_base_url_input.setText("https://oasis.example/v1")
            window._pending_vision_model = "qwen-vl-max"

            window._sync_api_from_ui()

            self.assertEqual(window._cfg.models.vision_model, "oasis-vision-model")
            window.deleteLater()
            self._app.processEvents()

    def test_external_vision_provider_model_field_drives_vision_model_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            cfg = AppConfig().with_updates(paths={"output_dir": tmp, "temp_dir": tmp})
            window = QCRMainWindow(cfg=cfg)
            window._api_key_input.setText("dash-key")
            window._vision_api_enabled_cb.setChecked(True)
            window._vision_api_key_input.setText("provider-key")
            window._vision_base_url_input.setText("https://vision.example/v1")
            window._pending_vision_model = "ioasis"
            window._pending_audio_model = "qwen3-asr-flash-filetrans"

            window._vision_provider_input.setText("fuckme")
            self.assertEqual(window._vision_model_label.text(), "fuckme")
            self.assertIn("视觉: fuckme", window._api_summary.text())
            self.assertIn("视觉Provider: fuckme", window._api_summary.text())
            self.assertIn("音频: qwen3-asr-flash-filetrans", window._api_summary.text())

            window._sync_api_from_ui()

            self.assertEqual(window._cfg.models.vision_model, "fuckme")
            self.assertEqual(window._cfg.vision_api.provider, "fuckme")
            self.assertEqual(window._cfg.models.asr_model, "qwen3-asr-flash-filetrans")
            window.deleteLater()
            self._app.processEvents()


if __name__ == "__main__":
    unittest.main()
