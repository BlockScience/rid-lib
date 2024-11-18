from rid_lib.core import RID

class SlackTeam(RID):
    space = "slack"
    form = "team"
    
    def __init__(
            self,
            team_id: str,
        ):
        self.team_id = team_id
            
    @property
    def reference(self):
        return self.team_id
        
    @classmethod
    def from_reference(cls, reference):
        return cls(reference)
                
RID.register_context(SlackTeam)
