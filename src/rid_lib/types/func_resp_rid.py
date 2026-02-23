from rid_lib.core import ORN


class FuncRespRid(ORN):
    namespace = "func.resp"

    def __init__(self, uuid: str):
        self.uuid = uuid

    @property
    def reference(self):
        return self.uuid

    @classmethod
    def from_reference(cls, reference):
        return cls(reference)
