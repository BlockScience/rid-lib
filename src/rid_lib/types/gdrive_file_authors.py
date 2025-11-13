from src.rid_lib.core import ORN
from src.rid_lib.types.gdrive_file import GoogleDriveFile

class FileAuthors(ORN):
    namespace = 'google_drive.file.authors'

    def __init__(self, id: str):
        self.id = id

    @property
    def file(self) -> GoogleDriveFile:
        return GoogleDriveFile(self.id)

    @property
    def reference(self):
        return self.id
            
    @classmethod
    def from_reference(cls, id):
        if len(id) >= 1:
            return cls(id)
        return None