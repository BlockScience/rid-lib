from rid_lib.core import ORN


class DiscordUser(ORN):
    namespace = "discord.user"
    
    def __init__(self, user_id: str):
        self.user_id = user_id
            
    @property
    def reference(self):
        return self.user_id
        
    @classmethod
    def from_reference(cls, reference):
        return cls(reference)
