import json
import hashlib
from base64 import urlsafe_b64encode, urlsafe_b64decode
from dataclasses import asdict, is_dataclass
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

def json_serialize(obj):
    if isinstance(obj, RID):
        return str(obj)
    elif is_dataclass(obj) and not isinstance(obj, type):
        return json_serialize(asdict(obj))
    elif isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, (list, tuple)):
        return [json_serialize(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: json_serialize(value) for key, value in obj.items()}
    else:
        return obj


class JSONSerializable:
    def to_json(self) -> dict:
        return json_serialize(self)
    
    @classmethod
    def from_json(cls, data: dict):
        if USING_PYDANTIC:
            return cls(**data)
        else:
            raise ImportError("Pydantic is necessary for JSON deserialization, install with `pip install rid_lib[ext]`")
        