import json
import hashlib
from base64 import urlsafe_b64encode, urlsafe_b64decode
from dataclasses import asdict, is_dataclass
from datetime import datetime
from pydantic import BaseModel
from rid_lib import RID


def sha256_hash_json(data: dict | BaseModel):
    if isinstance(data, BaseModel):
        data = json.loads(data.model_dump_json())
    json_str = json.dumps(data, separators=(',', ':'), sort_keys=True)
    json_bytes = json_str.encode()
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
