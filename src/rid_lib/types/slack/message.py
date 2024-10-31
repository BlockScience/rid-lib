from rid_lib.core import RID

class SlackMessage(RID):
    namespace = "slack.message"
    space = "slack"
    form = "message"
    
    def __init__(
            self,
            workspace_id: str,
            channel_id: str,
            message_id: str,
        ):
        self.workspace_id = workspace_id
        self.channel_id = channel_id
        self.message_id = message_id
            
    @property
    def reference(self):
        return f"{self.workspace_id}/{self.channel_id}/{self.message_id}"
        
    @classmethod
    def from_reference(cls, reference):
        components = reference.split("/")
        if len(components) in (3, 4):
            return cls(*components)
                
RID.register_context(SlackMessage)
