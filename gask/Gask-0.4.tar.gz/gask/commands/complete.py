import sqlite3
import os
import datetime
from gask.gittools.git_commit import git_commit
from gask.taskutils.taskspace import get_current_taskspace


def complete(num: int):
    """
    Marking a task complete and deleting it from the database.
    
    Takes an input of a id number. Deletes the corresponding task.
    """

    # Moving to the correct storage folder
    os.chdir(get_current_taskspace().filepath)

    # Connecting to the database
    connection = sqlite3.connect(get_current_taskspace().name + ".db")
    cursor = connection.cursor()

    # Storing completed task info
    cursor.execute("SELECT * FROM tasks WHERE ID = ?", (num))
    values = cursor.fetchall()[0]
    current_date = datetime.date.today()
    cursor.execute("INSERT INTO completed_tasks VALUES (?, ?, ?, ?)", (None, values[1], values[3], current_date))

    # Executing command
    cursor.execute("DELETE FROM tasks WHERE ID = ?", (num))
    connection.commit()

    # Closing connection to the database
    connection.close()

    # Updating git repository
    git_commit("Completing task")
