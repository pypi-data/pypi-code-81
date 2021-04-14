import os
import git

from gask.taskutils.taskspace import get_current_taskspace


def set_remote(url: str):
    """Setting the remote for the current taskspace"""

    # Initializing repo object
    repo = git.Repo(get_current_taskspace().filepath)

    # Setting the origin
    origin = repo.create_remote("origin", url=url)
    repo.git.push("--set-upstream", origin, repo.head.ref)