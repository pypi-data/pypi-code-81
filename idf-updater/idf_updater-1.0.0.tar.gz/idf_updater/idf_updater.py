"""
This module is used to update singular IDF's, lists of IDF's, or directories of IDF's to newer versions. Built
for Linux and MacOS as windows has the IDFVersionUpdater.exe functionality from
EnergyPlus.

Will find local energyplus conversion files. Currently supports version updating
from 8.0 --> newest EnergyPlus Version

'update_idf' can be passed a folder containing idfs, a path to a singular idf, or
a list of paths to idf files.
"""
import os
import sys
import glob
from shutil import copyfile, rmtree
import subprocess
from besos.eplus_funcs import get_ep_path, get_idf_version_pth
from besos.besos_utils import get_file_name
from besos.errors import InstallationError
import glob


# TODO: Maybe add ep_path functionality where user can pass in the installation path for their EnergyPlus

# NOTE: consider changing name directory
# NOTE: Could maybe move away from recursion
def update_idf(
    directory, goal_version=None, keep_orig=True, keep_int=False, recursive=False
):
    """Updates the given IDF to the goal version.

    :param directory: Either a string of a path to a idf file, string of a directory containing idf files, or a list of paths to idf files
    :param goal_version: Float of the version you want the idf updated to. Supports up to newest version of EnergyPlus installed on system
    :param keep_orig: Boolean of if the original idf should be retained
    :param keep_int: Boolean of if the intermediate files should be retained
    :param recursive: Boolean for directory searching for idf files, if the search should be recursive
    :return: None
    """
    if goal_version is None:
        ep_version, ep_versions, ep_path = get_ep_version()
        if len(ep_version) == 5:  # for example v9-0-1
            ep_version = ep_version[:3]  # 9-0-1 --> 9-0
        goal_version = float(ep_version.replace("-", "."))  # 9.0

    if isinstance(directory, list):
        for dir in directory:
            update_idf(
                dir, goal_version=goal_version, keep_orig=keep_orig, keep_int=keep_int
            )

    elif os.path.isdir(directory):
        if recursive:
            directory = os.path.join(directory, "**", "*.idf")
            directoryList = glob.glob(directory, recursive=True)
        else:
            directory = os.path.join(directory, "*.idf")
            directoryList = glob.glob(directory)
        for dir in directoryList:
            update_idf(
                dir, goal_version=goal_version, keep_orig=keep_orig, keep_int=False
            )

    elif os.path.isfile(directory):
        if isinstance(goal_version, str):
            if len(goal_version) == 5:
                goal_version = goal_version[:-2]
            goal_version = float(goal_version.replace("-", "."))

        current_version = get_idf_version_pth(directory)
        if len(current_version) == 5:
            current_version = current_version[:-2]
        current_version = float(current_version.replace("-", "."))

        if current_version > goal_version:
            s = f"IDF Provided was newer version then the goal.\nCurrent: {str(current_version)}\nGoal: {str(goal_version)}"
            raise ValueError(s)
        directory = os.path.abspath(directory)
        shList = create_scripts(cur_version=current_version)
        if keep_orig:
            keep_orig_path = directory.replace(".idf", f"-v{current_version}.idf")
            if not os.path.exists(keep_orig_path):
                copyfile(directory, keep_orig_path)
            else:
                copy_file(directory, current_version)
        update_idf_helper(
            directory, float(current_version), float(goal_version), keep_int, shList
        )


def update_idf_helper(path, current_version, goal_version, keep_int, shList):
    """'update_idf()' helper function that completes the conversions

    :param path: String of a path to the idf file
    :param goal_version: Float of the version you want the idf updated to. Supports up to newest version of EnergyPlus installed on system
    :param keep_int: Boolean of if the intermediate files should be retained
    :param shList: Dictionary of directories to shell scripts for conversions
    :return: None
    """
    if goal_version == current_version:
        print("Current Version: " + str(current_version) + ", Conversion Complete")
        old_file = os.path.abspath(path + "old")
        new_file = os.path.abspath(path + "new")
        err_file = os.path.abspath(path[:-3] + "VCpErr")
        file_name = get_file_name(path)
        folder_name = file_name.replace(file_name, "")
        exec_folder = os.path.abspath(os.path.join(folder_name, ".execFiles"))
        if keep_int and os.path.exists(err_file):
            copy_file(err_file, current_version)
        if os.path.exists(err_file):
            os.remove(err_file)
        if os.path.exists(new_file):
            os.remove(new_file)
        if os.path.exists(old_file):
            os.remove(old_file)
        if os.path.exists(exec_folder):
            rmtree(exec_folder)

    else:
        print("Current Version: " + str(current_version))
        execdir = os.path.abspath(shList[current_version])
        err_file = os.path.abspath(path[:-3] + "VCpErr")
        if keep_int:
            copy_file(path, current_version)
            if os.path.exists(err_file):
                copy_file(err_file, current_version)
        command = execdir + " " + path
        os.system(command)
        update_idf_helper(
            path, round(current_version + 0.1, 1), goal_version, keep_int, shList
        )


def copy_file(path, version):
    """Copies the passed file into the updatefiles folder.

    :param path: A directory to the idf file
    :param version: Version of the idf file
    :return: None
    """

    file_name = get_file_name(path)
    directory = path.replace(file_name, "")
    if file_name.endswith("VCpErr"):
        file_name = file_name[:-7] + "-V" + str(version) + "-ErrorFile.txt"
    else:
        file_name = file_name[:-4] + "-V" + str(version) + ".idf"
    directory = os.path.join(directory, "updatefiles")
    if not os.path.exists(directory):
        os.mkdir(directory)
    directory = os.path.join(directory, file_name)
    copyfile(path, directory)


def get_ep_version():
    """
    Gets latest version of E+ installed on system

    :returns: (ep_version, ep_versions, ep_path), ep_version is a string of version,
    ep_versions contains all older versions to create conversion files
    ep_path provides a path to the newest version of energyplus
    """
    ep_versions = [
        "9-4-0",
        "9-3-0",
        "9-2-0",
        "9-1-0",
        "9-0-1",
        "8-9-0",
        "8-8-0",
        "8-7-0",
        "8-6-0",
        "8-5-0",
        "8-4-0",
        "8-3-0",
        "8-2-0",
        "8-1-0",
        "8-0-0",
    ]  # NOTE: When new EnergyPlus versions come out, add to front of list

    ep_path = ep_version = None
    for version in ep_versions:  # Loop finds newest version of EnergyPlus installed
        try:
            ep_path = os.path.join(
                get_ep_path(version)[1], "PreProcess", "IDFVersionUpdater"
            )
            ep_version = version
            break
        except InstallationError:
            pass

    if ep_path is None or not os.path.exists(ep_path):
        raise InstallationError("Cannot find EnergyPlus directory or transition files")

    ep_versions = ep_versions[
        ep_versions.index(ep_version) :
    ]  # Removes newer EnergyPlus versions from  ep_versions from ep_version

    try:
        ep_versions[
            ep_versions.index("9-0-1")
        ] = "9-0-0"  # Changes 9-0-1 to 9-0-0 to work with transition files
    except KeyError:
        pass

    return ep_version, ep_versions, ep_path


def create_scripts(cur_version=8.0):
    """Creates shell scripts to execute conversions

    :param cur_version: Current version of idf attempting to convert to avoid unnecessary script creations
    :return: Dictionary of shell scripts for each version
    """
    ep_version, ep_versions, ep_path = get_ep_version()
    ep_versions.sort()  # sorts to ascending order
    cur_version = str(round(cur_version, 1)).replace(".", "-") + "-0"
    ep_versions = ep_versions[
        ep_versions.index(cur_version) :
    ]  # Removes older EnergyPlus versions than cur_version from ep_versions

    script_dict = {}
    if not os.path.exists(".execFiles"):
        os.mkdir(".execFiles")

    for x in range(len(ep_versions) - 1):
        transition_file = f"Transition-V{ep_versions[x]}-to-V{ep_versions[x+1]}"
        file_name = os.path.join(".execFiles", (transition_file + ".sh"))

        if os.path.exists(os.path.join(ep_path, transition_file)):
            with open(file_name, "w+") as f:
                command = f"cd {ep_path}\n./{transition_file} $1"
                f.write(command)
                f.close()
            script_dict[float(ep_versions[x][:-2].replace("-", "."))] = file_name
            subprocess.call(["chmod", "u+x", file_name])
        else:
            message = f"Transition file was not found\nExpected {os.path.join(ep_path, transition_file)}"
            raise InstallationError(message=message)

    return script_dict
