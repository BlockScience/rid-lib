from rid_lib.core import ORN


class GithubRepo(ORN):
    namespace = "github.repo"

    def __init__(self, owner: str, repo_name: str):
        self.owner = owner
        self.repo_name = repo_name

    @property
    def reference(self):
        return f"{self.owner}/{self.repo_name}"

    @classmethod
    def from_reference(cls, reference):
        components = reference.split("/", 1)
        if len(components) == 2 and components[0] and components[1]:
            return cls(*components)
        raise ValueError(
            "GithubRepo reference must contain two '/'-separated components: '<owner>/<repo_name>'"
        )


GitHubRepo = GithubRepo
