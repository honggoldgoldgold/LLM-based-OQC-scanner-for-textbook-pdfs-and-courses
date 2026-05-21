"""
gui 子包 — 延迟导入以避免导入时拉取 PyQt5。
"""

_EXPORTS = {
    "QCRMainWindow": "OCRLLM.gui.app",
    "FileInput": "OCRLLM.gui.widgets",
    "GuiWorker": "OCRLLM.gui.worker",
}


def __getattr__(name: str):
    mod_path = _EXPORTS.get(name)
    if mod_path:
        import importlib
        mod = importlib.import_module(mod_path)
        return getattr(mod, name)
    raise AttributeError(f"module 'OCRLLM.gui' has no attribute {name!r}")
