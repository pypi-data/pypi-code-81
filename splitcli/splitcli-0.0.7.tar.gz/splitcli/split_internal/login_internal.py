import requests

def list_api_tokens(session, org_id):
    url = f"https://app.split.io/internal/api/apiTokens/organization/{org_id}"
    response = session.get(url, headers={'Split-CSRF': session.cookies['split-csrf']})
    return response.json()

def get_api_token(session, org_id, environment_name, scope):
    api_tokens = list_api_tokens(session, org_id)['data']
    api_token = list(filter(lambda x: x['environmentURNs'][0]['name'] == environment_name and x['scope'] == scope, api_tokens))[0]
    return api_token['id']

def delete_api_token(session, api_token):
    url = f"https://app.split.io/internal/api/apiTokens/{api_token}"
    session.delete(url, headers={'Split-CSRF': session.cookies['split-csrf']})

def delete_api_tokens(session, org_id, exclude_list=[]):
    api_tokens = list_api_tokens(session, org_id)['data']
    for api_token in api_tokens:
        if api_token["id"] not in exclude_list:
            delete_api_token(session, api_token["id"])

def sdk_token(session, org_id, environment_name="Prod-Default", scope="SDK"):
	return get_api_token(session, org_id, environment_name, scope)

def admin_token(session, org_id):
    api_tokens = list_api_tokens(session, org_id)['data']
    api_token = list(filter(lambda x: x['scope'] == 'ADMIN', api_tokens))[0]
    return api_token['id']

def create_admin_token(session, org_id):
    url = f"https://app.split.io/internal/api/apiTokens"
    content = {"orgId":org_id,"name":"Split CLI Internal","scope":"ADMIN","workspaceIds":[],"environmentIds":[]}
    response = session.post(url, json=content, headers={'Split-CSRF': session.cookies['split-csrf']})
    return response.json()["id"]

def login(user, password):
    split_login = 'https://app.split.io/login'
    data = { 'email': user, 'password': password }
    session = requests.Session()
    session.post(split_login, data)
    return session