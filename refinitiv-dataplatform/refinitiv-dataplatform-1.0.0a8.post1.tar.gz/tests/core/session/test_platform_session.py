from mock import MagicMock

import conftest
import refinitiv.dataplatform as rdp


def test_refresh_token_event():
    """
    AuthenticationToken :: No "refresh_token" event in platform session.
    https://jira.refinitiv.com/browse/EAPI-628
    """

    async def mock_http_request_async(*args, **kwargs):
        mock_response = MagicMock()
        if 'refresh_token' in kwargs.get('data', {}):
            mock_response.status_code = 504
        else:
            mock_response.status_code = 200
            mock_response.json.return_value = {"expires_in": 2, "refresh_token": "refresh_token", "access_token": "access_token"}
        return mock_response

    event_code = None

    def on_event(*args, **kwargs):
        nonlocal event_code
        _, event_code, _ = args
        print(event_code)

    params = {
        "app_key": conftest.DESKTOP_APP_KEY,
        "oauth_grant_type": rdp.GrantPassword(
            username=conftest.EDP_USERNAME,
            password=conftest.EDP_PASSWORD
            ),
        "take_signon_control": True,
        "on_event": on_event,
        }
    session = rdp.CoreFactory.create_platform_session(**params)
    session.http_request_async = mock_http_request_async

    session.open()
    assert session.is_open() is True

    import asyncio
    asyncio.get_event_loop().run_until_complete(asyncio.sleep(5))

    assert event_code == rdp.PlatformSession.EventCode.SessionAuthenticationFailed
    assert event_code == session._status

