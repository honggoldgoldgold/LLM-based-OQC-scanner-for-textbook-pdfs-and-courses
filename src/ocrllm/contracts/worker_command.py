"""Current worker command union."""

from typing import TypeAlias

from .cancel_command import CancelCommand
from .capabilities_command import CapabilitiesCommand
from .image_recognition_request import ImageRecognitionRequest


WorkerCommand: TypeAlias = CapabilitiesCommand | ImageRecognitionRequest | CancelCommand
