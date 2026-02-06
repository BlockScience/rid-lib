from rid_lib.core import ORN


class DiscordChannel(ORN):
    namespace = "discord.channel"
    
    def __init__(self, channel_id: str):
        self.channel_id = channel_id
            
    @property
    def reference(self):
        return self.channel_id
        
    @classmethod
    def from_reference(cls, reference):
        return cls(reference)
