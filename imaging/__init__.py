"""
imaging 子包 — 按需导入以避免缺少可选依赖时崩溃。
"""


def __getattr__(name):
    """延迟导入，仅在实际使用时加载。"""
    if name == "RapidOCREngine":
        from OCRLLM.imaging.ocr_engine import RapidOCREngine
        return RapidOCREngine
    if name == "run_tbpu":
        from OCRLLM.imaging.tbpu import run_tbpu
        return run_tbpu
    if name == "pdf_to_images":
        from OCRLLM.imaging.pdf_renderer import pdf_to_images
        return pdf_to_images
    if name == "is_scanned_pdf":
        from OCRLLM.imaging.scan_detector import is_scanned_pdf
        return is_scanned_pdf
    if name == "ImagePreprocessor":
        from OCRLLM.imaging.preprocess import ImagePreprocessor
        return ImagePreprocessor
    if name == "imwrite_unicode":
        from OCRLLM.imaging.preprocess import imwrite_unicode
        return imwrite_unicode
    if name == "convert_heic_to_jpg":
        from OCRLLM.imaging.preprocess import convert_heic_to_jpg
        return convert_heic_to_jpg
    if name == "extract_audio":
        from OCRLLM.imaging.audio_extractor import extract_audio
        return extract_audio
    raise AttributeError(f"module 'OCRLLM.imaging' has no attribute {name!r}")
