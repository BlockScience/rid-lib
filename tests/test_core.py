import pytest
from rid_lib.core import RID
from rid_lib.exceptions import InvalidRIDError

def test_uri_rid_string():
    rid_string = "https://github.com/BlockScience/rid-lib/"
    rid_obj = RID.from_string(rid_string)
    
    assert rid_obj.scheme == "https"
    assert rid_obj.namespace == None
    assert rid_obj.context == "https"
    assert rid_obj.reference == "//github.com/BlockScience/rid-lib/"
    assert str(rid_obj) == rid_string
    assert repr(rid_obj) == f"<HTTPS RID '{rid_string}'>"
    
def test_orn_rid_string():
    rid_string = "orn:slack.message:TMQ3PKXT9/C0175M3GLSU/1698205575.367209"
    rid_obj = RID.from_string(rid_string)
    
    assert rid_obj.scheme == "orn"
    assert rid_obj.namespace == "slack.message"
    assert rid_obj.context == "orn:slack.message"
    assert rid_obj.reference == "TMQ3PKXT9/C0175M3GLSU/1698205575.367209"
    assert str(rid_obj) == rid_string
    assert repr(rid_obj) == f"<SlackMessage RID '{rid_string}'>"
    
def test_rid_equality():
    rid_string = "https://github.com/BlockScience/rid-lib/"
    rid_obj = RID.from_string(rid_string)
    rid_obj2 = RID.from_string(rid_string)
    
    assert rid_obj == rid_obj2
    
def test_rid_inequality():
    rid_obj = RID.from_string("https://github.com/BlockScience/rid-lib/")
    rid_obj2 = RID.from_string("orn:slack.message:TMQ3PKXT9/C0175M3GLSU/1698205575.367209")
    
    assert rid_obj != rid_obj2
    
def test_invalid_rid_string():    
    with pytest.raises(InvalidRIDError):
        rid_obj = RID.from_string("test")
        
def test_invalid_orn_rid_string():
    with pytest.raises(InvalidRIDError):
        rid_obj = RID.from_string("orn:test")
        
# def test_abstractmethod_from_reference():
#     RID.from_reference("reference")
    
    
    