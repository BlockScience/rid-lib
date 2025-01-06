import pytest
from rid_lib.core import RID, ORN
from rid_lib.exceptions import RIDTypeError

def test_custom_uri_type_invalid_context():
    with pytest.raises(RIDTypeError):
        class CustomURIType(RID):        
            def __init__(self, internal_id: str):
                self.internal_id = internal_id
            
            @property
            def reference(self):
                return self.internal_id
            
            @classmethod
            def from_reference(cls, reference):
                return cls(reference)
                    
def test_custom_orn_type_invalid_context():
    with pytest.raises(RIDTypeError):
        class CustomORNType(ORN):        
            def __init__(self, internal_id: str):
                self.internal_id = internal_id
            
            @property
            def reference(self):
                return self.internal_id
            
            @classmethod
            def from_reference(cls, reference):
                return cls(reference)