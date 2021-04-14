
import os

import pytest
import requests

from ..client import RedPocket, RedPocketLoginError

DIRPATH = os.path.dirname(__file__)


def test_fail_login():

    with pytest.raises(RedPocketLoginError):
        RedPocket(
            username='fakeUsername',
            password='realPassword',
        )


def test_extract_csrf_at_all():

    client = RedPocket(
        username='fakeUsername',
        password='realPassword',
        auto=False,
    )

    req = requests.get('https://redpocket.com/login')
    req.raise_for_status()

    client._extract_csrf(req.text)


def test_extract_csrf_correct():

    client = RedPocket(
        username='fakeUsername',
        password='realPassword',
        auto=False,
    )

    with open(DIRPATH + '/data/login.html', 'r') as fil:
        html = fil.read()

    csrf = client._extract_csrf(html)

    assert csrf == \
        '5b0ef5c21e548e99d6c12226223f5850-7ed41f7da4818f6a4f56f860d47020d7'
