from rid_lib.core import ORN


class SearchQuery(ORN):
    namespace = "search.query"

    def __init__(self, uuid: str):
        self.uuid = uuid

    @property
    def reference(self):
        return self.uuid

    @classmethod
    def from_reference(cls, reference):
        return cls(reference)
