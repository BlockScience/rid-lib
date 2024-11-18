from rid_lib.core import RID

class SlackChannel(RID):
    space = "slack"
    form = "channel"
    
    def __init__(
            self,
            team_id: str,
            channel_id: str,
        ):
        self.team_id = team_id
        self.channel_id = channel_id
            
    @property
    def reference(self):
        return f"{self.team_id}/{self.channel_id}"
        
    @classmethod
    def from_reference(cls, reference):
        components = reference.split("/")
        if len(components) == 2:
            return cls(*components)
                
RID.register_context(SlackChannel)
