from rid_lib.core import ORN


class GitHubEvent(ORN):
    namespace = "github.event"

    def __init__(self, repo_full_name: str, event_id: str):
        repo_parts = repo_full_name.split("/", 1)
        if len(repo_parts) != 2 or not repo_parts[0] or not repo_parts[1]:
            raise ValueError(
                f"Invalid repo_full_name format: {repo_full_name}. Expected 'owner/repo'."
            )
        if not str(event_id):
            raise ValueError("Event ID cannot be empty for GitHubEvent.")
        self.repo_full_name = repo_full_name
        self.event_id = str(event_id)

    @property
    def reference(self):
        return f"{self.repo_full_name}:{self.event_id}"

    @classmethod
    def from_reference(cls, reference):
        parts = reference.split(":", 1)
        if len(parts) != 2:
            raise ValueError(
                f"Invalid GitHubEvent reference format: '{reference}'. Expected 'owner/repo:event_id'."
            )
        if not parts[1]:
            raise ValueError(
                f"Event ID part cannot be empty in GitHubEvent reference: '{reference}'."
            )
        return cls(repo_full_name=parts[0], event_id=parts[1])


GithubEvent = GitHubEvent
