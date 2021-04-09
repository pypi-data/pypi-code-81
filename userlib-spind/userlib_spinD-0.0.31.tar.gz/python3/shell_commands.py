# -*- coding: utf-8 -*-
r"""
Lib for python - shell communication

Moritz Goerzen
08.2018
Spintronic Theory Kiel
---------------------------------
OS-System Dependency added by Hendrik Schrautzer
"""
import subprocess
import os
import sys
import platform
from contextlib import contextmanager
import time
from tempfile import mkstemp
from shutil import move, copy2
from os import fdopen, remove
from datetime import datetime

import python3.constants as const
from typing import TypeVar
from pathlib import Path

PathLike = TypeVar("PathLike", str, Path)

# operating system
OPERATINGSYSTEM = platform.system()


@contextmanager
def change_directory(newdir: PathLike) -> None:
    r"""
    Changes the directory using context manager. Will automatically put everything before the yield statement into the
    __enter__-method and everythin behind in the __exit__method.

    Args:
        newdir(str): name of the directory. Has to be a subdirectory of the actual directory.
    """
    prevdir = Path.cwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)


def make_directory(directory: PathLike) -> None:
    r"""
    Creates directory. Chooses the command based on OS. It is possible to create multiple nested directories. It is
    highly recommended to use the input type of pathlibs Path then. Otherwise one has to set the correct back- or
    forward slashes. This destroys the benefit of this platform indepent implementation.

    Args:
        directory(PathLike): new directory
    """
    if OPERATINGSYSTEM == 'Windows':
        command = "md " + str(directory)
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, shell=True)
    elif OPERATINGSYSTEM == 'Linux':
        command = "mkdir " + str(directory)
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    else:
        raise Exception('operating system not yet coded.')
    output, error = process.communicate()


def copy_folder(target: PathLike, destination: PathLike) -> None:
    r"""
    Copies folder from target to destination. Chooses the command based on Os. For windows the /i flag supresses asking
    whether copying and the /e flag enables empty copying.
    """
    if OPERATINGSYSTEM == 'Windows':
        command = "xcopy " + str(target) + " " + str(destination) + "/i /e"
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, shell=True)
    elif OPERATINGSYSTEM == 'Linux':
        command = "cp -r " + str(target) + " " + str(destination)
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    else:
        raise Exception('operating system not yet coded.')
    output, error = process.communicate()


def copy_element(target: PathLike, destination: PathLike) -> None:
    r"""
    Copies an element (target) to a destination. Chooses the command based on OS. On windows the shell=True flag
    must be set. Should be replaced someday by shutil.which
    (https://stackoverflow.com/questions/3022013/windows-cant-find-the-file-on-subprocess-call)

    Args:
        target(PathLike): target file
        destination(PathLike): destination file
    """
    if OPERATINGSYSTEM == 'Windows':
        command = "copy " + str(target) + " " + str(destination)
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, shell=True)
    elif OPERATINGSYSTEM == 'Linux':
        command = "cp " + str(target) + " " + str(destination)
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    else:
        raise Exception('operating system not yet coded.')
    output, error = process.communicate()


def copy_all_elements(targetdirectory, extension, destination):
    # ==================================================================
    for filename in os.listdir(targetdirectory):
        if filename.endswith(extension):
            pathname = os.path.join(targetdirectory, filename)
            if os.path.isfile(pathname):
                copy2(pathname, destination)


def remove_element(filename: PathLike) -> None:
    r"""
    Removes element (filename). Chooses the command based on Os. The windows /q flag is for silent removing. If the file
    is given as a path it is highly recomm. to use pathlibs Path for platform indepent input.
    """
    if OPERATINGSYSTEM == 'Windows':
        command = "del " + str(filename) + " /q"
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, shell=True)
    elif OPERATINGSYSTEM == 'Linux':
        command = "rm " + str(filename)
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    else:
        raise Exception('operating system not yet coded.')
    output, error = process.communicate()


def remove_folder(directory: PathLike) -> None:
    r"""
    Removes directory with everything inside. Chooses the command based on Os. The windows /s flag is for
    deleting subfolders and files and the /q flag is for silent modus.
    """
    if OPERATINGSYSTEM == 'Windows':
        command = "rmdir " + str(directory) + " /s /q"
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, shell=True)
    elif OPERATINGSYSTEM == 'Linux':
        command = "rm -r " + str(directory)
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    else:
        raise Exception('operating system not yet coded.')
    output, error = process.communicate()


def call_bash(scriptname):
    # ==================================================================
    # calls an .sh-script on linux desktop
    bashCommand = "bash " + str(scriptname)
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()


def call_sbatch(scriptname):
    # ==================================================================
    # calls an .sh-script on linux clusters
    bashCommand = "sbatch " + str(scriptname)
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()


def call_python(scriptname):
    # ==================================================================
    # calls an external python script
    bashCommand = "python " + str(scriptname)
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()


def adjust_parameter(keyword, value, directory_file):
    # ==================================================================
    # looks up "directory_file" for the given "keyword" and substitutes everything behind it
    # with "value"
    fh, abs_path = mkstemp()
    with fdopen(fh, 'w') as new_file:
        with open(directory_file) as old_file:
            for line in old_file:
                words = line.split()
                if not words:
                    pass
                elif words[0] == keyword:
                    new_file.write(line.replace(line, keyword + " " + str(value) + "\n"))
                else:
                    new_file.write(line)
    # Remove original file
    remove(directory_file)
    # Move new file
    move(abs_path, directory_file)


def set_jobname(name, directory_file):
    fh, abs_path = mkstemp()
    with fdopen(fh, 'w') as new_file:
        with open(directory_file) as file:
            for line in file:
                if line.startswith('#SBATCH'):
                    if line.split()[1].startswith('--job-name='):
                        new_file.write(line.replace(line, '#SBATCH --job-name=' + name + "\n"))
                    else:
                        new_file.write(line)
                else:
                    new_file.write(line)
    # Remove original file
    remove(directory_file)
    # Move new file
    move(abs_path, directory_file)


def adjust_line_under_key(keyword, value, directory_file):
    # ==================================================================
    # looks up "directory_file" for the given "keyword" and substitutes everything behind it
    # with "value"
    fh, abs_path = mkstemp()
    with fdopen(fh, 'w') as new_file:
        with open(directory_file) as old_file:
            for line in old_file:
                words = line.split()
                if not words:
                    pass
                elif words[0] == keyword:
                    new_file.write(line)
                    line2 = next(old_file)
                    new_file.write(line2.replace(line2, str(value) + "\n"))
                else:
                    new_file.write(line)
    # Remove original file
    remove(directory_file)
    # Move new file
    move(abs_path, directory_file)


def adjust_parameter_new_version(keyword, value, directory_file):
    # ==================================================================
    # looks up "directory_file" for the given "keyword" and substitutes everything behind it
    # with "value"
    keyword_array = keyword.split()
    fh, abs_path = mkstemp()
    with fdopen(fh, 'w') as new_file:
        with open(directory_file) as old_file:
            for line in old_file:
                words = line.split()
                # keywords can consist of more than one word. Every word has to match the corresponding element of the current line
                keyword_match = True
                set_space = True
                if len(keyword_array) == 0 or len(keyword_array) > len(words):
                    keyword_match = False
                else:
                    for i in range(0, len(keyword_array)):
                        if keyword_array[i] not in words[i]:
                            keyword_match = False
                        elif keyword_array[i] != words[i]:
                            set_space = False
                if not words:
                    pass
                elif keyword_match == True:
                    if set_space == True:
                        new_file.write(line.replace(line, keyword + " " + str(value) + "\n"))
                    else:
                        new_file.write(line.replace(line, keyword + str(value) + "\n"))
                else:
                    new_file.write(line)
    # Remove original file
    remove(directory_file)
    # Move new file
    move(abs_path, directory_file)


def make_file(filename):
    # ==================================================================
    # simple touch
    bashCommand = "touch " + str(filename)
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()


def call_spin(pathtoexecutable: PathLike = None) -> None:
    r"""
    Calls the spin D algorithm

    Args:
        pathtoexecutable(PathLike, Optional): the path to the SpinD executable. The default is None. In that case the
        default Linux or Windows paths is chosen based on the OS.
    """
    if pathtoexecutable is None:
        if OPERATINGSYSTEM == 'Windows':
            command = const.SPIND_WINDOWS
        elif OPERATINGSYSTEM == 'Linux':
            command = const.SPIND_LINUX
        else:
            raise Exception('operating system not yet coded.')
    else:
        command = pathtoexecutable
    with open('job.out', 'a') as f:
        process = subprocess.Popen(command.split(), stdout=f, shell=True)
    output, error = process.communicate()


def backuping_mkdir(directory):
    # ==================================================================
    # copies folder to oldVersion if already exists and then creates new one as required
    if os.path.isdir(directory):
        temp_directory = directory + "_backup"
        i = 1
        while os.path.isdir(temp_directory):
            temp_directory = directory + "_backup" + str(i)
            i += 1
        print(
            'directory ' + '\"' + directory + '\" ' + 'already exists : backuping old version to ' + '\"' + temp_directory + '\"')
        copy_folder(directory, temp_directory)
        remove_folder(directory)
    make_directory(directory)
    time.sleep(1.0)


def backuping_touch(filename):
    # ==================================================================
    # copies file to oldVersion if already exists and then creates new one as required
    if Path(filename).is_file():
        temp_file = filename + "_backup"
        i = 1
        while Path(temp_file).is_file():
            temp_file = filename + "_backup" + str(i)
            i += 1
        print(
            'file ' + '\"' + filename + '\" ' + 'already exists : backuping old version to ' + '\"' + temp_file + '\"')
        copy_element(filename, temp_file)
        remove_element(filename)
    make_file(filename)
    time.sleep(1.0)


def cluster():
    # ==================================================================
    # reads the current machines name and returns the bool variable @cluster
    bashCommand = 'hostname'
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    # ADD INDICATOR FOR YOUR MACHINE NAME HERE
    # OUTPUT IS IN FORMAT bytestream SO USE @b IN FRONT OF STRING
    desktop_machine_names = [b'goerzen', b'sh8', b'DESKTOP-TIBLOAM']
    for name in desktop_machine_names:
        if output.startswith(name):
            return False
    # MACHINE IS CONSIDERED TO BE SLURM CLUSTER IF NAMES DID NOT MATCH
    return True


def read_last_line(filename):
    # ==================================================================
    num_lines = sum(1 for line in open(filename))
    with open(filename, 'rb') as f:
        if num_lines > 1:
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b'\n':
                f.seek(-2, os.SEEK_CUR)
            return f.readline().decode()
        else:
            return f.readline().decode()


def writelog(file: PathLike, message: str, end: str = '\n') -> None:
    r"""
    During testing one wants to show the result of the test within the console but also write a log file presenting
    the results of the tests for later usage.

    Args:
        file(PathLike): log file

        message(str): message which is printed as well as written to the logfile

        end(str): indicator for the end of the lie
    """
    print(message, end=end)
    with open(file, 'a') as f:
        f.write(message + end)


def startlogger(file: PathLike) -> None:
    r"""
    Starts the logging.

    Args:
        file(PathLike): log file
    """
    if os.path.isfile(file):
        remove_element(file)
    writelog(file=file, message='#' * 100)
    writelog(file=file, message=f'Test were run at: {datetime.now()}')
    writelog(file=file, message='#' * 100)
