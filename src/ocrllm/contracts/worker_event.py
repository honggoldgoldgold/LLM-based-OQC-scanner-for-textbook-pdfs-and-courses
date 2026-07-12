"""Current worker event union."""

from typing import TypeAlias

from .accepted_event import AcceptedEvent
from .capabilities_event import CapabilitiesEvent
from .error_event import ErrorEvent
from .progress_event import ProgressEvent
from .result_event import ResultEvent
from .warning_event import WarningEvent


WorkerEvent: TypeAlias = (
    CapabilitiesEvent
    | AcceptedEvent
    | ProgressEvent
    | WarningEvent
    | ResultEvent
    | ErrorEvent
)
