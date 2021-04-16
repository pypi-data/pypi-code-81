"""
Wrapper class for managing complex github commands needed to be
executed for this action
"""
from pencil_pusher.process_util import ProcessUtil
from github import Github
from github.ContentFile import ContentFile
from github.Repository import Repository


class GithubAPI:
    def __init__(self, personal_access_token: str = ""):
        """
        Creates a new GithubAPI wrapper object for computing
        complex github operations

        Args:
            personal_access_token (str): the github token to use
                for authentication.
        """
        self._has_token = personal_access_token != ""
        self._pat = personal_access_token
        if self._has_token:
            self._Github = Github(personal_access_token)
        else:
            self._Github = Github()

    def clone_repo(self, owner: str, repo: str, local_path: str = ""):
        """
        Clones a given github repo to a given local file path

        Args:
            owner (str): the owner of the repo
            repo (str): the name of the repo
            local_path (str): the local path to store this repo
        """
        url = f"https://github.com/{owner}/{repo}.git"
        if self._has_token:
            url = f"https://{owner}:{self._pat}@github.com/{owner}/{repo}.git"

        ProcessUtil.execute(["git", "clone", f"{url}", f"{local_path}"])

    def full_update(self, owner: str, repo: str, path: str):
        """
        stages, commits and pushes all changes to a git repo
        in the given directory.

        NOTE: will not create a commit if no files were changed

        Args:
            owner (str): the owner of the repo
            repo (str): the name of the repo
            path (str): the location of the repo
        """
        ProcessUtil.execute(
            [
                "git",
                "remote",
                "set-url",
                "origin",
                f"https://{owner}:{self._pat}@github.com/{owner}/{repo}.git",
            ],
            cwd=path,
        )

        ProcessUtil.execute(
            ["git", "config", "user.name", "pencil-pusher"], cwd=path
        )

        ProcessUtil.execute(["git", "config", "user.email", "<>"], cwd=path)

        ProcessUtil.execute(["git", "add", "."], cwd=path)

        returncode: int = ProcessUtil.execute(
            ["git", "commit", "-m", '"Auto commit by pencil-pusher"'], cwd=path
        )
        if returncode == 1:
            print("all docs are up to date")
            return

        ProcessUtil.execute(["git", "push"], cwd=path)

    @staticmethod
    def get_public_file(
        owner: str, repo: str, file_path: str, personal_access_token: str = ""
    ) -> str:
        """
        Gets a file from a public repo

        Args:
            owner (str): the owner the repo being queried
            repo (str): the name of the repo being queried
            file_path (str): the relative path of the file
                in the repo being queried
            personal_access_token (str): the github token used
                for authentication, required for private repos
        """
        g = (
            Github()
            if personal_access_token == ""
            else Github(personal_access_token)
        )
        repo: Repository = g.get_repo(f"{owner}/{repo}")
        response: ContentFile = repo.get_contents(file_path)
        return str(response.decoded_content, "utf-8")

    def _require_token(self):
        """
        Simple function that raises a Value error if a
        token is not defined but is required for the operation
        """
        if not self._has_token:
            raise ValueError(
                "The selected operation requires that a token be provided"
            )
