from rid_lib.core import ORN
from .slack_workspace import SlackWorkspace


class SlackUserGroup(ORN):
    namespace = "slack.usergroup"
    
    def __init__(self, team_id: str, subteam_id: str):
        self.team_id = team_id
        self.subteam_id = subteam_id
        
    @property
    def reference(self):
        return f"{self.team_id}/{self.subteam_id}"
    
    @property
    def mention(self) -> str:
        return f"<!subteam^{self.subteam_id}>"
    
    @property
    def workspace(self):
        return SlackWorkspace(team_id=self.team_id)
    
    @classmethod
    def from_reference(cls, reference):
        components = reference.split("/")
        if len(components) == 2:
            return cls(*components)
        else:
            raise ValueError("Slack User Group reference must containt two '/'-separated componeonts: '<team_id>/<usergroup_id>'")
        