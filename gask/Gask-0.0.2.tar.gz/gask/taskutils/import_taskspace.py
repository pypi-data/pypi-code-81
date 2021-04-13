import json
import os
from gask.fileutils.directory import get_user_folder
from gask.fileutils.directory import get_repos_path


def import_taskspace():
    """Importing a taskspace from a file location"""
    # Getting the location
    folder_path = get_user_folder()
    # Setting up the new taskspace
    name: str = json.loads(open(os.path.join(folder_path, "info.json")).read())["Name"]
    new_repo = dict()
    new_repo["name"] = name
    new_repo["path"] = folder_path

    # If the repos.json file exists
    if os.path.isfile(get_repos_path()):
        repos: dict = json.loads(open(get_repos_path()).read())
        option = input("\n Would you like to make this the current taskspace(y/n)").lower().strip()
        new_repo = option == 'y'
        # Making any other taskspace not current
        if new_repo:
            for i in repos["Taskspaces"]:
                if i["current"]:
                    i["current"] = False

    # If the repos.json file doesn't exist
    else:
        repos = dict()
        repos["Taskspaces"] = []
        new_repo["current"] = True

    repos["Taskspaces"].append(new_repo)

    # Adding taskspace to the repos file
    open(get_repos_path(), "w").write(json.dumps(repos, indent=2))
