from datetime import datetime, timezone
from typing import Annotated
from rid_lib.core import RID
from .utils import sha256_hash_json, JSONSerializable
from .pydantic_adapter import RIDFieldAnnotation, dataclass


@dataclass
class Manifest(JSONSerializable):
    rid: Annotated[RID, RIDFieldAnnotation]
    timestamp: datetime
    sha256_hash: str
    
    @classmethod
    def generate(cls, rid: RID, data: dict):
        """Generates a Manifest using the current time and hashing the provided data."""
        return cls(
            rid=rid,
            timestamp=datetime.now(timezone.utc),
            sha256_hash=sha256_hash_json(data)
        )