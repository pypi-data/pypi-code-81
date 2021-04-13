import git
import os
import json
import datetime
from gask.taskutils.taskspace import get_current_taskspace


def git_commit(commit_message: str):
    """ Committing the folder the taskspace is in """

    # Updating the info file
    info = json.loads(open("info.json").read())
    info["Last Commit"] = str(datetime.date.today())
    open("info.json", "w").write(json.dumps(info, indent=2))

    # Committing the changes to the git repo
    os.chdir(get_current_taskspace().filepath)
    repo = git.Repo(".")
    repo.index.add("*")
    repo.index.commit(commit_message)
