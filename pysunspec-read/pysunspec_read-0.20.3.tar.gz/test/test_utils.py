import json
import logging
import os
import shutil
import tempfile
from pathlib import Path

log = logging.getLogger(__name__)


def assert_json_files_equals(self, actual_json_path, expected_json_path_relative_to_test):
    expected_path = Path(get_test_folder(), expected_json_path_relative_to_test)
    with open(expected_path, mode='r', newline=None) as expected, open(actual_json_path, 'r') as actual:
        expected_json = expected.read()
        actual_json = actual.read()
        print(actual_json)
        self.assertEqual(expected_json, actual_json)


def assert_json_equals(self, json_str, expected_json_path_relative_to_test):
    expected_path = Path(get_test_folder(), expected_json_path_relative_to_test)
    with open(expected_path, mode='r', newline=None) as expected:
        expected_json = expected.read()
        print(json_str)
        self.assertEqual(expected_json, json_str)


def load_resource_as_string(resource_path_string_relative_to_test):
    resource_path = get_resource_path(resource_path_string_relative_to_test)
    return load_path_as_string(resource_path)


def load_path_as_string(path):
    with open(path, mode='r', newline=None) as expected:
        content = expected.read()
    return content


def load_resource_as_json(json_path_relative_to_test):
    resource_path = get_resource_path(json_path_relative_to_test)
    return load_path_as_json(resource_path)


def load_path_as_json(path):
    content = load_path_as_string(path)
    return json.loads(content)


def get_resource_path(path_relative_to_test_folder: str):
    return Path(get_test_folder(), path_relative_to_test_folder)


def get_test_folder():
    return get_folder()


def get_folder(name: str = "test"):
    nested = 1
    current_folder = Path(".").absolute()
    while current_folder.name != name:
        print("looking for {name} folder, currently at {current}".format(name=name,
                                                                         current=current_folder.name + " " + str(
                                                                             current_folder)))
        current_folder = current_folder.parent
        nested += 1
        if nested == 10:
            break
    log.debug("found {name} folder {current}".format(name=name, current=str(current_folder)))
    return current_folder.absolute()


def get_temp_file(dirname: str, filename: str):
    output_file = Path(tempfile.gettempdir(), dirname, filename)
    os.makedirs(output_file.parent)
    return output_file


def get_temp_dir(dirname: str, create: bool = True):
    temp_dir = Path(tempfile.gettempdir(), dirname)
    if create:
        temp_dir.mkdir(exist_ok=True)
    return temp_dir


def cleanup(name):
    temp_dir = get_temp_dir(name, create=False)
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
