import os

import pytest

from d8s_yaml import yaml_read, is_yaml, yaml_write, yaml_sort, yaml_files, yaml_clean
from d8s_file_system import directory_delete, directory_create, file_write

NON_EXISTENT_FILE_PATH = './foo'
TEST_DIRECTORY_PATH = './test_files'
TEST_FILE_CONTENTS = 'a'
TEST_FILE_NAME_A = 'a.yml'
TEST_FILE_PATH_A = os.path.join(TEST_DIRECTORY_PATH, TEST_FILE_NAME_A)
TEST_FILE_NAME_B = 'a.yaml'
TEST_FILE_PATH_B = os.path.join(TEST_DIRECTORY_PATH, TEST_FILE_NAME_B)


@pytest.fixture(autouse=True)
def clear_testing_directory():
    """This function is run after every test."""
    directory_delete(TEST_DIRECTORY_PATH)
    directory_create(TEST_DIRECTORY_PATH)
    file_write(TEST_FILE_PATH_A, TEST_FILE_CONTENTS)
    file_write(TEST_FILE_PATH_B, TEST_FILE_CONTENTS)


def setup_module():
    """This function is run before all of the tests in this file are run."""
    directory_create(TEST_DIRECTORY_PATH)


def teardown_module():
    """This function is run after all of the tests in this file are run."""
    directory_delete(TEST_DIRECTORY_PATH)


def test_yaml_files_1():
    result = yaml_files(TEST_DIRECTORY_PATH)
    assert result == ['a.yaml']

    result = yaml_files(TEST_DIRECTORY_PATH, include_yml_extensions=True)
    assert result == ['a.yaml', 'a.yml']


def test_yaml_clean_1():
    s = '''b:
  d: 2
  c: [3, 4]
a: Easy!'''
    result = yaml_clean(s)
    assert (
        result
        == '''a: Easy!
b:
  c:
  - 3
  - 4
  d: 2
'''
    )


def test_yaml_sort_1():
    s = '''b:
  d: 2
  c: [3, 4]
a: Easy!'''

    result = yaml_read(s)
    assert result == {'b': {'d': 2, 'c': [3, 4]}, 'a': 'Easy!'}

    result = yaml_sort(s)
    assert result == '''a: Easy!\nb:\n  c:\n  - 3\n  - 4\n  d: 2\n'''


def test_yaml_read_1():
    s = '''sunday: 10
monday: 11'''
    result = yaml_read(s)
    assert result == {'monday': 11, 'sunday': 10}

    s = '''
a: Easy!
b:
  c: 2
  d: [3, 4]
'''
    result = yaml_read(s)
    print(result)
    assert result == {'a': 'Easy!', 'b': {'c': 2, 'd': [3, 4]}}


def test_yaml_write_1():
    d = {'a': 'Easy!', 'b': {'c': 2, 'd': [3, 4]}}
    result = yaml_write(d)
    assert result == 'a: Easy!\nb:\n  c: 2\n  d:\n  - 3\n  - 4\n'


def test_is_yaml_1():
    s = '''sunday: 10
monday: 11'''
    assert is_yaml(s)

    s = '''foo:: bar
bing buzz boo'''
    assert not is_yaml(s)
