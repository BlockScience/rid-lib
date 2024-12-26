import json
import hashlib
from base64 import urlsafe_b64encode, urlsafe_b64decode


def hash_json(data: dict):
    json_bytes = json.dumps(data, sort_keys=True).encode()
    hash = hashlib.sha256()
    hash.update(json_bytes)
    return hash.hexdigest()

def encode_b64(string: str):
    return urlsafe_b64encode(
        string.encode()).decode().rstrip("=")

def decode_b64(string: str):
    return urlsafe_b64decode(
        (string + "=" * (-len(string) % 4)).encode()).decode()
