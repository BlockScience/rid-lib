from rid_lib.core import RID

class SlackChannel(RID):
    namespace = "slack.channel"
    space = "slack"
    form = "channel"
    
    def __init__(
            self,
            workspace_id: str,
            channel_id: str,
        ):
        self.workspace_id = workspace_id
        self.channel_id = channel_id
            
    @property
    def reference(self):
        return f"{self.workspace_id}/{self.channel_id}"
        
    @classmethod
    def from_reference(cls, reference):
        components = reference.split("/")
        if len(components) == 2:
            return cls(*components)
                
RID.register_context(SlackChannel)
