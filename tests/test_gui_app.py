import os
import tempfile
import unittest
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QApplication, QMessageBox

from OCRLLM.config import AppConfig
from OCRLLM.gui.app import QCRMainWindow


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


if __name__ == "__main__":
    unittest.main()