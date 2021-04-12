
def list_event_types(session, org_id):
    url = f"https://app.split.io/internal/api/organization/{org_id}/eventTypes/v2"
    response = session.get(url, headers={'Split-CSRF': session.cookies['split-csrf']})
    result = response.json()
    return result['objects']

def delete_all_event_types(session, org_id):
    event_types = list_event_types(session, org_id)
    for event_type in event_types:
        delete_event_type(session, org_id, event_type['eventTypeId'])

def delete_event_type(session, org_id, event_type_id):
    url = f"https://app.split.io/internal/api/organization/{org_id}/eventTypes/{event_type_id}"
    session.delete(url, headers={'Split-CSRF': session.cookies['split-csrf']})