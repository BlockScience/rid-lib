from rid_lib.core import ORN, RID


class NormalizedText(ORN):
    namespace = "normalized.text"
    
    def __init__(self, wrapped_rid: RID):
        self.wrapped_rid = wrapped_rid
        
    @property
    def reference(self):
        return str(self.wrapped_rid)
    
    @classmethod
    def from_reference(cls, reference):
        return cls(RID.from_string(reference))