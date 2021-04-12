from splitcli.accounts import user
from splitcli.split_internal import login_internal, metrics_internal, traffictypes_internal, workshop_experiment, eventtypes_internal, definitions_internal
from splitcli.split_apis import splits_api, workspaces_api, segments_api, traffic_types_api
from splitcli.ux import menu
from splitcli.splitio_selectors import split_selectors, definition_selectors
from splitcli.experiment.experiment import Experiment

def admin_user():
    return 'workshop@split.io'

def admin_password():
    return 'Workshop_12345' # input('Provide Workshop Account Password: ')

_admin_session = None
def admin_session():
    global _admin_session
    if _admin_session == None:
        _admin_session = login_internal.login(admin_user(), admin_password())
    return _admin_session

def demo_base_url():
    return 'https://app.split.io/internal/api/splitAdmin/organization'

def demo_email_url():
    email = admin_user()
    base_url = demo_base_url()
    return f'{base_url}?email={email}'

def demo_org_url(org_id):
    base_url = demo_base_url()
    return f'{base_url}/{org_id}'


def create_org_workshop_imp():
    menu.success_message("Creating Implementation Workshop Organization")
    session = admin_session()
    response = session.post(demo_email_url(), headers={'Split-CSRF': session.cookies['split-csrf']})
    
    result = response.json()
    org_id = result['organizationId']

    menu.success_message("Logging in as User")
    user_session = login_internal.login(result['userEmail'],result['userPassword'])

    # Internal Actions
    menu.success_message("Deleting Metrics & Event Types")
    metrics_internal.delete_metrics(user_session, org_id)
    eventtypes_internal.delete_all_event_types(user_session, org_id)

    # Delete tokens
    menu.success_message("Creating Admin API Token")
    admin_token = login_internal.create_admin_token(user_session, org_id)

    # Shift Scope for External API actions
    base_user = user.get_user()
    org_user = user.User(admin_token, "", "", "", "", "")
    user.set_user(org_user)

    # External Actions
    workspaces = workspaces_api.list_workspaces()
    for workspace in workspaces:
        menu.success_message("Clearing Workspace: " + workspace["name"])
        splits_api.delete_all_splits(workspace["id"])
        segments_api.delete_all_segments(workspace["id"])

        traffic_types = traffic_types_api.list_traffic_types(workspace["id"])
        # Internal again
        for traffic_type in traffic_types:
            if traffic_type['name'] != 'user':
                traffictypes_internal.delete_traffic_type(user_session, traffic_type['id'])

    # Delete excess api tokens
    menu.success_message("Managing API Tokens")
    sdk_token = login_internal.sdk_token(user_session, org_id)
    js_token = login_internal.sdk_token(user_session, org_id, scope="SHARED")
    login_internal.delete_api_tokens(user_session, org_id, exclude_list=[sdk_token,js_token])

    # Return scope to base_user
    user.set_user(base_user)

    menu.success_message("Organization created")

    return result

def create_org_workshop_exp():
    menu.success_message("Creating Experimentation Workshop Organization")
    session = admin_session()
    response = session.post(f'https://app.split.io/internal/api/splitAdmin/organization?email={admin_user()}', headers={'Split-CSRF': session.cookies['split-csrf']})

    result = response.json()
    org_id = result['organizationId']
    user_id = result['userId']

    menu.success_message("Logging in as User")
    user_session = login_internal.login(result['userEmail'],result['userPassword'])

    # Internal Actions
    menu.success_message("Modifying Settings")
    enable_recalculations(org_id)
    disable_mcc(user_session, org_id)
    menu.success_message("Deleting Metrics & Event Types")
    metrics_internal.delete_metrics(user_session, org_id)
    eventtypes_internal.delete_all_event_types(user_session, org_id)
    menu.success_message("Creating Admin Token")
    admin_token = login_internal.create_admin_token(user_session, org_id)

    # Shift Scope for External API actions
    base_user = user.get_user()
    org_user = user.User(admin_token, "", "", "", "", "")
    user.set_user(org_user)

    # Clear Workspace
    workspace = workspaces_api.get_workspace("Default")
    menu.success_message("Clearing Workspace: " + workspace["name"])
    splits_api.delete_all_splits(workspace["id"])
    segments_api.delete_all_segments(workspace["id"])

    traffic_types = traffic_types_api.list_traffic_types(workspace["id"])
    # Internal again
    for traffic_type in traffic_types:
        if traffic_type['name'] != 'user':
            traffictypes_internal.delete_traffic_type(user_session, traffic_type['id'])
    
    # Create and ramp onboarding
    menu.success_message("Creating Feature")
    split_name = "onboarding"
    workspace_id = workspace["id"]
    split_selectors.create_split_operator(workspace_id, "user", split_name)
    definition_selectors.ramp_split_operator(workspace_id, "Prod-Default", split_name, ramp_percent=50)
    
    # Run Experiment
    menu.success_message("Running Experiment")
    sdk_token = login_internal.sdk_token(user_session, org_id)
    workshop_experiment.run_experiment(sdk_token, split_name)

    # Create metrics
    menu.success_message("Creating Metrics")
    traffic_type = traffic_types_api.get_traffic_type(workspace_id, "user")
    # metrics_internal.create_metric(user_session, user_id, org_id, workspace_id, traffic_type["id"], "Onboarding Completion Rate", "onboarding_completed", "RATE")
    # metrics_internal.create_metric(user_session, user_id, org_id, workspace_id, traffic_type["id"], "Onboarding Completion Time", "onboarding_completed", "AVERAGE", is_positive=False)
    # metrics_internal.create_metric(user_session, user_id, org_id, workspace_id, traffic_type["id"], "Average Onboarding Survey Score", "new_user_survey", "AVERAGE", property_value="survey_score")
    # metrics_internal.create_metric(user_session, user_id, org_id, workspace_id, traffic_type["id"], "Onboarding Survey Completion Rate", "new_user_survey", "RATE", filter_event_type="onboarding_completed", filter_aggregation="RATE")
    # metrics_internal.create_metric(user_session, user_id, org_id, workspace_id, traffic_type["id"], "Onboarding Progression - Plan", "onboarding_completed", "RATE", filter_event_type="onboarding_progress", filter_aggregation="RATE", filter_property_filters=[{"property":"stage","operator":"STRING_IN_LIST","inverted":False,"stringInListOperand":["plan"]}])
    # metrics_internal.create_metric(user_session, user_id, org_id, workspace_id, traffic_type["id"], "Reports Run", "report", "COUNT")
    # metrics_internal.create_metric(user_session, user_id, org_id, workspace_id, traffic_type["id"], "Total Booking Revenue", "booking", "TOTAL")
    # metrics_internal.create_metric(user_session, user_id, org_id, workspace_id, traffic_type["id"], "Return Rate - 7 day", "session_start", "RATE", base_property_filters=[{"property":"user_age","operator":"GREATER_THAN","secondOperand":"604800000","inverted":False}])
    # metrics_internal.create_metric(user_session, user_id, org_id, workspace_id, traffic_type["id"], "Exceptions", "exception", "COUNT", is_positive=False)
    # metrics_internal.create_metric(user_session, user_id, org_id, workspace_id, traffic_type["id"], "Exceptions - Desktop", "exception", "COUNT", base_property_filters=[{"property":"platform","operator":"STRING_IN_LIST","inverted":False,"stringInListOperand":["desktop"]}], is_positive=False)
    
    # definitions_internal.force_calculation(user_session, org_id, workspace_id, "Prod-Default", split_name)
    
    # Return scope to base_user
    user.set_user(base_user)

    menu.success_message("Organization created: " + result['userEmail'])

    return result

def list_demo_orgs():
    session = admin_session()
    response = session.get(demo_email_url(), headers={'Split-CSRF': session.cookies['split-csrf']})
    try:
        return response.json()
    except:
        return []

def get_demo_org(email):
    orgs = list_demo_orgs()
    orgs = list(filter(lambda x: x['userEmail'] == email, orgs))
    if len(orgs) == 0:
        return None
    else:
        return orgs[0]

def delete_demo_org(org_id):
    session = admin_session()
    session.delete(demo_org_url(org_id), headers={'Split-CSRF': session.cookies['split-csrf']})

def delete_all_demo_orgs():
    orgs = list_demo_orgs()
    for org in orgs:
        delete_demo_org(org['organizationId'])

def enable_recalculations(org_id):
    session = admin_session()
    url = f"https://app.split.io/internal/api/plans/organization/{org_id}/limits"
    data = [
      {
        "orgId": org_id,
        "limitValue": 1,
        "limitKey": "metricsCalculation",
        "type": "SERVICE",
        "hidden": True
      },
      {
        "orgId": org_id,
        "limitValue": 100,
        "limitKey": "metrics",
        "type": "SERVICE",
        "hidden": False
      }
    ]
    session.put(url, json=data, headers={'Split-CSRF': session.cookies['split-csrf']})

def disable_mcc(session, org_id):
    data = {
      "organizationId": org_id,
      "typeOneThreshold": 0.05,
      "typeTwoThreshold": 0.2,
      "reviewPeriod": 0, # Set review period to 1 day
      "monitoringWindow": 86400000,
      "multipleComparisonCorrection": "NONE", # Disable MCC
      "monitorSignificanceThreshold": 0.05,
      "minimumSampleSize": 355
    }
    session.post(f'https://app.split.io/internal/api/organization/{org_id}/results/settings', json=data, headers={'Split-CSRF': session.cookies['split-csrf']})

def create_org():
    session = admin_session()
    response = session.post(f'https://app.split.io/internal/api/splitAdmin/organization?email={admin_user()}', headers={'Split-CSRF': session.cookies['split-csrf']})
    return response.json()

def reset_metrics(user_session, org_id):
    menu.success_message("Modifying Settings")
    enable_recalculations(org_id)
    disable_mcc(user_session, org_id)
    menu.success_message("Deleting Metrics & Event Types")
    metrics_internal.delete_metrics(user_session, org_id)
    eventtypes_internal.delete_all_event_types(user_session, org_id)

def connect_admin(user_session, org_id):
    # Internal Actions
    menu.success_message("Creating Admin Token")
    admin_token = login_internal.create_admin_token(user_session, org_id)

    # Shift Scope for External API actions
    previous_user = user.get_user()
    org_user = user.User(admin_token, "", "", "", "", "")
    user.set_user(org_user)

    return previous_user

def reset_workspace(user_session, workspace):
    # Clear Workspace
    menu.success_message("Clearing Workspace: " + workspace["name"])
    splits_api.delete_all_splits(workspace["id"])
    segments_api.delete_all_segments(workspace["id"])

    traffic_types = traffic_types_api.list_traffic_types(workspace["id"])
    # Internal again
    for traffic_type in traffic_types:
        if traffic_type['name'] != 'user':
            traffictypes_internal.delete_traffic_type(user_session, traffic_type['id'])

def create_org_onboarding():
    menu.success_message("Creating Onboarding Organization")
    org = create_org()
    org_id = org['organizationId']
    user_id = org['userId']

    menu.success_message("Logging in as User")
    user_session = login_internal.login(org['userEmail'],org['userPassword'])

    reset_metrics(user_session, org_id)
    previous_user = connect_admin(user_session, org_id)

    workspace = workspaces_api.get_workspace("Default")
    reset_workspace(user_session, workspace)

    sdk_token = login_internal.sdk_token(user_session, org_id)
    onboarding_1(user_session, user_id, org_id, sdk_token, workspace)
    onboarding_2(user_session, user_id, org_id, sdk_token, workspace)

    # Return scope to base_user
    user.set_user(previous_user)

    menu.success_message("Organization created: " + org['userEmail'])


def update_org():
    user_email = "workshop+demoorg-20210409-aXPWt@split.io"
    password = "Test_1234"

    result = get_demo_org(user_email)
    
    org_id = result['organizationId']
    user_id = result['userId']

    menu.success_message("Logging in as User")
    user_session = login_internal.login(user_email,password)

    reset_metrics(user_session, org_id)
    previous_user = connect_admin(user_session, org_id)

    workspace = workspaces_api.get_workspace("Default")
    reset_workspace(user_session, workspace)

    sdk_token = login_internal.sdk_token(user_session, org_id)
    onboarding_1(user_session, user_id, org_id, sdk_token, workspace)
    onboarding_2(user_session, user_id, org_id, sdk_token, workspace)

    # Return scope to base_user
    user.set_user(previous_user)

    menu.success_message("Updated")

def onboarding_1(user_session, user_id, org_id, sdk_token, workspace):
    menu.success_message("Creating Onboarding 1")

    # Create Dedicated Traffic Type
    traffic_type_name = "user_1"
    traffictypes_internal.create_traffic_type(user_session, org_id, workspace["id"], traffic_type_name)

    # Create and ramp onboarding
    split_name = "sign_up_button"
    split_selectors.create_split_operator(workspace["id"], traffic_type_name, split_name)
    definition_selectors.ramp_split_operator(workspace["id"], "Prod-Default", split_name, ramp_percent=50)

    # Run Experiment
    menu.success_message("Running Experiment")
    experiment = Experiment(sdk_token, split_name, traffic_type=traffic_type_name)
    experiment.register("sign_up").probability(.1834,1,.22)
    experiment.run(5000)

    # Create metrics
    menu.success_message("Creating Metrics")
    traffic_type = traffic_types_api.get_traffic_type(workspace["id"], traffic_type_name)
    metrics_internal.create_metric(user_session, user_id, org_id, workspace["id"], traffic_type["id"], "Sign Up Rate", "sign_up", "RATE")

def onboarding_2(user_session, user_id, org_id, sdk_token, workspace):
    menu.success_message("Creating Onboarding 2")

    # Create Dedicated Traffic Type
    traffic_type_name = "user_2"
    traffictypes_internal.create_traffic_type(user_session, org_id, workspace["id"], traffic_type_name)

    # Create and ramp onboarding
    split_name = "metrics_reference"
    split_selectors.create_split_operator(workspace["id"], traffic_type_name, split_name)
    definition_selectors.ramp_split_operator(workspace["id"], "Prod-Default", split_name, ramp_percent=25)

    # Run Experiment
    menu.success_message("Running Experiment")
    experiment = Experiment(sdk_token, split_name, traffic_type=traffic_type_name)
    experiment.register("click", properties={ "element": "#btn-create_metric" }).count(delta=.04023,p_value=.5472,mean=8)
    experiment.register("session.ping", properties={ "url": "https://www.split.io/guides/metrics-reference/active-users/" }).total(.32592,0.163409,85453)
    experiment.register("page_load").average(.0443213,0.915853,187.324)
    experiment.run(2000)

    # Create metrics
    menu.success_message("Creating Metrics")
    traffic_type = traffic_types_api.get_traffic_type(workspace["id"], traffic_type_name)
    base_filter = [{ "property": "element", "operator": "STRING_EQUAL", "secondOperand": "#btn-create_metric", "inverted": False,"numberRangeOperand": None,"stringInListOperand": None }]
    metrics_internal.create_metric(user_session, user_id, org_id, workspace["id"], traffic_type["id"], "Metric Creation", "click", "COUNT", base_property_filters=base_filter)
    
    base_filter = [{ "property": "url", "operator": "STRING_EQUAL", "secondOperand": ".*/guides/metrics-reference/.*", "inverted": False,"numberRangeOperand": None,"stringInListOperand": None }]
    metrics_internal.create_metric(user_session, user_id, org_id, workspace["id"], traffic_type["id"], "Time in Metric Reference", "session.ping", "TOTAL", base_property_filters=base_filter)
    metrics_internal.create_metric(user_session, user_id, org_id, workspace["id"], traffic_type["id"], "Average Page Load Time", "page_load", "AVERAGE")
