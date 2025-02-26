from enum import StrEnum
from pydantic import BaseModel
from .bundle import Bundle
from .pydantic_adapter import RIDField


class EventType(StrEnum):
    NEW = "NEW"
    UPDATE = "UPDATE"
    FORGET = "FORGET"


class Event(BaseModel):
    rid: RIDField
    event_type: EventType
    bundle: Bundle | None = None