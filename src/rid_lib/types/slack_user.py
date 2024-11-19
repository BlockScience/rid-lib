from rid_lib.core import RID, ORN

class SlackUser(ORN):
    namespace = "slack.user"

    def __init__(
            self,
            team_id: str,
            user_id: str,
        ):
        self.team_id = team_id
        self.user_id = user_id
            
    @property
    def reference(self):
        return f"{self.team_id}/{self.user_id}"
        
    @classmethod
    def from_reference(cls, reference):
        components = reference.split("/")
        if len(components) == 2:
            return cls(*components)
                
RID.register_context(SlackUser)
