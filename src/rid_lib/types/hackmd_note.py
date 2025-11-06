from rid_lib.core import ORN


class HackMDNote(ORN):
    namespace = "hackmd.note"
    
    def __init__(self, note_id: str):
        self.note_id = note_id
        
    @property
    def reference(self):
        return self.note_id
    
    @classmethod
    def from_reference(cls, reference):
        return cls(reference)
