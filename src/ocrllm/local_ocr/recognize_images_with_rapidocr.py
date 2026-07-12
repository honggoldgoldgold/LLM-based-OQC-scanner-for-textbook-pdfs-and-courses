"""Recognize ordered images locally with one lazy RapidOCR engine."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

from ..config import Config
from ..errors import NoTextDetected, OCRBackendError
from ..processor_output import ProcessorOutput
from ..raise_if_cancelled import raise_if_cancelled
from .build_local_ocr_markdown import build_local_ocr_markdown
from .load_rapidocr import load_rapidocr
from .parse_rapidocr_result import parse_rapidocr_result
from .resolve_rapidocr_version import resolve_rapidocr_version


LOCAL_OCR_LIMITATION_WARNING = (
    "Local OCR extracts text lines but does not reconstruct formula, table, "
    "handwriting, or layout semantics like the vision workflow."
)


def recognize_images_with_rapidocr(
    image_paths: Sequence[Path],
    *,
    profile: str,
    config: Config,
) -> ProcessorOutput:
    """Return deterministic offline OCR output with no provider calls."""

    paths = tuple(Path(path) for path in image_paths)
    if type(config) is not Config or config.image_mode != "ocr" or config.local_ocr is None:
        raise TypeError("config must be an exact validated OCR-mode Config")
    raise_if_cancelled(config.cancellation)
    factory = load_rapidocr()
    settings = config.local_ocr
    try:
        engine = factory(
            params={
                "Global.log_level": "critical",
                "Global.text_score": settings.minimum_confidence,
            }
        )
        if not callable(engine):
            raise TypeError
    except Exception:
        raise OCRBackendError(
            "The local OCR backend could not be initialized.",
            code="OCR_BACKEND_FAILED",
            details={"engine": "rapidocr", "phase": "initialization"},
        ) from None

    image_results = []
    for image_index, path in enumerate(paths):
        raise_if_cancelled(config.cancellation)
        try:
            raw_result = engine(path)
        except Exception:
            raise OCRBackendError(
                "The local OCR backend could not recognize an image.",
                code="OCR_BACKEND_FAILED",
                details={
                    "engine": "rapidocr",
                    "phase": "inference",
                    "image_index": image_index,
                },
            ) from None
        image_results.append(
            parse_rapidocr_result(
                raw_result,
                minimum_confidence=settings.minimum_confidence,
            )
        )

    retained_confidences = tuple(
        confidence
        for result in image_results
        for confidence in result.confidences
    )
    if not retained_confidences:
        raise NoTextDetected(
            "Local OCR found no text above the configured confidence threshold.",
            details={
                "engine": "rapidocr",
                "image_count": len(paths),
                "minimum_confidence": settings.minimum_confidence,
            },
        ) from None
    markdown = build_local_ocr_markdown(image_results)
    return ProcessorOutput(
        media_type="image",
        profile=profile,
        markdown=markdown,
        warnings=(LOCAL_OCR_LIMITATION_WARNING,),
        metadata={
            "recognition_mode": "ocr",
            "ocr_engine": "rapidocr",
            "ocr_engine_version": resolve_rapidocr_version(),
            "image_count": len(paths),
            "detected_line_count": sum(
                result.detected_line_count for result in image_results
            ),
            "retained_line_count": len(retained_confidences),
            "empty_image_count": sum(not result.lines for result in image_results),
            "minimum_confidence": settings.minimum_confidence,
            "mean_confidence": sum(retained_confidences) / len(retained_confidences),
            "provider_call_count": 0,
            "network_call_count": 0,
        },
    )
