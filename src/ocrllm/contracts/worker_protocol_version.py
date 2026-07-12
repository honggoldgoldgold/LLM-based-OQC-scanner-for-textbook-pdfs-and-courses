"""Worker protocol version names."""

from typing import Literal, TypeAlias


WorkerProtocolVersion: TypeAlias = Literal["ocrllm.v1alpha1", "ocrllm.v1alpha2"]
CURRENT_WORKER_PROTOCOL_VERSION: Literal["ocrllm.v1alpha1"] = "ocrllm.v1alpha1"
KNOWN_WORKER_PROTOCOL_VERSIONS = frozenset({"ocrllm.v1alpha1", "ocrllm.v1alpha2"})
SUPPORTED_WORKER_PROTOCOL_VERSIONS = frozenset({CURRENT_WORKER_PROTOCOL_VERSION})
