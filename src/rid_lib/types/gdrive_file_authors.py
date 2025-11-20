from rid_lib.core import ORN
from rid_lib.types.gdrive_file import GoogleDriveFile


class GoogleDriveFileAuthors(ORN):
    namespace = 'google_drive.file.authors'

    def __init__(self, fileId: str):
        self.fileId = fileId

    @property
    def file(self) -> GoogleDriveFile:
        return GoogleDriveFile(self.fileId)

    @property
    def reference(self):
        return self.fileId
            
    @classmethod
    def from_reference(cls, fileId: str):
        if type(fileId) is str:
            if len(fileId) >= 1:
                return cls(fileId)
            else:
                raise ValueError("Google Drive File Authors reference must not be an empty string")
        else:
            raise ValueError("Google Drive File Authors reference must be a string")