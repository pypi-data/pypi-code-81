from unittest.mock import MagicMock

from behave import *
import refinitiv.dataplatform as rdp

from requests_async import codes as requests_async_codes
import env


@when("I input the correct application key and port number")
def step_impl(context):
    session = context.session
    session._app_key = env.desktop_app_key
    session.set_port_number(port_number=9000)


@when("I input the incorrect application key")
def step_impl(context):
    session = context.session
    session._app_key = env.invalid_desktop_app_key


@step('I receive an error notification: "{error_msg}"')
def step_impl(context, error_msg):
    session = context.session
    is_open = session.is_open()
    event_code = context.event_code
    event_msg = context.event_msg

    assert event_code
    assert event_code == rdp.Session.EventCode.SessionAuthenticationFailed
    assert event_msg
    assert error_msg in event_msg
    assert not is_open


@then('I receive an error notification about Api Proxy port: "{error_msg}", network error')
def step_impl(context, error_msg):
    session = context.session
    is_open = session.is_open()
    event_code = context.event_code
    event_msg = context.event_msg

    assert event_code
    assert event_code == rdp.Session.EventCode.SessionAuthenticationFailed
    assert event_msg
    assert error_msg in event_msg
    assert not is_open


@step("I have an Eikon application is not running")
def step_impl(context):
    async def check_port_dummy(*args, **kwargs):
        pass

    session = context.session
    session.check_port = check_port_dummy
    session._check_port_result = False


@step("I have an Eikon application is running")
def step_impl(context):
    response = MagicMock()

    async def http_request_async_dummy(*args, **kwargs):
        body = kwargs.get('json')
        if body.get('AppKey') == env.invalid_desktop_app_key:
            response.status_code = requests_async_codes.bad
        else:
            response.status_code = requests_async_codes.ok
        return response

    async def check_port_dummy(*args, **kwargs):
        pass

    session = context.session
    session.check_port = check_port_dummy
    session._check_port_result = True
    session.http_request_async = http_request_async_dummy
