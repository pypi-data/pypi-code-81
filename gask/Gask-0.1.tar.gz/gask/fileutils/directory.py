import os
from gask.fileutils.folderopen import choose_folder


def get_top_directory():
    """
    Returns the directory that the project is stored in.
    
    Returns a string of a file path.
    """
    return os.path.dirname(os.path.dirname(__file__))


def get_repos_path():
    """Returns the path to the repos.json file."""
    import gask
    return os.path.join(os.path.dirname(os.path.realpath(gask.__file__)), "repos.json")


def get_user_folder():
    """Getting the user to choose a folder."""
    choice = input("Would you like to use the current folder? (y/n)\n").strip().lower()

    if choice == 'y':
        return os.getcwd()
    else:
        current_dir = os.getcwd()
        chosen_filepath = choose_folder()
        os.chdir(current_dir)
        return chosen_filepath

