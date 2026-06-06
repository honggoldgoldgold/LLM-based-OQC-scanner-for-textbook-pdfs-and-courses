"""
RapidOCR 引擎封装 — 纯 Python 进程内 OCR，无外部 exe。
"""

from __future__ import annotations

import io
import logging
from pathlib import Path
from typing import List, Dict

import numpy as np
from PIL import Image

try:
    from rapidocr_onnxruntime import RapidOCR
except ImportError:
    raise ImportError("请安装 rapidocr_onnxruntime: pip install rapidocr_onnxruntime")

logger = logging.getLogger(__name__)


class RapidOCREngine:
    """纯 Python OCR 引擎（RapidOCR ONNX Runtime）。"""

    def __init__(self, use_angle: bool = False, max_side_len: int = 4096):
        self._ocr = RapidOCR(use_angle_clf=use_angle, max_side_len=max_side_len)

    def run_image(self, img_path: str) -> List[Dict]:
        """对图片文件执行 OCR 识别。

        Args:
            img_path: 图片文件路径。

        Returns:
            识别结果列表，每项含 box、text、score。
        """
        if not Path(img_path).exists():
            return []
        return self._format(self._ocr(str(img_path)))

    def run_bytes(self, img_bytes: bytes) -> List[Dict]:
        """对图片字节数据执行 OCR 识别。

        Args:
            img_bytes: 图片的原始字节。

        Returns:
            识别结果列表，每项含 box、text、score。
        """
        try:
            img = Image.open(io.BytesIO(img_bytes))
            arr = np.array(img)
        except Exception:
            return []
        return self._format(self._ocr(arr))

    def __enter__(self):
        return self

    def __exit__(self, *_):
        pass

    @staticmethod
    def _format(ocr_result) -> List[Dict]:
        if not ocr_result:
            return []
        results = ocr_result[0] if isinstance(ocr_result, tuple) else ocr_result
        if not results:
            return []
        blocks = []
        for box, text, score in results:
            box_list = [list(pt) if not isinstance(pt, list) else pt for pt in box]
            blocks.append({"box": box_list, "text": text, "score": float(score)})
        return blocks
