import pathlib


class Subrepo:
    def __init__(self, repo_path, revision="master", local_path="."):
        self.repo_path = repo_path
        self.revision = revision
        self.local_path = local_path
        #
        self.repo_name = pathlib.Path(repo_path).stem
