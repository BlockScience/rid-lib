from src.rid_lib.core import ORN
from src.rid_lib.types.gdrive_export import GoogleDriveExport

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
            id=self.id
        )

    @property
    def reference(self):
        return self.id

    @classmethod
    def from_reference(cls, id):
        if len(id) >= 1:
            return cls(id)
        return None