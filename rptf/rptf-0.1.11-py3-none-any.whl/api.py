import json
import os

import requests

GITLAB_API_URL = os.environ.get('GITLAB_API_URL', 'https://gitlab.com/api/v4')


def headers():
    return {'Private-Token': os.environ['GITLAB_ACCESS_TOKEN']}


def trigger_pipeline(project_id, ref='master', variables=None):
    # prepare variables
    if variables is None:
        variables = {}
    variables_list = []
    for key in variables.keys():
        variables_list.append({'key': key, 'value': variables[key]})
    # request
    url = '%s/projects/%s/pipeline?ref=%s' % (GITLAB_API_URL, project_id, ref)
    res = requests.post(url=url, headers=headers(), json={'variables': variables_list})
    res_dict = json.loads(res.text)
    return res_dict['id'], res_dict['web_url']


def get_pipeline(project_id, pipeline_id):
    url = '%s/projects/%s/pipelines/%s' % (GITLAB_API_URL, project_id, pipeline_id)
    res = requests.get(url=url, headers=headers())
    return json.loads(res.text)


def get_jobs(project_id, pipeline_id):
    url = '%s/projects/%s/pipelines/%s/jobs' % (GITLAB_API_URL, project_id, pipeline_id)
    res = requests.get(url=url, headers=headers())
    return json.loads(res.text)
