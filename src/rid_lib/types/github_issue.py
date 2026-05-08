from rid_lib.types.github_repo import GitHubRepo
from rid_lib.core import ORN


class GitHubIssue(ORN):
    namespace = "github.issue"

    def __init__(self, owner: str, repo_name: str, issue_number: int):
        self.owner = owner
        self.repo_name = repo_name
        self.issue_number = int(issue_number)

    @property
    def reference(self):
        return f"{self.owner}/{self.repo_name}:{self.issue_number}"

    @classmethod
    def from_reference(cls, reference):
        parts = reference.split(":", 1)
        if len(parts) != 2:
            raise ValueError(
                "GitHubIssue reference must be '<owner>/<repo_name>:<issue_number>'"
            )
        repo_parts = parts[0].split("/", 1)
        if len(repo_parts) != 2 or not repo_parts[0] or not repo_parts[1]:
            raise ValueError(
                "GitHubIssue reference must be '<owner>/<repo_name>:<issue_number>'"
            )
        try:
            issue_number = int(parts[1])
        except ValueError:
            raise ValueError(f"Invalid issue number in GitHubIssue reference: {parts[1]}")
        return cls(owner=repo_parts[0], repo_name=repo_parts[1], issue_number=issue_number)

    def get_repo_rid(self) -> GitHubRepo:
        return GitHubRepo(owner=self.owner, repo_name=self.repo_name)


GithubIssue = GitHubIssue
