"""
core 子包 — 延迟导入以避免导入时拉取重型依赖（openai, httpx）。
"""

_EXPORTS = {
    "LLMClient": "OCRLLM.core.llm_client",
    "ensure_dir": "OCRLLM.core.utils",
    "batch_list": "OCRLLM.core.utils",
    "concat_md_files": "OCRLLM.core.utils",
    "resize_image_if_needed": "OCRLLM.core.utils",
    "sort_files_by_time": "OCRLLM.core.utils",
    "strip_md_fence": "OCRLLM.core.utils",
    "setup_logging": "OCRLLM.core.utils",
    "get_ffmpeg": "OCRLLM.core.utils",
}


def __getattr__(name: str):
    mod_path = _EXPORTS.get(name)
    if mod_path:
        import importlib
        mod = importlib.import_module(mod_path)
        return getattr(mod, name)
    raise AttributeError(f"module 'OCRLLM.core' has no attribute {name!r}")
