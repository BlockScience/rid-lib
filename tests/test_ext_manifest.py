from datetime import datetime, timezone
import pytest
from rid_lib.core import RID
from rid_lib.ext import Manifest, utils
from rid_lib.ext.pydantic_adapter import USING_PYDANTIC

@pytest.mark.skipif(not USING_PYDANTIC, reason="Pydantic not available")
def test_manifest_constructors():
    rid = RID.from_string("test:rid")
    
    manifest = Manifest(
        rid=rid,
        timestamp=datetime.now(timezone.utc),
        sha256_hash=utils.sha256_hash_json({})
    )
    
    manifest_json = manifest.to_json()
    
    assert manifest == Manifest.from_json(manifest_json)

def test_manifest_generate():
    rid = RID.from_string("test:rid")
    data = {
        "val": "test"
    }
    
    manifest = Manifest.generate(rid, data)
    
    assert manifest == Manifest(
        rid=rid,
        timestamp=manifest.timestamp,
        sha256_hash=utils.sha256_hash_json(data)
    )