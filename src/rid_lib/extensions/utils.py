import json
import hashlib
from base64 import urlsafe_b64encode, urlsafe_b64decode


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
