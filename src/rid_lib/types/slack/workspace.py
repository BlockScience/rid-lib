from rid_lib.core import RID

class SlackWorkspace(RID):
    space = "slack"
    form = "workspace"
    
    def __init__(
            self,
            workspace_id: str,
        ):
        self.workspace_id = workspace_id
            
    @property
    def reference(self):
        return self.workspace_id
        
    @classmethod
    def from_reference(cls, reference):
        return cls(reference)
                
RID.register_context(SlackWorkspace)
