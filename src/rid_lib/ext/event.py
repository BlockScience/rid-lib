from enum import StrEnum
from typing import Annotated
from pydantic.dataclasses import dataclass
from rid_lib.core import RID
from .manifest import Manifest
from .pydantic_adapter import RIDFieldAnnotation
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