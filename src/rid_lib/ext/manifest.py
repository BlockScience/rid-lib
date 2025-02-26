from datetime import datetime, timezone
from pydantic import BaseModel
from rid_lib.core import RID
from .utils import sha256_hash_json
from .pydantic_adapter import RIDField


class Manifest(BaseModel):
    rid: RIDField
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