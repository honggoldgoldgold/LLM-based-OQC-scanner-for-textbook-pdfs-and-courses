"""Validate and confidence-filter one RapidOCR result object."""

from __future__ import annotations

import math
import unicodedata
from collections.abc import Sequence

from ..errors import OCRBackendError
from .rapidocr_image_result import RapidOCRImageResult


def parse_rapidocr_result(
    result: object,
    *,
    minimum_confidence: float,
) -> RapidOCRImageResult:
    """Return safe text/confidence tuples without exposing backend objects."""

    try:
        return _parse_rapidocr_result(
            result,
            minimum_confidence=minimum_confidence,
        )
    except OCRBackendError:
        raise
    except Exception:
        raise _invalid_result() from None


def _parse_rapidocr_result(
    result: object,
    *,
    minimum_confidence: float,
) -> RapidOCRImageResult:
    try:
        texts = getattr(result, "txts")
        scores = getattr(result, "scores")
    except Exception:
        raise _invalid_result() from None
    if texts is None and scores is None:
        return RapidOCRImageResult((), (), 0)
    if (
        not isinstance(texts, Sequence)
        or isinstance(texts, (str, bytes, bytearray))
        or not isinstance(scores, Sequence)
        or isinstance(scores, (str, bytes, bytearray))
        or len(texts) != len(scores)
    ):
        raise _invalid_result()

    lines: list[str] = []
    confidences: list[float] = []
    for text, score in zip(texts, scores, strict=True):
        if type(text) is not str or type(score) not in {int, float}:
            raise _invalid_result()
        confidence = float(score)
        if not math.isfinite(confidence) or not 0 <= confidence <= 1:
            raise _invalid_result()
        normalized_text = text.strip()
        if confidence < minimum_confidence or not _contains_visible_text(normalized_text):
            continue
        lines.append(normalized_text)
        confidences.append(confidence)
    return RapidOCRImageResult(
        lines=tuple(lines),
        confidences=tuple(confidences),
        detected_line_count=len(texts),
    )


def _contains_visible_text(value: str) -> bool:
    return any(
        unicodedata.category(character)[0] in {"L", "N", "S"}
        for character in value
    )


def _invalid_result() -> OCRBackendError:
    return OCRBackendError(
        "The local OCR backend returned an invalid result.",
        code="OCR_RESULT_INVALID",
        details={"engine": "rapidocr"},
    )
