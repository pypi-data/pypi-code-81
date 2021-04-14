import os
import git

from gask.taskutils.taskspace import get_current_taskspace


def create_central_repo():
    """Initialising a variable of central repo to operate on"""
    os.chdir(get_current_taskspace().filepath)
    repo = git.Repo(".")

    central_repo = repo.remotes["origin"]
    return central_repo


def update_to():
    """Push changes to central repo"""
    central_repo = create_central_repo()
    central_repo.push()


def update_from():
    """Receive changes from central repo"""
    central_repo = create_central_repo()
    central_repo.pull()
