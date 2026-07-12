"""Build deterministic Markdown from ordered local-OCR image lines."""

from __future__ import annotations

from collections.abc import Sequence

from .rapidocr_image_result import RapidOCRImageResult


def build_local_ocr_markdown(results: Sequence[RapidOCRImageResult]) -> str:
    """Preserve OCR reading order and make multi-image boundaries explicit."""

    image_results = tuple(results)
    if not image_results or any(
        type(result) is not RapidOCRImageResult for result in image_results
    ):
        raise TypeError("results must contain exact RapidOCRImageResult values")
    if len(image_results) == 1:
        return "\n\n".join(image_results[0].lines)

    sections: list[str] = []
    for index, result in enumerate(image_results, start=1):
        body = "\n\n".join(result.lines)
        sections.append(f"## Image {index}" + (f"\n\n{body}" if body else ""))
    return "\n\n".join(sections)
