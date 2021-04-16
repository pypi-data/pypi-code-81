import os
import random
from importlib import reload

import conftest
from refinitiv.dataplatform import configure


# region DEFAULT_CONFIG_FILE
def test_default_config_file_path():
    reload(configure)
    assert 3 == len(configure._config_files_paths)


# endregion


# region USER_CONFIG_FILE
def test_user_config_file_path_not_exists(user_config_path, write_user_config):
    path = write_user_config('{"prop": "value"}')

    reload(configure)
    assert 3 == len(configure._config_files_paths)
    assert path == configure._config_files_paths[1]

    conftest.remove_user_config()

    reload(configure)
    assert 3 == len(configure._config_files_paths)
    assert path != configure._config_files_paths[0]


def test_user_config_file_path_already_exists(write_user_config):
    path = write_user_config('{"prop": "value"}')

    reload(configure)
    assert 3 == len(configure._config_files_paths)
    assert path == configure._config_files_paths[1]
    assert path != configure._config_files_paths[0]


def test_user_config_file_path_created_after_load_package(user_config_path):
    conftest.remove_user_config()

    reload(configure)
    with open(user_config_path, 'w'):
        pass
    assert 3 == len(configure._config_files_paths)
    assert user_config_path != configure._config_files_paths[0]

    conftest.remove_user_config()


# endregion


# region PROJECT_CONFIG_FILE
def test_project_config_file_path_not_exists(project_config_path):
    conftest.remove_project_config()

    reload(configure)
    assert 3 == len(configure._config_files_paths)
    assert project_config_path != configure._config_files_paths[2]


def test_project_config_file_path_already_exists(write_project_config):
    path = write_project_config('{"prop":"value"}')

    reload(configure)
    assert 3 == len(configure._config_files_paths)
    assert path == configure._config_files_paths[0]
    assert path != configure._config_files_paths[1]


def test_project_config_file_path_created_at_runtime(project_config_path):
    conftest.remove_project_config()

    reload(configure)
    with open(project_config_path, 'w'):
        pass
    assert 3 == len(configure._config_files_paths)
    assert project_config_path != configure._config_files_paths[2]


# endregion

def test_environ_env_name_and_env_dir(monkeypatch, tmpdir):
    env_name = str(random.randint(0, 100))
    env_dir = str(random.randint(0, 100))
    d = tmpdir / env_dir
    d.mkdir()
    f = tmpdir / env_dir / (configure._config_filename_template % env_name)
    f.write('{"prop": "value"}')

    monkeypatch.setenv(configure._RDPLIB_ENV, env_name)
    monkeypatch.setenv(configure._RDPLIB_ENV_DIR, str(d))

    reload(configure)

    assert env_name in configure._config_filename
    assert env_name == configure._env_name
    assert d == configure._project_config_dir
    assert 3 == len(configure._config_files_paths)
    assert f == configure._config_files_paths[0]


def test_environ_env_name(monkeypatch):
    from pathlib import Path

    env_name = str(random.randint(0, 100))

    f = Path(os.getcwd()) / (configure._config_filename_template % env_name)
    f.write_text('{"prop": "value"}', encoding='utf-8')

    monkeypatch.setenv(configure._RDPLIB_ENV, env_name)
    monkeypatch.delenv(configure._RDPLIB_ENV_DIR, raising=False)

    reload(configure)
    assert env_name in configure._config_filename
    assert env_name == configure._env_name
    assert os.getcwd() == configure._project_config_dir
    assert 3 == len(configure._config_files_paths)
    assert str(f) == configure._config_files_paths[0]

    f.unlink()
    monkeypatch.delenv(configure._RDPLIB_ENV, raising=False)


def test_environ_env_dir(monkeypatch, tmpdir):
    reload(configure)
    env_dir = str(random.randint(0, 100))
    d = tmpdir / env_dir
    d.mkdir()
    f = tmpdir / env_dir / configure._config_filename
    f.write('{"prop": "value"}')

    monkeypatch.delenv(configure._RDPLIB_ENV, raising=False)
    monkeypatch.setenv(configure._RDPLIB_ENV_DIR, str(d))

    reload(configure)
    assert d == configure._project_config_dir
    assert 3 == len(configure._config_files_paths)
    assert str(f) == configure._config_files_paths[0]


def test_environ_empty(monkeypatch):
    from pathlib import Path

    f = Path(os.getcwd()) / configure._config_filename
    f.write_text('{"prop": "value"}', encoding='utf-8')

    monkeypatch.delenv(configure._RDPLIB_ENV, raising=False)
    monkeypatch.delenv(configure._RDPLIB_ENV_DIR, raising=False)

    reload(configure)
    assert os.getcwd() == configure._project_config_dir
    assert 3 == len(configure._config_files_paths)
    assert str(f) == configure._config_files_paths[0]

    f.unlink()
