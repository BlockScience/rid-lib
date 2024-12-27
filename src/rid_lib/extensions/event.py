from dataclasses import dataclass
from enum import StrEnum
from rid_lib.core import RID
from .manifest import Manifest


class EventType(StrEnum):
    NEW = "NEW"
    UPDATE = "UPDATE"
    FORGET = "FORGET"

@dataclass
class Event:
    rid: RID
    event_type: EventType
    manifest: Manifest | None = None
    
    @classmethod
    def from_json(cls, data: dict):
        return cls(
            rid=data["rid"],
            event_type=data["event_type"],
        )
    
    def to_json(self):
        return {
            "rid": str(self.rid),
            "event_type": self.event_type,
            "manifest": self.manifest.to_json() if self.manifest else None
        }