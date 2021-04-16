from http import HTTPStatus
from urllib.parse import urljoin

import pytest
import requests

from atoti.session import Session


@pytest.mark.legacy_app
def test_legacy_url_returns_content(session: Session):
    legacy_url = urljoin(f"{session.url}/", "legacy/")
    res = requests.get(legacy_url)
    assert res.status_code == HTTPStatus.OK
