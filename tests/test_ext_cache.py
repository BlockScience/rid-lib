from rid_lib.core import RID
from rid_lib.ext import Manifest
from rid_lib.ext.cache import Cache, CacheEntry

def test_cache_entry_constructors():
    rid = RID.from_string("test:rid")
    data = {
        "val": "test"
    }
    
    cache_entry = CacheEntry(
        Manifest.generate(rid, data),
        data
    )
    
    cache_entry_json = cache_entry.to_json()
    
    assert cache_entry == CacheEntry.from_json(cache_entry_json)
    
def test_cache_functions():
    cache = Cache()
    rid = RID.from_string("test:rid")
    data = {
        "val": "test"
    }
    
    cache.drop()
    
    assert cache.exists(rid) == False
    
    cache_entry = cache.write(rid, data)
    
    assert cache_entry.manifest.rid == rid
    assert cache_entry.contents == data
    
    assert cache.exists(rid) == True
    
    assert cache.read(rid) == cache_entry
    
    assert cache.read_all_rids() == [rid]
    
    cache.delete(rid)
    
    assert cache.read(rid) == None
    
    cache.delete(rid)
    cache.drop()
