import socket

from termcolor import colored

from ros_configurator.ros_parameters import RosParameters
from ros_configurator.utilities import configure_bashrc

def get_ip():
    return socket.gethostbyname(socket.gethostname())


def set_ip_localhost():
    ros_parameters = RosParameters()
    ros_parameters.set_ros_master_uri('127.0.0.1')
    ros_parameters.set_ros_hostname('127.0.0.1')
    ros_parameters.write_file()
    configure_bashrc()


def set_ip():
    ros_parameters = RosParameters()
    ip = get_ip()
    ros_parameters.set_ros_master_uri(ip)
    ros_parameters.set_ros_hostname(ip)
    ros_parameters.write_file()
    configure_bashrc()


def set_ros_master_uri():
    ros_parameters = RosParameters()
    ip = input('Insert the ros master IP\n')
    ros_parameters.set_ros_master_uri(ip)
    ros_parameters.write_file()


def list_source_files():
    ros_parameters = RosParameters()
    i = 0
    for file in ros_parameters.get_source_files():
        print(f'[{i}] -> {file}')
        i += 1


def add_source_file():
    file = input('Insert the file\'s path to source (type \'.\' if you are in a ros workspace)\n')
    ros_parameters = RosParameters()
    ros_parameters.add_source_file(file)
    ros_parameters.write_file()
    configure_bashrc()


def remove_source_file():
    ros_parameters = RosParameters()
    i = 0
    for file in ros_parameters.get_source_files():
        print(f'[{i}] -> {file}')
        i += 1

    number = int(input('Type the number of file to remove\n'))
    if number < 0 or number > len(ros_parameters.get_source_files()):
        colored(f'Please insert a number between 0 and {len(ros_parameters.get_source_files())}')
        return

    ros_parameters.remove_source_file(number)
    ros_parameters.write_file()
