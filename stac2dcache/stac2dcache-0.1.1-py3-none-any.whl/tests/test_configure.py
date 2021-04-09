import fsspec
import pystac
import pytest
import stac2dcache

from stac2dcache.configure import configure, configure_filesystem

from . import test_data_path


@pytest.fixture(scope="function")
def set_default_pystac_readers():
    yield
    pystac.STAC_IO.read_text_method = pystac.STAC_IO.default_read_text_method
    pystac.STAC_IO.write_text_method = pystac.STAC_IO.default_write_text_method


def test_configure_filesystem_returns_correct_fs_class():
    for fs_type in ("http", "dcache", "file"):
        fs_class = fsspec.get_filesystem_class(fs_type)
        fs = configure_filesystem(filesystem=fs_type)
        assert isinstance(fs, fs_class)


def test_configure_filesystem_sets_username_and_password():
    auth = dict(username="user", password="pass")
    for fs_type in ("http", "dcache"):
        fs = configure_filesystem(filesystem=fs_type,
                                  **auth)
        assert fs.client_kwargs['auth'].login == auth["username"]
        assert fs.client_kwargs['auth'].password == auth["password"]


def test_configure_filesystem_sets_token_filename():
    # test two formats for the token file
    for token_file in (test_data_path/"macaroon.conf",
                       test_data_path/"macaroon.dat"):
        for fs_type in ("http", "dcache"):
            fs = configure_filesystem(filesystem=fs_type,
                                      token_filename=token_file)
            assert "Authorization" in fs.client_kwargs["headers"]


def test_configure_filesystem_checks_authentication_methods():
    with pytest.raises(ValueError):
        configure_filesystem(username="user")  # missing password
    with pytest.raises(ValueError):
        configure_filesystem(username="user")  # missing username
    with pytest.raises(ValueError):
        configure_filesystem(token_filename=test_data_path/"macaroon.conf",
                             username="user",
                             password="passwd")  # uname/passwd and token


def test_configure_returns_correct_datatype(set_default_pystac_readers):
    for fs_type in ("http", "dcache", "file"):
        fs_class = fsspec.get_filesystem_class(fs_type)
        fs = configure(filesystem=fs_type)
        assert isinstance(fs, fs_class)


def test_configure_modifies_pystac_io_methods(set_default_pystac_readers):
    assert pystac.STAC_IO.read_text_method \
           == pystac.STAC_IO.default_read_text_method
    assert pystac.STAC_IO.write_text_method \
           == pystac.STAC_IO.default_write_text_method
    _ = configure()
    assert pystac.STAC_IO.read_text_method.__func__ == stac2dcache.io.IO.read
    assert pystac.STAC_IO.write_text_method.__func__ == stac2dcache.io.IO.write
