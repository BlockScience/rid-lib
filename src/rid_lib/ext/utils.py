import json
import hashlib
from base64 import urlsafe_b64encode, urlsafe_b64decode
from dataclasses import asdict
from datetime import datetime
from rid_lib import RID
from .pydantic_adapter import USING_PYDANTIC


def sha256_hash_json(data: dict):
    json_bytes = json.dumps(data, sort_keys=True).encode()
    hash = hashlib.sha256()
    hash.update(json_bytes)
    return hash.hexdigest()

def b64_encode(string: str):
    return urlsafe_b64encode(
        string.encode()).decode().rstrip("=")

def b64_decode(string: str):
    return urlsafe_b64decode(
        (string + "=" * (-len(string) % 4)).encode()).decode()

def serialize(obj):
    if isinstance(obj, RID):
        return str(obj)
    elif isinstance(obj, JSONSerializable):
        return obj.to_json()
    elif isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, (list, tuple)):
        return [serialize(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: serialize(value) for key, value in obj.items()}
    else:
        return obj

class JSONSerializable:
    def to_json(self) -> dict:
        return serialize(asdict(self))
    
    @classmethod
    def from_json(cls, data: dict):
        if USING_PYDANTIC:
            return cls(**data)
        else:
            raise ImportError(
                "Pydantic is required to use the from_json() function for JSONSerializable dataclasses. This can be installed as an optional dependency via `pip install rid-lib[pydantic]`"
            )
        