"""
扫描型 PDF 检测器。
"""

from __future__ import annotations

import logging
import fitz

logger = logging.getLogger(__name__)


def is_scanned_pdf(
    pdf_path: str, sample_pages: int = 5, text_threshold: int = 50
) -> bool:
    """
    检测 PDF 是否为扫描型（图片型，无可提取文本）。

    策略: 抽样若干页面提取文本，平均字符数低于阈值认为是扫描版。
    """
    doc = fitz.open(pdf_path)
    try:
        total = len(doc)
        if total == 0:
            return True

        step = max(1, total // sample_pages)
        sampled = list(range(0, total, step))[:sample_pages]

        total_chars = 0
        for idx in sampled:
            total_chars += len(doc[idx].get_text("text").strip())
    finally:
        doc.close()

    avg_chars = total_chars / len(sampled) if sampled else 0
    result = avg_chars < text_threshold
    logger.info("[SCAN_DETECT] %s: 采样%d页, 平均字符数=%.0f, 扫描型=%s",
                 pdf_path, len(sampled), avg_chars, result)
    return result
