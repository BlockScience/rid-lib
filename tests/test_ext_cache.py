import pytest
from rid_lib.core import RID
from rid_lib.ext import Manifest
from rid_lib.ext.cache import Cache, CacheBundle
from rid_lib.ext.pydantic_adapter import USING_PYDANTIC


@pytest.mark.skipif(not USING_PYDANTIC, reason="Pydantic not available")
def test_cache_bundle_constructors():
    rid = RID.from_string("test:rid")
    data = {
        "val": "test"
    }
    
    cache_bundle = CacheBundle(
        Manifest.generate(rid, data),
        data
    )
    
    cache_bundle_json = cache_bundle.to_json()
    
    assert cache_bundle == CacheBundle.from_json(cache_bundle_json)

@pytest.mark.skipif(not USING_PYDANTIC, reason="Pydantic not available")
def test_cache_functions():
    cache = Cache(".rid_cache")
    rid = RID.from_string("test:rid")
    data = {
        "val": "test"
    }
    
    cache.drop()
    
    assert cache.exists(rid) == False
    
    cache_bundle = CacheBundle(
        Manifest.generate(rid, data), data
    )
    
    cache.write(rid, cache_bundle)
    
    assert cache_bundle.manifest.rid == rid
    assert cache_bundle.contents == data
    
    assert cache.exists(rid) == True
    
    assert cache.read(rid) == cache_bundle
    
    assert cache.read_all_rids() == [rid]
    
    cache.delete(rid)
    
    assert cache.read(rid) == None
    
    cache.delete(rid)
    cache.drop()

@pytest.mark.skipif(not USING_PYDANTIC, reason="Pydantic not available")
def test_invalid_cache_write():
    cache = Cache(".rid_cache")
    rid = RID.from_string("test:rid")
    other_rid = RID.from_string("test:other")
    data = {
        "val": "test"
    }
    
    cache_bundle = CacheBundle(
        Manifest.generate(other_rid, data), 
        data
    )
    
    with pytest.raises(ValueError):
        cache.write(rid, cache_bundle)