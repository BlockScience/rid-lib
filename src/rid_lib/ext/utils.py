import json
import hashlib
from base64 import urlsafe_b64encode, urlsafe_b64decode
from pydantic import BaseModel
from vendor.org.webpki.json.Canonicalize import canonicalize


def sha256_hash_json(data: dict | BaseModel):
    if isinstance(data, BaseModel):
        data = json.loads(data.model_dump_json())
    json_bytes = canonicalize(data)
    hash = hashlib.sha256()
    hash.update(json_bytes)
    return hash.hexdigest()

def b64_encode(string: str):
    return urlsafe_b64encode(
        string.encode()).decode().rstrip("=")

def b64_decode(string: str):
    return urlsafe_b64decode(
        (string + "=" * (-len(string) % 4)).encode()).decode()