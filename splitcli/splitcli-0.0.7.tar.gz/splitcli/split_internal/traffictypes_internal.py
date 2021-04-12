
def delete_traffic_type(session, traffic_type_id):
    url = f"https://app.split.io/internal/api/trafficTypes/{traffic_type_id}"
    session.delete(url, headers={'Split-CSRF': session.cookies['split-csrf']})

def create_traffic_type(session, org_id, workspace_id, name):
    url = f"https://app.split.io/internal/api/trafficTypes"
    data = {"name":name,"orgId":org_id,"workspaceIds":[workspace_id]}
    session.post(url,  json=data, headers={'Split-CSRF': session.cookies['split-csrf']})