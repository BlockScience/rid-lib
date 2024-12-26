from dataclasses import dataclass
from datetime import datetime, timezone
from .core import RID
from .utils import hash_json


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
            sha256_hash=hash_json(data)
        )
        
    @classmethod
    def from_dict(cls, d: dict):
        return cls(
            rid=RID.from_string(d.get("rid")),
            timestamp=datetime.fromisoformat(d.get("timestamp")),
            sha256_hash=d.get("sha256_hash")
        )
        
    def to_dict(self):
        return {
            "rid": str(self.rid),
            "timestamp": self.timestamp.isoformat(),
            "sha256_hash": self.sha256_hash
        }