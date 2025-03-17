from datetime import datetime, timezone
from pydantic import BaseModel
from rid_lib.core import RID
from .utils import sha256_hash_json
from .pydantic_adapter import RIDField


class Manifest(BaseModel):
    # created on demand
    rid: RIDField       # implicit
    timestamp: datetime # get current time
    sha256_hash: str    # requires access to contents
    
    # optional?
    # version: str = "1.0.0"
    # source_node: RIDField   # must exist within a node
    # cacheable: bool
    # schema: ...
    # event_source: ...
    # provenance: list[RIDField]
    # common_fields: dict[str, str] = {
    #     "text": "text"
    # }
    # internal_rids: list[RIDField] = [
    #     "orn:slack.user"
    # ]
    
    
    @classmethod
    def generate(cls, rid: RID, data: dict):
        """Generates a Manifest using the current time and hashing the provided data."""
        return cls(
            rid=rid,
            timestamp=datetime.now(timezone.utc),
            sha256_hash=sha256_hash_json(data)
        )