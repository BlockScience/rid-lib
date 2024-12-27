from dataclasses import dataclass
from datetime import datetime, timezone
from rid_lib.core import RID
from .utils import sha256_hash_json


@dataclass
class Manifest:
    rid: RID
    timestamp: datetime
    sha256_hash: str
    
    @classmethod
    def generate(cls, rid: RID, data: dict):
        return cls(
            rid=rid,
            timestamp=datetime.now(timezone.utc),
            sha256_hash=sha256_hash_json(data)
        )
        
    @classmethod
    def from_json(cls, data: dict):
        return cls(
            rid=RID.from_string(data["rid"]),
            timestamp=datetime.fromisoformat(data["timestamp"]),
            sha256_hash=data["sha256_hash"]
        )
        
    def to_json(self):
        return {
            "rid": str(self.rid),
            "timestamp": self.timestamp.isoformat(),
            "sha256_hash": self.sha256_hash
        }