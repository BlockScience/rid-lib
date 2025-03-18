from datetime import datetime, timezone
import pytest
from rid_lib.core import RID

from rid_lib.ext import RID_EXT_ENABLED
if RID_EXT_ENABLED:
    from rid_lib.ext import Manifest, utils


@pytest.mark.skipif(not RID_EXT_ENABLED, reason="Missing rid-lib ext dependencies")
def test_manifest_constructors():
    rid = RID.from_string("test:rid")
    
    manifest = Manifest(
        rid=rid,
        timestamp=datetime.now(timezone.utc),
        sha256_hash=utils.sha256_hash_json({})
    )
    
    manifest_json = manifest.model_dump()
    
    assert manifest == Manifest.model_validate(manifest_json)

@pytest.mark.skipif(not RID_EXT_ENABLED, reason="Missing rid-lib ext dependencies")
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