import pytest
from rid_lib.core import RID
from rid_lib.exceptions import InvalidRIDError

        
def test_prov_ctx_rid_string():
    rid_string = "test:reference"
    rid_obj = RID.from_string(rid_string)
    
    assert rid_obj.scheme == "test"
    assert rid_obj.namespace == None
    assert rid_obj.context == "test"
    assert rid_obj.reference == "reference"
    assert str(rid_obj) == rid_string
    
    repr(rid_obj)
    
    rid_obj2 = RID.from_string(rid_string)
    
    assert rid_obj == rid_obj2
    assert type(rid_obj) == type(rid_obj2)
        
def test_prov_ctx_orn_rid_string():
    rid_string = "orn:test:reference"
    rid_obj = RID.from_string(rid_string)
    
    assert rid_obj.scheme == "orn"
    assert rid_obj.namespace == "test"
    assert rid_obj.context == "orn:test"
    assert rid_obj.reference == "reference"
    assert str(rid_obj) == rid_string
    
    repr(rid_obj)
    
    rid_obj2 = RID.from_string(rid_string)
    
    assert rid_obj == rid_obj2
    assert type(rid_obj) == type(rid_obj2)
        
def test_missing_ctx_rid_string():
    with pytest.raises(InvalidRIDError):
        rid_obj = RID.from_string("test:reference", allow_prov_ctx=False)

def test_missing_ctx_orn_rid_string():
    with pytest.raises(InvalidRIDError):
        rid_obj = RID.from_string("orn:test:reference", allow_prov_ctx=False)
        