import re
from pathlib import Path

from termcolor import colored

from ros_configurator.ros_parameters import configuration_file_name


def check_source_ros_configuration_file():
    try:
        open(Path.home() / '.bashrc', 'r')
    except FileNotFoundError:
        colored('.bashrc file does not exists!', 'red')

    bashrc_file = open(Path.home() / '.bashrc', 'r')
    for line in bashrc_file.readlines():
        if re.match('^source ~/' + configuration_file_name + '$', line):
            bashrc_file.close()
            return True

    bashrc_file.close()
    return False


def configure_bashrc():
    try:
        open(Path.home() / '.bashrc', 'r')
    except FileNotFoundError:
        colored('.bashrc file does not exists!', 'red')

    if not check_source_ros_configuration_file():
        bashrc_file = open(Path.home() / '.bashrc', 'a')
        bashrc_file.write('source ~/' + configuration_file_name + '\n')
        bashrc_file.close()




