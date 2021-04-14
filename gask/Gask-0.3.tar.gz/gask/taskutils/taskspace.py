import json
from gask.fileutils.directory import get_top_directory
from gask.fileutils.directory import get_repos_path


class Taskspace:
    """A class to store information about taskspaces."""
    name: str
    filepath: str
    is_current: bool

    def create_dict(self):
        """Turning a taskspace into a dictionary."""
        ret_dict = dict()

        ret_dict["name"] = self.name
        ret_dict["path"] = self.filepath
        ret_dict["current"] = self.is_current

        return ret_dict

    def __str__(self):
        """Returns a presentable form of a taskspace"""
        return self.name + '|' + self.filepath + '|' + str(self.is_current)

    def __init__(self, name: str, path: str, is_current: bool):
        """Construct a taskspace object"""
        self.name = name
        self.filepath = path
        self.is_current = is_current


def create_taskspace_from_dict(task_dict: dict):
    """Converts a taskspace dictionary into a taskspace object"""
    taskspace: Taskspace = Taskspace(task_dict["name"], task_dict["path"], task_dict["current"])
    return taskspace


def read_task_spaces():
    """Reading taskspaces from the json file and returns a list of taskspace objects"""
    taskspaces = list()
    for i in json.loads(open(get_repos_path()).read())["Taskspaces"]:
        taskspaces.append(create_taskspace_from_dict(i))
    return taskspaces


def get_current_taskspace():
    """Getting the current taskspace."""
    for i in read_task_spaces():
        if i.is_current:
            return i


def get_list_of_taskspace_dicts(task_objects: list):
    """Returning a list of taskspaces in dictionaries from the repos.json file"""
    dict_list = list()

    for i in task_objects:
        dict_list.append(i.create_dict())

    return dict_list


def deset_current_taskspace():
    """Making any current taskspaces not current"""
    taskspaces = read_task_spaces()
    for i in range(len(taskspaces)):
        taskspaces[i].is_current = False
    write_to_repos_from_list(taskspaces)


def write_to_repos_from_list(taskspaces: list):
    """Taking a list of taskspace objects and writing them to the repos file"""
    taskspaces = get_list_of_taskspace_dicts(taskspaces)
    write_dict = dict()
    write_dict["Taskspaces"] = taskspaces

    file = open(get_repos_path(), "w")
    file.write(json.dumps(write_dict, indent=2))
    file.close()
