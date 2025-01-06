from enum import StrEnum
from typing import Annotated
from rid_lib.core import RID
from .manifest import Manifest
from .pydantic_adapter import RIDFieldAnnotation, dataclass
from .utils import JSONSerializable


class EventType(StrEnum):
    NEW = "NEW"
    UPDATE = "UPDATE"
    FORGET = "FORGET"


@dataclass
class Event(JSONSerializable):
    rid: Annotated[RID, RIDFieldAnnotation]
    event_type: EventType
    manifest: Manifest | None = None