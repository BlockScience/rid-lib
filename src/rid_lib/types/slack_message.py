from rid_lib.core import RID

class SlackMessage(RID):
    namespace = "slack.message"
    
    def __init__(
            self,
            team_id: str,
            channel_id: str,
            ts: str,
        ):
        self.team_id = team_id
        self.channel_id = channel_id
        self.ts = ts
            
    @property
    def reference(self):
        return f"{self.team_id}/{self.channel_id}/{self.ts}"
        
    @classmethod
    def from_reference(cls, reference):
        components = reference.split("/")
        if len(components) in (3, 4):
            return cls(*components)
                
RID.register_context(SlackMessage)
