import os
import sqlite3

from gask.taskutils.taskspace import get_current_taskspace


def change_task_value(value: list):
    """Changing information about a task"""
    entry = int(value[0])
    if value[1] == "deadline":
        while "." in value[2]:
            value[2] = value[2].replace('.', '-')
        while "/" in value[2]:
            value[2] = value[2].replace('/', '-')

        # Connecting to the database
        database_path = os.path.join(get_current_taskspace().filepath, get_current_taskspace().name + ".db")
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        # Executing the command
        cursor.execute('UPDATE tasks SET deadline=? where id=?', (value[2], str(entry)))
        connection.commit()

        # Closing connection to the database
        connection.close()

    elif value[1] == "description" or value[1] == "name":
        # Connecting to the database
        database_path = os.path.join(get_current_taskspace().filepath, get_current_taskspace().name + ".db")
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        # Setting the new name/description
        new_description = " ".join(value[2:])
        if new_description[0] == '"':
            new_description = new_description[1:]
        if new_description[-1] == '"':
            new_description = new_description[0:len(new_description) - 2]

        # Updating the database
        cursor.execute('UPDATE tasks SET name=? where id=?', (new_description, str(entry)))
        connection.commit()
        connection.close()

    # If the field to change (e.g deadline) does not exist
    else:
        print("Unrecognised item to change")
