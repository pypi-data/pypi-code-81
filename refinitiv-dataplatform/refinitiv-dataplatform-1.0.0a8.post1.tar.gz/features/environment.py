import refinitiv.dataplatform as rdp
import os
EventCode = rdp.Session.EventCode

desktop_app_key = os.environ.get('DESKTOP_APP_KEY')
edp_password = os.environ.get('EDP_PASSWORD')
edp_username = os.environ.get('EDP_USERNAME')


def before_scenario(context, scenario):
    def on_state(_, state_code, state_msg):
        if state_code is EventCode.SessionAuthenticationSuccess:
            session._token_expires_in_secs = 5

        context.state_code = state_code
        context.state_msg = state_msg

    def on_event(_, event_code, event_msg):
        context.event_code = event_code
        context.event_msg = event_msg
    session = None
    if 'desktop_session' in scenario.tags:
        session = rdp.CoreFactory.create_desktop_session(
            app_key="", on_state=on_state, on_event=on_event
        )

    if 'platform_session' in scenario.tags:
        session = rdp.CoreFactory.create_platform_session(
            app_key="",
            oauth_grant_type=rdp.GrantPassword(),
            on_state=on_state, on_event=on_event
        )
        session._app_key = desktop_app_key
        session._grant._username = edp_username
        session._grant._password = edp_password

    context.session = session


def after_scenario(context, scenario):
    if 'platform_session' in scenario.tags:
        session = context.session
        session.close()
        print("Result: " + scenario.status.name)

    if 'desktop_session' in scenario.tags:
        session = context.session
        session.close()
        print("Result: " + scenario.status.name)




