import os

import pytest
from d8s_file_system import directory_create, directory_delete, file_write

from d8s_archives import archive_create, archive_read

from .test_archive_utils import subprocess_run

TEST_DIRECTORY_PATH = './_test_data/archive/'
TEST_DIRECTORY_BASE_PATH = './_test_data/'
DEFAULT_FILE_CONTENTS = 'abc'


@pytest.fixture(autouse=True)
def clear_testing_directory():
    """This function is run after every test."""
    directory_delete(TEST_DIRECTORY_PATH)
    directory_create(TEST_DIRECTORY_PATH)


def setup_module():
    """This function is run before all of the tests in this file are run."""
    directory_create(TEST_DIRECTORY_PATH)


def teardown_module():
    """This function is run after all of the tests in this file are run."""
    directory_delete(TEST_DIRECTORY_BASE_PATH)


def _create_sample_file(path, contents=DEFAULT_FILE_CONTENTS):
    full_path = os.path.join(TEST_DIRECTORY_PATH, path)
    result = file_write(full_path, contents)
    assert result
    return full_path


def test_archive_read():
    file_path = _create_sample_file('a')
    output_dir = '_test_data/archive/a.zip'

    archive_create(file_path, output_dir)
    assert list(archive_read(output_dir)) == [('a', DEFAULT_FILE_CONTENTS)]
    assert list(archive_read(output_dir, archive_name='a')) == [('a', DEFAULT_FILE_CONTENTS)]


def test_archive_read_password_encrypted():
    password = 'foo'

    file_path = _create_sample_file('a')
    zip_path = os.path.join(TEST_DIRECTORY_PATH, 'a.zip')
    command = f'zip -P foo {zip_path} {file_path}'
    subprocess_run(command, input_=password)

    results = list(archive_read(zip_path, password=password))
    assert results == [('_test_data/archive/a', 'abc')]
