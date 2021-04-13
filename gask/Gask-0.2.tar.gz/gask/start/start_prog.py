import sys
from gask.start.create_repo import create_repo
from gask.commands.commandsearch import search
from gask.fileutils.directory import *
from gask.taskutils.import_taskspace import import_taskspace


def first_check():
    """Checks to see if a task space exists."""

    if len(sys.argv) > 1 and sys.argv[1].lower().strip() == "import":
        import_taskspace()
    # If repos.json is not found
    elif "repos.json" not in os.listdir(get_top_directory()) or open(get_repos_path()).read().strip() == "":

        print("No repo found")
        print("Would you like to to create a new Taskspace? (y/n)")
        choice = input().lower().strip()

        if choice == "y":
            print()
            create_taskspace(True)

    # If repos.json is found
    else:
        search(sys.argv[1:])


def create_taskspace(set_current: bool):
    """Beginning the process of creating a task space if there is no one listed."""

    print("Please enter a name")
    name = input()
    create_repo(name, get_user_folder(), set_current)



