import json
import hashlib
from rid_lib.core import ORN
from .koi_net_node import KoiNetNode


class KoiNetEdge(ORN):
    namespace = "koi-net.edge"
    
    def __init__(self, id):
        self.id = id
        
    @classmethod
    def generate(cls, source: KoiNetNode, target: KoiNetNode):
        edge_json = {
            "source": str(source),
            "target": str(target)
        }
        json_bytes = json.dumps(edge_json).encode()
        hash = hashlib.sha256()
        hash.update(json_bytes)
        hash.hexdigest()
        
        return cls(hash.hexdigest())
        
    @property
    def reference(self):
        return self.id
    
    @classmethod
    def from_reference(cls, reference):
        return cls(reference)