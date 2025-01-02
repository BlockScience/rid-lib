from enum import StrEnum
from rid_lib.core import RID
from .manifest import Manifest
from .pydantic_adapter import dataclass, RIDField
from .utils import JSONSerializable

class EventType(StrEnum):
    NEW = "NEW"
    UPDATE = "UPDATE"
    FORGET = "FORGET"

@dataclass
class Event(JSONSerializable):
    rid: RIDField
    event_type: EventType
    manifest: Manifest | None = None