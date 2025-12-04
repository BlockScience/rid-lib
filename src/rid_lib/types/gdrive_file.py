from rid_lib.core import ORN
from rid_lib.types.gdrive_export import GoogleDriveExport


class GoogleDriveFile(ORN):
    namespace = 'google_drive.file'
    mimeType = 'application/vnd.google-apps.file'

    def __init__(self, id: str):
        self.id = id

    @property
    def url(self):
        return f'https://drive.google.com/file/d/{self.id}'
    
    @property
    def export(self, type: str, subtype: str) -> GoogleDriveExport:
        return GoogleDriveExport(
            type=type, 
            subtype=subtype, 
            fileId=self.id
        )

    @property
    def reference(self):
        return self.id

    @classmethod
    def from_reference(cls, id: str):
        if type(id) is str:
            if len(id) >= 1:
                return cls(id)
            else:
                raise ValueError("Google Drive File reference MUST NOT be an empty string")
        else:
            raise ValueError("Google Drive File reference MUST be a string")