import datetime
import os
import sqlite3
from gask.taskutils.taskspace import get_current_taskspace


def burndown():
    """Drawing a burndown chart based on the current taskspace in matplotlib"""

    # This library needs matplotlib to run
    try:
        import matplotlib.pyplot as plot
    except ModuleNotFoundError:
        print("Matplotlib needed for this feature")
        exit(1)

    # Connecting to database
    database_path = os.path.join(get_current_taskspace().filepath, get_current_taskspace().name + ".db")
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    # Performing query
    cursor.execute("SELECT * FROM tasks")
    current_tasks = cursor.fetchall()
    cursor.execute("SELECT * FROM completed_tasks")
    completed_tasks = cursor.fetchall()

    # Initializing the storing of data
    tasks_undone = list()
    tasks_done = list()
    labels = list()

    # Appending the data to the lists
    for i in get_months():
        labels.append(short_display_of_date(i))
        data = get_data_for_day(i, current_tasks, completed_tasks)
        tasks_done.append(data[0])
        tasks_undone.append(data[1])

    # Drawing the graph
    plot.figure(figsize=(8, 6))
    plot.xticks(range(len(labels)), labels)
    plot.bar(range(len(tasks_done)), tasks_done)
    plot.bar(range(len(tasks_undone)), tasks_undone, bottom=tasks_done)
    plot.legend(("Completed", "Pending"))

    # Making the graph visible
    plot.show()


def short_display_of_date(date: datetime):
    """Reformatting the date in a format suitable for the graph"""
    return str(date.day) + "/" + str(date.month)


def get_data_for_day(date: datetime.date, current_tasks: list, completed_tasks: list):
    """Measures the number of tasks that were done or not done on a certain date"""
    number_of_tasks_undone: int = 0
    number_of_tasks_done: int = 0

    # If the date is before or the same as the given date
    # Then add to the undone section
    for i in current_tasks:
        if date >= get_date_from_string(i[3]):
            number_of_tasks_undone += 1

    for i in completed_tasks:
        # Check if the date is before the date the task was created
        if date >= get_date_from_string(i[2]):
            # If the date is after the completed date, then the task was not complete on that day
            if date < get_date_from_string(i[3]):
                number_of_tasks_undone += 1
            else:
                number_of_tasks_done += 1
    return number_of_tasks_undone, number_of_tasks_done


def get_date_from_string(string: str):
    """Converts a string in a yyyy-mm-dd format to a date time object"""
    string = string.split("-")
    return datetime.date(year=int(string[0]), month=int(string[1]), day=int(string[2]))


def get_months():
    """Returns dates 15 days before the current date and the current date"""
    # Creating list of dates
    dates = list()

    # Going back 15 days
    first_day = datetime.date.today() - datetime.timedelta(days=15)

    # Adding the dates to the list
    for i in range(16):
        dates.append(first_day)
        first_day += datetime.timedelta(days=1)

    return dates
