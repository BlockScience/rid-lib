from rid_lib.core import ORN
from rid_lib.types.gdrive_export import GoogleDriveExport


document_mimeType = 'application/vnd.google-apps.document'
sheets_mimeType = 'application/vnd.google-apps.spreadsheet'
slides_mimeType = 'application/vnd.google-apps.presentation'

export_mimeType_map = {
    document_mimeType: {'text': {'plain': 'text/plain', 'markdown': 'text/markdown'}},
    sheets_mimeType: {'text': {'csv': 'text/csv', 'tab-separated-values': 'text/tab-separated-values'}},
    slides_mimeType: {'text': {'plain': 'text/plain'}}
}
export_mimeTypes = {
    document_mimeType: export_mimeType_map[document_mimeType]['text']['plain'], # 'text/plain'
    sheets_mimeType: export_mimeType_map[sheets_mimeType]['text']['csv'], # 'text/csv'
    slides_mimeType: export_mimeType_map[slides_mimeType]['text']['plain'], # 'text/plain'
}

class GoogleDriveFile(ORN):
    namespace = 'google_drive.file'
    mimeType = 'application/vnd.google-apps.file'
    export_mimeTypes = export_mimeTypes

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
                raise ValueError("Google Drive File reference must not be an empty string")
        else:
            raise ValueError("Google Drive File reference must be a string")