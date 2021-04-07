import json


def build_list_from_request(request, field, object_type):
    jrequest = request.json()
    if field not in jrequest:
        raise ValueError("No field {} in {}".format(field, json.dumps(jrequest)))
    json_repos = jrequest[field]
    repos = []
    for json_repo in json_repos:
        repos.append(object_type(json_repo))
    return repos
