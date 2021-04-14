import json

import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.parametrize(
    "data,success",
    [
        ({"username": "winstonsmith", "password": "goldstein"}, True),
        ({"username": "winstonsmith"}, False),
        ({"password": "goldstein"}, False),
    ],
)
def test_token_proxy(db, settings, admin_client, requests_mock, data, success):
    requests_mock.post(
        f"{settings.GWR_HOUSING_STAT_BASE_URI}/tokenWS/",
        json={"success": True, "token": "eyIMATOKEN"},
    )
    url = reverse("housingstattoken-list")

    resp = admin_client.post(
        url, data=json.dumps(data), content_type="application/json"
    )
    if success:
        assert resp.status_code == status.HTTP_201_CREATED
        assert resp.json() == {"token": "eyIMATOKEN"}
    else:
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert resp.json() == {
            "400": {
                "source": "internal",
                "reason": 'No housing stat credentials found for user "admin"',
            }
        }


@pytest.mark.parametrize(
    "housing_stat_creds__username,housing_stat_creds__password",
    [("winstonsmith", "goldstein")],
)
@pytest.mark.parametrize(
    "data",
    [
        {"username": "winston_smith", "password": "hunter2"},
        {"username": "winston_smith"},
        {"password": "hunter2"},
        {},
    ],
)
def test_token_proxy_success_existing_creds(
    db, settings, admin_client, requests_mock, housing_stat_creds, data
):
    requests_mock.post(
        f"{settings.GWR_HOUSING_STAT_BASE_URI}/tokenWS/",
        json={"success": True, "token": "eyIMATOKEN"},
    )
    url = reverse("housingstattoken-list")

    resp = admin_client.post(
        url, data=json.dumps(data), content_type="application/json"
    )
    assert resp.status_code == status.HTTP_201_CREATED

    housing_stat_creds.refresh_from_db()
    for k, v in data.items():
        assert getattr(housing_stat_creds, k) == v


def test_token_proxy_external_error(
    db, settings, admin_client, requests_mock, housing_stat_creds
):
    requests_mock.post(
        f"{settings.GWR_HOUSING_STAT_BASE_URI}/tokenWS/",
        status_code=401,
        text="wrong creds",
    )
    url = reverse("housingstattoken-list")

    resp = admin_client.post(url)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp.json() == {"401": {"reason": "wrong creds", "source": "external"}}
