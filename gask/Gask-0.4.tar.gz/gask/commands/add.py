import datetime
import os
import sqlite3

from gask.gittools.git_commit import git_commit
from gask.taskutils.taskspace import get_current_taskspace


def add(task: str):
    """Adds a task to the database."""

    # Moving to the taskspace
    os.chdir(get_current_taskspace().filepath)

    # Connecting to the database
    connection = sqlite3.connect(get_current_taskspace().name + ".db")
    cursor = connection.cursor()

    # Executing the command
    current_date = datetime.date.today()
    cursor.execute('INSERT INTO tasks VALUES (?,?,?,?)', (None, task, None, current_date))
    connection.commit()

    # Closing connection to the database
    connection.close()

    # Updating git repo
    git_commit("Adding task")
