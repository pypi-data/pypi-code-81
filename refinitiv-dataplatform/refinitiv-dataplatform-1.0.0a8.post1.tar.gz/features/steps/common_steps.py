from behave import *

import refinitiv.dataplatform as rdp

from response_tests import success_response_tests, not_success_response_tests, success_response_without_data_tests

EventCode = rdp.Session.EventCode


@given("I want to set up '{session_type}' session")
def step_impl(context, session_type):
    def on_state(_, state_code, state_msg):
        if state_code is EventCode.SessionAuthenticationSuccess:
            session._token_expires_in_secs = 5

        context.state_code = state_code
        context.state_msg = state_msg

    def on_event(_, event_code, event_msg):
        context.event_code = event_code
        context.event_msg = event_msg

    session = None
    if session_type == 'desktop':
        session = rdp.CoreFactory.create_desktop_session(
            app_key="", on_state=on_state, on_event=on_event
            )
    elif session_type == 'platform':
        session = rdp.CoreFactory.create_platform_session(
            app_key="",
            oauth_grant_type=rdp.GrantPassword(),
            on_state=on_state, on_event=on_event
            )

    context.session = session


@step("I open session")
def step_impl(context):
    session = context.session
    session.open()


@then("I receive a notification that session is opened")
def step_impl(context):
    session = context.session
    state_code = context.state_code
    state_msg = context.state_msg

    assert session.is_open() is True, rdp.ContentFactory._last_error_status
    assert state_code is rdp.Session.State.Open
    assert state_msg is not None

    session.close()


@then('I receive response with status code "{status_code}"')
def step_impl(context, status_code):
    session = context.session
    is_open = session.is_open()
    event_code = context.event_code
    event_msg = context.event_msg

    assert event_code
    assert event_code == rdp.Session.EventCode.SessionAuthenticationFailed, event_code
    assert status_code in event_msg, status_code
    assert not is_open


@then(u'data is retrieved')
def step_impl(context):
    success_response_tests(context.response)


@then(u'error is received')
def step_impl(context):
    response = context.response
    not_success_response_tests(response, check_status=False)


@then(u'error is raised with message "{error_message}"')
def step_impl(context, error_message):
    assert context.error.message == error_message


@given(u'platform session closed')
def step_impl(context):
    context.platform_session.close()


@then(u'empty data is retrieved')
def step_impl(context):
    success_response_without_data_tests(context.response)


