from uuid import uuid4
from rid_lib.core import ORN


class KoiNetNode(ORN):
    namespace = "koi-net.node"
    
    def __init__(self, name, uuid):
        self.name = name
        self.uuid = uuid
        
    @classmethod
    def generate(cls, name):
        return cls(name, uuid4())
        
    @property
    def reference(self):
        return f"{self.name}+{self.uuid}"
    
    @classmethod
    def from_reference(cls, reference):
        components = reference.split("+")
        if len(components) == 2:
            return cls(*components)
        else:
            raise ValueError("KOI-net Node reference must contain two '+'-separated components: '<name>+<uuid>'")