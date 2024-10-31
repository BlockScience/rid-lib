from rid_lib.core import RID

class SlackUser(RID):
    namespace = "slack.user"
    space = "slack"
    form = "user"
    
    def __init__(
            self,
            workspace_id: str,
            user_id: str,
        ):
        self.workspace_id = workspace_id
        self.user_id = user_id
            
    @property
    def reference(self):
        return f"{self.workspace_id}/{self.user_id}"
        
    @classmethod
    def from_reference(cls, reference):
        components = reference.split("/")
        if len(components) == 2:
            return cls(*components)
                
RID.register_context(SlackUser)
