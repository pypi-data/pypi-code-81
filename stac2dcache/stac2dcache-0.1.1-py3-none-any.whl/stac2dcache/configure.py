import aiohttp
import configparser
import dcachefs
import fsspec
import pathlib

from .io import IO


fsspec.register_implementation("dcache", dcachefs.dCacheFileSystem)


def configure(filesystem="https", username=None, password=None,
              token_filename=None):
    """
    Set up a remote file system with the provided authentication credentials
    (username/password or bearer-token) and configure custom read/write methods
    for PySTAC

    :param filesystem: (str)
    :param username: (optional, str)
    :param password: (optional, str)
    :param token_filename: (optional, str) path to file with the token
    """
    fs = configure_filesystem(filesystem, username, password, token_filename)
    io = IO(filesystem_from=fs, filesystem_to=fs)
    io.set_custom_reader_and_writer()
    return fs


def configure_filesystem(filesystem="https", username=None, password=None,
                         token_filename=None):
    """
    Set up a remote file system with the provided authentication credentials
    (username/password or bearer-token)

    :param filesystem: (str)
    :param username: (optional, str)
    :param password: (optional, str)
    :param token_filename: (optional, str) path to file with the token
    """
    client_kwargs = {}
    # use username/password authentication
    if (username is None) ^ (password is None):
        raise ValueError("Username or password not provided")
    if (username is not None) and (password is not None):
        client_kwargs.update(auth=aiohttp.BasicAuth(username, password))

    # use bearer token authentication
    token = _get_token(token_filename)
    if token is not None:
        if password is not None:
            raise ValueError("Provide either token or username/password")
        client_kwargs.update(headers=dict(Authorization=f"Bearer {token}"))

    # get fsspec filesystem
    filesystem_class = fsspec.get_filesystem_class(filesystem)
    filesystem = filesystem_class(
        client_kwargs=client_kwargs,
        block_size=0,  # stream mode
    )
    return filesystem


def _get_token(filename=None):
    """
    Read the token from a file

    :param filename: (optional, str) name of the file
    """
    token = None
    if filename is not None:
        filepath = pathlib.Path(filename)
        assert filepath.exists(), f'Token file {filepath.as_posix()} not found'
        if filepath.suffix == '.conf':
            token = _parse_rclone_config_file(filepath)
        else:
            token = _parse_plain_file(filepath)
    return token


def _parse_rclone_config_file(filename):
    filepath = pathlib.Path(filename)
    config = configparser.ConfigParser()
    config.read(filepath)
    return config[filepath.stem]['bearer_token']


def _parse_plain_file(filename):
    filepath = pathlib.Path(filename)
    with filepath.open() as f:
        return f.read().strip()
