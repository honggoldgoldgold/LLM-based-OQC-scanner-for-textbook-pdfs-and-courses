"""
processors 子包 — 延迟导入以避免导入时拉取 cv2, fitz, rapidocr 等重型依赖。
"""

_EXPORTS = {
    "BaseProcessor": "OCRLLM.processors.base",
    "PDFProcessor": "OCRLLM.processors.pdf",
    "BoardProcessor": "OCRLLM.processors.board",
    "VideoProcessor": "OCRLLM.processors.video",
    "AudioProcessor": "OCRLLM.processors.audio",
    "PPTXProcessor": "OCRLLM.processors.future_formats",
    "PPTProcessor": "OCRLLM.processors.future_formats",
    "DOCXProcessor": "OCRLLM.processors.future_formats",
    "DOCProcessor": "OCRLLM.processors.future_formats",
    "HTMLProcessor": "OCRLLM.processors.future_formats",
    "ProcessorRegistry": "OCRLLM.processors.registry",
    "ProcessorSpec": "OCRLLM.processors.registry",
    "get_default_registry": "OCRLLM.processors.registry",
    "get_processor_spec": "OCRLLM.processors.registry",
    "get_processor_spec_for_path": "OCRLLM.processors.registry",
    "create_processor": "OCRLLM.processors.registry",
    "create_processor_for_path": "OCRLLM.processors.registry",
    "InputRoutingError": "OCRLLM.processors.routing",
    "RoutedInputs": "OCRLLM.processors.routing",
    "route_input_paths": "OCRLLM.processors.routing",
    "identify_input_type": "OCRLLM.processors.routing",
}


def __getattr__(name: str):
    mod_path = _EXPORTS.get(name)
    if mod_path:
        import importlib
        mod = importlib.import_module(mod_path)
        return getattr(mod, name)
    raise AttributeError(f"module 'OCRLLM.processors' has no attribute {name!r}")
