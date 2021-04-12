import json

def list_metrics(session, org_id):
    url = f"https://app.split.io/internal/api/organization/{org_id}/metrics"
    response = session.get(url, headers={'Split-CSRF': session.cookies['split-csrf']})
    return response.json()

def delete_metric(session, org_id, metric_id):
    url = f"https://app.split.io/internal/api/organization/{org_id}/metrics/{metric_id}"
    session.delete(url, headers={'Split-CSRF': session.cookies['split-csrf']})

def delete_metrics(session, org_id):
    metrics = list_metrics(session, org_id)
    for metric in metrics['data']:
        delete_metric(session, org_id, metric['id'])

def create_metric(session, user_id, org_id, workspace_id, traffic_type_id, metric_name, base_event_type, aggregation, metric_description="", metric_format="0,0.00", is_positive=True, spread="PER", filter_event_type="", filter_aggregation="", base_property_filters=[], filter_property_filters=[], property_value=None):
    metric = {
        "organizationId": org_id,
        "name":metric_name,
        "description":metric_description,
        "format":metric_format,
        "positive":is_positive,
        "baseEventTypeId":base_event_type,
        "aggregation":aggregation,
        "spread":spread,
        "trafficTypeId":traffic_type_id,
        "filterEventTypeId":filter_event_type,
        "filterAggregation":filter_aggregation,
        "tags":[],
        "workspaceIds":[workspace_id],
        "filterEventPropertyFilters":filter_property_filters,
        "baseEventPropertyFilters":base_property_filters,
        "propertyForValue":property_value,
        "type":"Metric",
        "owners":[
            {"id":user_id,"type":"User"}
        ]
    }
    change = {"orgId":org_id,
        "wsId":workspace_id,
        "objectType":"Metric",
        "operationType":"CREATE",
        "object":metric
    }
    preview_url = 'https://app.split.io/internal/api/changeRequests/preview/'
    response = session.put(preview_url, json=change, headers={'Split-CSRF': session.cookies['split-csrf']})
    if response.status_code == 200:
        change_url = 'https://app.split.io/internal/api/changeRequests/'
        response = session.post(change_url, json=response.json(), headers={'Split-CSRF': session.cookies['split-csrf']})
        return response.json()
    else:
        print(json.dumps(response.json()))
        return None
    
def set_key_metrics(session, metadata_id, metric_ids):
    url = f"https://app.split.io/internal/api/testMetadata/{metadata_id}/keyMetrics"
    response = session.post(url, json=metric_ids, headers={'Split-CSRF': session.cookies['split-csrf']})