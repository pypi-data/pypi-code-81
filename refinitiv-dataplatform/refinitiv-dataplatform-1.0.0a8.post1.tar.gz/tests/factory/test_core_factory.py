from importlib import reload

import pytest

import refinitiv.dataplatform as rdp
from conftest import DESKTOP_APP_KEY, EDP_USERNAME, EDP_PASSWORD, request_desktop_api
from refinitiv.dataplatform import configure


def test_create_session_platform(write_project_config):
    write_project_config(
        {
            "sessions": {
                "platform": {
                    "my-session": {
                        "app_key":  DESKTOP_APP_KEY,
                        "username": EDP_USERNAME,
                        "password": EDP_PASSWORD,
                        "base-url": "https://api.refinitiv.com",
                        "auth":     {
                            "url":       "/auth/oauth2/v1",
                            "authorize": "/authorize",
                            "token":     "/token"
                            }
                        }
                    },
                },
            }
        )
    reload(configure)
    session = rdp.create_session('my-session')
    assert session
    session.open()
    assert session.is_open() is True
    assert isinstance(session, rdp.PlatformSession)
    session.close()


def test_create_session_desktop(write_project_config):
    write_project_config(
        {
            "sessions": {
                "desktop": {
                    "my-session": {
                        "app_key":        DESKTOP_APP_KEY,
                        "base-url":       "http://127.0.0.1:9000",
                        "platform-paths": {
                            "rdp": "/api/rdp",
                            "udf": "/api/udf"
                            },
                        "handshake-url":  "/api/handshake"
                        }
                    },
                },
            }
        )
    reload(configure)
    session = rdp.create_session('my-session')
    assert session

    success = request_desktop_api()

    if success:
        session.open()
        assert session.is_open() is True

    assert isinstance(session, rdp.DesktopSession)
    session.close()


def test_create_session_same_name_for_desktop_and_platform(write_project_config):
    write_project_config(
        {
            "sessions": {
                "platform": {
                    "my-session": {
                        "app_key":  DESKTOP_APP_KEY,
                        "username": EDP_USERNAME,
                        "password": EDP_PASSWORD,
                        "base-url": "https://api.refinitiv.com",
                        "auth":     {
                            "url":       "/auth/oauth2/v1",
                            "authorize": "/authorize",
                            "token":     "/token"
                            }
                        }
                    },
                "desktop":  {
                    "my-session": {
                        "app_key":        DESKTOP_APP_KEY,
                        "base-url":       "http://127.0.0.1:9000",
                        "platform-paths": {
                            "rdp": "/api/rdp",
                            "udf": "/api/udf"
                            },
                        "handshake-url":  "/api/handshake"
                        }
                    }
                },
            }
        )
    reload(configure)
    session = rdp.create_session('my-session')
    assert session
    session.open()
    assert session.is_open() is True
    assert isinstance(session, rdp.PlatformSession)
    session.close()


def test_create_session_platform_raise_not_define(write_project_config):
    write_project_config(
        {
            "sessions": {
                "platform": {
                    "my-session": {
                        "base-url": "https://api.refinitiv.com",
                        "auth":     {
                            "url":       "/auth/oauth2/v1",
                            "authorize": "/authorize",
                            "token":     "/token"
                            }
                        }
                    },
                },
            }
        )
    reload(configure)

    with pytest.raises(rdp.RDPError, match='Configuration does not define'):
        rdp.create_session('my-session')


def test_create_session_desktop_raise_not_define(write_project_config):
    write_project_config(
        {
            "sessions": {
                "desktop": {
                    "my-session": {
                        "base-url":       "http://127.0.0.1:9000",
                        "platform-paths": {
                            "rdp": "/api/rdp",
                            "udf": "/api/udf"
                            },
                        "handshake-url":  "/api/handshake"
                        }
                    },
                },
            }
        )
    reload(configure)

    with pytest.raises(rdp.RDPError, match='Configuration does not define'):
        rdp.create_session('my-session')


def test_create_session_raise_cannot_find():
    reload(configure)
    session_name = 'my-session'
    with pytest.raises(rdp.RDPError, match=f'Cannot find session configuration with name "{session_name}"'):
        rdp.create_session(session_name)
