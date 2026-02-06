from rid_lib.core import ORN


class GoogleDriveExport(ORN):
    namespace = 'google_drive.export'
    
    def __init__(self, type: str, subtype: str, fileId: str):
        self.type = type
        self.subtype = subtype
        self.fileId = fileId

    @property
    def mimeType(self):
        return f'{self.type}/{self.subtype}'
    
    @property
    def reference(self):
        return f'{self.mimeType}/{self.fileId}'
    
    @classmethod
    def from_reference(cls, reference):
        if type(reference) is str:
            components = reference.split("/")
            if len(components) == 3:
                return cls(*components)
            else:
                raise ValueError(
                    "Google Drive File Export reference must contain 3 '/'-separated components: '<type>/<subtype>/<fileId>'"
                )
        else:
            raise ValueError("Google Drive File Export reference must be a string")