import shutil

from gask.commands.switch import switch
from gask.taskutils.taskspace import read_task_spaces
from gask.taskutils.taskspace import write_to_repos_from_list


def delete_taskspace():
    """Deletes a taskspace"""

    # Displaying the current taskspaces
    count: int = 1
    taskspaces = read_task_spaces()
    print()
    for i in taskspaces:
        print(str(count) + ": " + str(i))
        count += 1

    # The user chooses which taskspace to delete
    print('\n Please enter a taskspace to delete')
    choice = int(input())

    # Checking if the choice exists
    if choice < 1 or choice > count:
        print("Incorrect folder")
        exit(1)

    # Storing the deleted taskspace for later options
    is_current = taskspaces[choice - 1].is_current

    # Allowing the user to delete the folder
    print("Would you like to delete the folder?(y/n)")
    empty = input().lower().strip()
    if empty == 'y':
        shutil.rmtree(taskspaces[choice - 1].filepath)

    # Deleting the taskspaces
    del taskspaces[choice - 1]

    # Rewriting the changes to the repos.json file
    write_to_repos_from_list(taskspaces)

    # Allowing the user to choose a new taskspace
    # if the current taskspace was deleted and
    # there is a taskspace left
    if is_current and count > 1:
        print("\nCurrent taskspace deleted.")
        print("Would you like to select another taskspace?")
        empty = input().lower().strip()
        if empty == "y":
            print()
            switch()
