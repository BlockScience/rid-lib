from rid_lib.types.github_repo import GitHubRepo
from rid_lib.core import ORN


class GitHubCommit(ORN):
    namespace = "github.commit"

    def __init__(self, owner: str, repo_name: str, commit_sha: str):
        self.owner = owner
        self.repo_name = repo_name
        self.commit_sha = commit_sha

    @property
    def reference(self):
        return f"{self.owner}/{self.repo_name}:{self.commit_sha}"

    @classmethod
    def from_reference(cls, reference):
        parts = reference.split(":", 1)
        if len(parts) != 2:
            raise ValueError(
                "GitHubCommit reference must be '<owner>/<repo_name>:<commit_sha>'"
            )
        repo_parts = parts[0].split("/", 1)
        if len(repo_parts) != 2 or not repo_parts[0] or not repo_parts[1] or not parts[1]:
            raise ValueError(
                "GitHubCommit reference must be '<owner>/<repo_name>:<commit_sha>'"
            )
        return cls(owner=repo_parts[0], repo_name=repo_parts[1], commit_sha=parts[1])

    def get_repo_rid(self) -> GitHubRepo:
        return GitHubRepo(owner=self.owner, repo_name=self.repo_name)


GithubCommit = GitHubCommit
