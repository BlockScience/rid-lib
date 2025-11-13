from src.rid_lib.core import ORN
from src.rid_lib.types.gdrive_file import GoogleDriveFile


class GoogleDriveExport(ORN):
    namespace = 'google_drive.export'
    
    def __init__(self, type: str, subtype: str, id: str):
        self.type = type
        self.subtype = subtype
        self.id = id

    @property
    def mimeType(self):
        return f'{self.type}/{self.subtype}'
    
    @property
    def reference(self):
        return f'{self.mimeType}/{self.id}'
    
    @property
    def file(self) -> GoogleDriveFile:
        return super().__init__(self.id)
    
    @classmethod
    def from_reference(cls, reference):
        components = reference.split("/")
        if len(components) == 3:
            return cls(*components)
        else:
            raise ValueError(
                "File Export reference must contain 3 '/'-separated components: '<type>/<subtype>/<id>'"
            )