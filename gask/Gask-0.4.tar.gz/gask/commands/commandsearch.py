from gask.commands.burndown import burndown
from gask.commands.complete import complete
from gask.commands.add import add
from gask.commands.list import list_tasks
from gask.commands.pull import pull
from gask.commands.push import push
from gask.commands.set import change_task_value
from gask.commands.setremote import set_remote
from gask.commands.newspace import new_space
from gask.commands.switch import switch
from gask.commands.delete_taskspace import delete_taskspace

"""
This file points the program to the correct function based on the argument given in the command line
May be switched at some point to a dictionary with functions or switch cases when they are introduced
to improve performance. 

This has become quite a large file due to the large number of commands implemented so I may look for a neater solution 
to sort this out. 

Also looking to switch to argparse or optparse in the future.

Many of the names of commands are taken from taskwarrior and git. As these are both open source, 
it made sense to do this to make the software familiar to those who have used those two in the past.  
"""


def search(args: list):
    """Runs an argument given through the commandline."""

    # Checking whether an argument is given
    if len(args) == 0:
        print("No arguments given")

    # Standard Commands

    # Adding a task
    elif args[0] == "add":
        add(" ".join(args[1:]))

    # Completing/Removing a task
    elif args[0] == "complete":
        complete(args[1])

    # listing the tasks
    elif args[0] == "list":
        list_tasks()

    # Taskspace Management

    # Creates a new Taskspace
    elif args[0] == "create":
        new_space()

    # Deletes a taskspace
    elif args[0] == "delete":
        delete_taskspace()

    # Changes the current taskspace
    elif args[0] == "switch":
        switch()

    # Sets a detail about a task in the current task space
    elif args[0] == "set":
        change_task_value(args[1:])

    # Central repository

    # Sets a central repository as a remote for a current taskspace
    elif args[0] == "setremote":
        set_remote(args[1])

    # Committing changes to a central repository
    elif args[0] == "push":
        push()

    # Retrieving changes from a central repository
    elif args[0] == "pull":
        pull()

    # Completing a complete update with a central repository
    elif args[0] == "update":
        pull()
        push()

    # Extra
        
    # Draws a burndown chart in matplotlib
    elif args[0] == "burndown":
        burndown()

    
    else:
        print("Unrecognised argument")
