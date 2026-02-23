from rid_lib.types.github_repo import GitHubRepo
from rid_lib.core import ORN


class GitHubPullRequest(ORN):
    namespace = "github.pr"

    def __init__(self, owner: str, repo_name: str, pr_number: int):
        self.owner = owner
        self.repo_name = repo_name
        self.pr_number = int(pr_number)

    @property
    def reference(self):
        return f"{self.owner}/{self.repo_name}:{self.pr_number}"

    @classmethod
    def from_reference(cls, reference):
        parts = reference.split(":", 1)
        if len(parts) != 2:
            raise ValueError(
                "GitHubPullRequest reference must be '<owner>/<repo_name>:<pr_number>'"
            )
        repo_parts = parts[0].split("/", 1)
        if len(repo_parts) != 2 or not repo_parts[0] or not repo_parts[1]:
            raise ValueError(
                "GitHubPullRequest reference must be '<owner>/<repo_name>:<pr_number>'"
            )
        try:
            pr_number = int(parts[1])
        except ValueError:
            raise ValueError(f"Invalid PR number in GitHubPullRequest reference: {parts[1]}")
        return cls(owner=repo_parts[0], repo_name=repo_parts[1], pr_number=pr_number)

    def get_repo_rid(self) -> GitHubRepo:
        return GitHubRepo(owner=self.owner, repo_name=self.repo_name)


GithubPullRequest = GitHubPullRequest
