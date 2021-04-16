from behave import given

import refinitiv.dataplatform as rdp
import env


@given(u'platform session created')
def step_impl(context):
    params = {
        "oauth_grant_type": rdp.GrantPassword(
            username=env.edp_username,
            password=env.edp_password
        ),
        "app_key": env.desktop_app_key,
        "take_signon_control": True
    }
    platform_session = rdp.CoreFactory.create_platform_session(**params)
    context.platform_session = platform_session


@given(u'platform session opens')
def step_impl(context):
    session = context.platform_session
    session.open()
    rdp.legacy.set_default_session(session)


