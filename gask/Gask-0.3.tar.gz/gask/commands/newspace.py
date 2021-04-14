import gask.start.start_prog
import gask.taskutils.taskspace


def new_space():
    """Creating a new taskspace"""

    # Asking the user if they want to create a new taskspace
    inp = input("Would you like to make this the current taskspace (y/n)\n")
    inp = inp.lower().strip()

    if inp == "y":
        # Deselecting the current taskspace
        taskutils.taskspace.deset_current_taskspace()
        start.start_prog.create_taskspace(True)
    else:
        start.start_prog.create_taskspace(False)