from rid_lib.core import ORN


class DiscordMessage(ORN):
    namespace = "discord.message"
    
    def __init__(self, channel_id: str, message_id: str):
        self.channel_id = channel_id
        self.message_id = message_id
            
    @property
    def reference(self):
        return f"{self.channel_id}/{self.message_id}"
        
    @classmethod
    def from_reference(cls, reference):
        components = reference.split("/")
        if len(components) == 2:
            return cls(*components)
