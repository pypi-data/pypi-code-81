import sqlite3
import os
import terminaltables
from gask.taskutils.taskspace import get_current_taskspace


def list_tasks():
    """Listing the current tasks in the database."""

    # Moving to the current taskspace
    os.chdir(get_current_taskspace().filepath)

    # connecting to database
    connection = sqlite3.connect(get_current_taskspace().name + ".db")
    cursor = connection.cursor()

    # running query
    cursor.execute("SELECT * FROM tasks")

    # Printing all of the tasks
    tasks = [["Id", "Description", "Deadline", "Date Set"]] + cursor.fetchall()
    print(terminaltables.AsciiTable(tasks).table)

    # closing connection to database
    connection.close()
