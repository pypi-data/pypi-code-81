import _curses
import os
from pick import pick
import sys


def create_menu_items(hide: bool):
    """
    Generating the list of items to be shown to the user during
    file selection.

    Tasks a boolean argument which determines whether hidden files are shown.
    i.e. whether there is a '.' character at the start of the name.
    """

    # Creating and initialising the list of options
    options = ["Use This Folder", "Make New Folder"]

    # Adding options based on whether files are hidden
    if hide:
        options = options + ["Show Hidden Folders"] + \
                  [".."] + \
                  sorted([i for i in os.listdir() if os.path.isdir(i) and i[0] != "."])
    else:
        options = options + ["Hide Hidden Folders"] + \
                  [".."] + \
                  sorted([i for i in os.listdir() if os.path.isdir(i)])

    # Adding an option to change drive if on windows
    if sys.platform == "win32":
        options.insert(3, "Change Drive")

    return options


def make_folder():
    """Asking the user to create a folder"""
    name = input("Please enter the name of the new Folder: ")
    os.mkdir(name)


def change_win_drive():
    """Changing the current drive in windows based on a user input"""
    os.chdir(input("Please enter the drive letter\n") + ":")


def choose_folder():
    """Opening a menu to allow the user to graphically select a folder."""

    # Whether hidden folders should be shown or not
    hide = False

    while True:
        # Creating Menu
        try:
            option, index = pick(create_menu_items(hide), os.getcwd(), indicator="-->")
        # If curses is not supported
        except _curses.error:
            folder_path = input("Please enter a filepath\n")
            if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
                print("Folder not found")
                sys.exit(1)
            else:
                return folder_path
        # Returning the path of the current folder
        if index == 0:
            return os.getcwd()
        # Creating a new folder
        elif index == 1:
            make_folder()
        # Changing the hide setting
        elif index == 2:
            hide = not hide
        # Changing the current drive on windows
        elif index == 3 and sys.platform == "win32":
            change_win_drive()
        # Moving to the selected folder
        else:
            os.chdir(option)

