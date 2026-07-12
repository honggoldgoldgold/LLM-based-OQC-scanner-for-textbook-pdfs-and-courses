"""Resolve installed RapidOCR distribution identity without importing it."""

from importlib.metadata import version


def resolve_rapidocr_version() -> str:
    """Return a stable version string for result metadata."""

    try:
        installed_version = version("rapidocr")
    except Exception:
        return "unknown"
    if not installed_version.strip():
        return "unknown"
    return installed_version
