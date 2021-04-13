import git
import sqlite3
import os
import json
import gask.taskutils.taskspace
import datetime
from gask.fileutils.directory import get_repos_path
from gask.taskutils.taskspace import read_task_spaces, get_list_of_taskspace_dicts


def create_repo(name: str, path: str, is_current: bool):
    """Creating a new taskspace in a given path."""

    current_path = os.getcwd()

    # Setting the queries to create the databases
    create_tasks_database = get_create_tasks_query()
    create_completed_database = get_completed_tasks_query()

    # Crating a empty git repo 
    repo = git.Repo.init(path)

    # Moving to the correct folder 
    os.chdir(path)

    # Creating the database 
    connection = sqlite3.connect(name + ".db")
    cursor = connection.cursor()
    cursor.execute(create_tasks_database)
    cursor.execute(create_completed_database)
    connection.close()

    # Making a initial commit
    repo.index.add("*")
    repo.index.commit("Creating new taskspace")

    # Creating info file
    info = dict()
    info["Name"] = name
    info["Last Commit"] = str(datetime.date.today())
    writer = open("info.json", "w")
    writer.write(json.dumps(info))
    writer.close()

    os.chdir(current_path)
    taskspace = gask.taskutils.taskspace.Taskspace(name, path, is_current)
    task_dict = taskspace.create_dict()
    file_exists = os.path.isfile(get_repos_path())

    # Adding to the Repos.json file
    if file_exists:
        taskspaces = get_list_of_taskspace_dicts(read_task_spaces())
        taskspaces.append(taskspace.create_dict())

    # Creating the Repos.json file
    else:
        taskspaces = list()
        taskspaces.append(task_dict)

    file = open(get_repos_path(), "w")
    write_dict = dict()
    write_dict["Taskspaces"] = taskspaces

    file.write(json.dumps(write_dict, indent=2))
    file.close()


def get_create_tasks_query():
    """Returns the query to create the tasks table"""
    return """
    CREATE TABLE tasks(
        id INTEGER PRIMARY KEY,
        name TEXT,
        deadline TEXT,
        date_set TEXT
    );
    """


def get_completed_tasks_query():
    """Returns the query to create the completed tasks table"""
    return """
    CREATE TABLE completed_tasks(
        id INTEGER PRIMARY KEY,
        name TEXT,
        date_set TEXT,
        completed TEXT
    );
    """
