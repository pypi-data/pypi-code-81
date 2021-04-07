import re
from pathlib import Path
import os

configuration_file_name = '.ros_configuration_file'
ROS_MASTER_URI = 'ROS_MASTER_URI'
ROS_HOSTNAME = 'ROS_HOSTNAME'
IP_CONFIG_LINES = {ROS_MASTER_URI: 'export ROS_MASTER_URI=', ROS_HOSTNAME: 'export ROS_HOSTNAME='}


class RosParameters:
    def __init__(self):
        self._ip_config_lines: dict = {ROS_MASTER_URI: 'http://127.0.0.1:11311/', ROS_HOSTNAME: '127.0.0.1'}
        self._source_config_lines: list = []

        # Read the file (if exists) and get the parameters
        try:
            open(Path.home() / configuration_file_name, 'r')
        except FileNotFoundError:
            open(Path.home() / configuration_file_name, 'w').close()

        configuration_file = open(Path.home() / configuration_file_name, 'r')

        # Read the config file to populate the class
        for line in configuration_file.readlines():
            # Check if it is a source line
            match_source_line = re.search('^source ([a-zA-Z0-9~\/\-_\.]*)$', line)
            match_env_variable = re.search('^([a-zA-Z0-9\-_])=([a-zA-Z0-9~\/\-_:]*)$', line)
            if match_source_line:
                self._source_config_lines.append(match_source_line.group(1))

            #Chek it the line is a env variable
            elif match_env_variable:
                variable_name = match_env_variable.group(0)
                variable_value = match_env_variable.group(2)
                self._ip_config_lines[variable_name] = variable_value

        configuration_file.close()

    def set_ros_master_uri(self, master_uri: str):
        self._ip_config_lines[ROS_MASTER_URI] = 'http://' + master_uri + ':11311/'

    def set_ros_hostname(self, hostname):
        self._ip_config_lines[ROS_HOSTNAME] = hostname

    def get_source_files(self) -> list:
        return self._source_config_lines

    def add_source_file(self, path: str):
        if path == '.':
            path = os.path.join(os.getcwd(), 'devel', 'setup.bash')
        self._source_config_lines.append(path)

    def remove_source_file(self, number: int):
        if 0 <= number < len(self._source_config_lines):
            self._source_config_lines = self._source_config_lines[:number] + self._source_config_lines[number + 1:]

    def write_file(self):
        configuration_file = open(Path.home() / configuration_file_name, 'w')
        for source_file in self._source_config_lines:
            configuration_file.write('source ' + source_file + '\n')

        for key, value in self._ip_config_lines.items():
            configuration_file.write(IP_CONFIG_LINES[key] + value + '\n')

        configuration_file.close()

