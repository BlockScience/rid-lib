from rid_lib.core import ORN


class HackMDNote(ORN):
    namespace = "hackmd.note"

    def __init__(self, note_id: str, workspace_id: str | None = None):
        self.note_id = note_id
        self.workspace_id = workspace_id

    @property
    def reference(self) -> str:
        if self.workspace_id:
            return f"{self.workspace_id}/{self.note_id}"
        return self.note_id

    @classmethod
    def from_reference(cls, reference: str) -> "HackMDNote":
        if "/" in reference:
            workspace_id, note_id = reference.split("/", 1)
            return cls(note_id=note_id, workspace_id=workspace_id)
        return cls(note_id=reference)
