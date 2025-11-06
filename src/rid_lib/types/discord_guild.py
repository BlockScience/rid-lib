from rid_lib.core import ORN


class DiscordGuild(ORN):
    namespace = "discord.guild"
    
    def __init__(self, guild_id: str):
        self.guild_id = guild_id
            
    @property
    def reference(self):
        return self.guild_id
        
    @classmethod
    def from_reference(cls, reference):
        return cls(reference)
