"""Lazy-load the supported OpenAI client used by the DashScope adapter."""

from __future__ import annotations

from types import ModuleType

from ...errors import DependencyMissing


def load_openai() -> ModuleType:
    """Return OpenAI 2.30+ and below 3, or raise a typed dependency error."""
    try:
        import openai
    except (ImportError, OSError) as error:
        raise DependencyMissing(
            "DashScope vision requires the optional 'dashscope' extra.",
            details={"extra": "dashscope"},
        ) from error

    version = getattr(openai, "__version__", None)
    if not _is_supported_openai_version(version) or not callable(
        getattr(openai, "OpenAI", None)
    ):
        details = {"extra": "dashscope"}
        if type(version) is str and 0 < len(version) <= 64:
            details["installed_version"] = version
        raise DependencyMissing(
            "DashScope vision requires openai>=2.30,<3.",
            details=details,
        ) from None
    return openai


def _is_supported_openai_version(version: object) -> bool:
    if type(version) is not str:
        return False
    release = version.split("+", 1)[0].split("-", 1)[0].split(".")
    if len(release) < 2 or not release[0].isdigit() or not release[1].isdigit():
        return False
    return int(release[0]) == 2 and int(release[1]) >= 30
