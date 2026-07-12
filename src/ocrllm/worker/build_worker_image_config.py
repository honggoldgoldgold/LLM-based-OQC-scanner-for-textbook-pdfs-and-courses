"""Build the exact Beijing image workflow from one worker request."""

from __future__ import annotations

from ocrllm.config import Config
from ocrllm.providers.dashscope.provider_settings import DashScopeSettings
from ocrllm.providers.dashscope.resolve_dashscope_model import DEFAULT_DASHSCOPE_MODEL
from ocrllm.vision_model_settings import VisionModelSettings

from ocrllm.contracts.image_recognition_request import ImageRecognitionRequest

from .file_uri_to_path import file_uri_to_path


def build_worker_image_config(command: ImageRecognitionRequest) -> Config:
    """Return one credential-free Config for the command's explicit workflow."""

    if type(command) is not ImageRecognitionRequest:
        raise TypeError("command must be an exact ImageRecognitionRequest")
    output_uri = command.options["output_directory_uri"]
    output_dir = None if output_uri is None else file_uri_to_path(output_uri)
    return Config(
        provider=DashScopeSettings(
            region="cn-beijing",
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            enable_thinking=True,
            vl_high_resolution_images=True,
            standalone_sign_scout_model=DEFAULT_DASHSCOPE_MODEL,
        ),
        vision_model=VisionModelSettings(name=command.model),
        profile="board",
        input_languages=command.input_languages,
        output_language=command.output_language,
        output_dir=output_dir,
        timeout_seconds=command.options["timeout_seconds"],
        overwrite=command.options["overwrite"],
    )
