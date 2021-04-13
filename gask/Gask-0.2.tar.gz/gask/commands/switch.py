import gask.taskutils.taskspace
from gask.taskutils.taskspace import write_to_repos_from_list


def switch():
    """Changing the current taskspace"""

    # Getting the taskspace
    taskspaces = gask.taskutils.taskspace.read_task_spaces()

    # Displaying the taskspaces
    for c, i in enumerate(taskspaces):
        print(str(c + 1) + ": " + i.name + ": " + i.filepath)

    # The user chooses a taskspace
    num = int(input("Select a taskspace\n").strip())

    # Setting the current taskspace and unsetting any other taskspaces
    for i in range(len(taskspaces)):
        if num - 1 == i:
            taskspaces[i].is_current = True
        else:
            taskspaces[i].is_current = False
        taskspaces[i] = taskspaces[i].create_dict()

    # Updating the repos.json file
    write_to_repos_from_list(taskspaces)
