"""
OCRLLM GUI 入口。
"""

from __future__ import annotations

import sys
import argparse
import subprocess
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parent
WORKSPACE_ROOT = PACKAGE_ROOT.parent
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

from PyQt5.QtWidgets import QApplication

from OCRLLM.config import AppConfig
from OCRLLM.gui.app import QCRMainWindow


def main():
    """GUI 主入口 — 初始化 PyQt5 应用并显示主窗口。

    支持 ``--spawn N`` 启动多个独立窗口进程。
    """
    parser = argparse.ArgumentParser(description="OCRLLM 课程识别工具 (GUI)")
    parser.add_argument("--spawn", type=int, default=0, help="直接启动多个独立窗口")
    parser.add_argument("--child-index", type=int, default=0, help=argparse.SUPPRESS)
    args = parser.parse_args()

    if args.spawn > 0:
        kw = {}
        if sys.platform == "win32":
            kw["creationflags"] = (
                subprocess.DETACHED_PROCESS
                | subprocess.CREATE_NEW_PROCESS_GROUP
            )
            kw["close_fds"] = True
        for index in range(args.spawn):
            subprocess.Popen(
                [sys.executable, "-m", "OCRLLM.main", "--child-index", str(index)],
                cwd=str(WORKSPACE_ROOT), **kw)
        return

    cfg = AppConfig.from_env()
    app = QApplication(sys.argv)
    window = QCRMainWindow(cfg=cfg, window_index=args.child_index)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
