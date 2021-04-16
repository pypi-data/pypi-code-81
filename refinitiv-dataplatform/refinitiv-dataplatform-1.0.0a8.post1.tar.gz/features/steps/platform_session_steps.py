from unittest.mock import patch

from behave import *
import env
import refinitiv.dataplatform as rdp


@step("I input '{text}' RDP credentials")
def step_impl(context, text):
    session = context.session

    if text == "valid":
        session._app_key = env.desktop_app_key
        session._grant._username = env.edp_username
        session._grant._password = env.edp_password

    elif text == "invalid":
        session._app_key = env.invalid_desktop_app_key
        session._grant._username = env.invalid_edp_username
        session._grant._password = env.invalid_edp_password


@step("I input the '{text}' host value")
def step_impl(context, text):
    deployed_platform_host = ""
    if text == 'valid':
        deployed_platform_host = env.deployed_platform_host
    elif text == 'invalid':
        deployed_platform_host = env.invalid_deployed_platform_host

    session = context.session
    # session._connection_type = rdp.PlatformSession.PlatformConnectionType.RefinitivDataplatformConectionAndDeployedPlatform
    session._connection = rdp.connection.RefinitivDataAndDeployedConnection(session)
    session._deployed_platform_host = deployed_platform_host


@when("My token is going to expire")
def step_impl(context):
    token_expires_at = context.session._token_expires_at
    token_expires_in_secs = context.session._token_expires_in_secs
    assert token_expires_in_secs == 5, token_expires_in_secs
    assert token_expires_at is not None


@then("I receive new valid token with platform session")
def step_impl(context):
    import asyncio

    with patch('refinitiv.dataplatform.Session.set_stream_authentication_token') as mock:
        while mock.call_count == 0:
            asyncio.get_event_loop().run_until_complete(asyncio.sleep(1))

        mock.assert_called_once()


@step("I receive a notification that token refresh success")
def step_impl(context):
    state_code = context.state_code
    state_msg = context.state_msg

    assert state_code is not None
    assert state_code == rdp.Session.State.Open
    assert state_msg is not None

    context.session.close()


@when("My attempt to refresh token with platform session is failed")
def step_impl(context):
    import asyncio

    with patch('httpx.AsyncClient.send') as mock:
        mock.side_effect = Exception("MockException")

        counter = 10
        while counter:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.sleep(1))
            counter -= 1


@then("I receive a notification that token refresh failed")
def step_impl(context):
    event_code = context.event_code
    event_msg = context.event_msg

    assert event_code is not None
    assert event_code == rdp.Session.EventCode.SessionAuthenticationFailed
    assert event_msg is not None


@step("Session stops requesting a new token and is closed")
def step_impl(context):
    session = context.session
    assert session._auth_manager.is_closed() is True


@then("I receive a notification that '{text}'")
def step_impl(context, text):
    assert context.event_code is not None

    if text == 'StreamDisconnected':
        assert context.event_code == context.session.EventCode.StreamDisconnected

    assert context.event_msg is not None


@step("I receive a notification that session is closed")
def step_impl(context):
    state_code = context.state_code
    state_msg = context.state_msg

    assert state_code is not None
    assert state_code is rdp.Session.State.Closed
    assert state_msg is not None


@then('I receive error message "{error_msg}"')
def step_impl(context, error_msg):
    session = context.session

    assert session._app_key == error_msg
