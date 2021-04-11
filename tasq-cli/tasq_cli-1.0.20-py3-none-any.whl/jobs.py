import requests
import json

from tasq_cli.settings import SERVER, TOKEN
from tasq_cli import settings
from tasq_cli.server import make_request

logger = None

def run_job(args):
    global logger
    logger = settings.get_logger()
    url = f'/jobs'
    tag = args.tag
    headers = {'content-type': 'application/vnd.api+json', 'accept': 'application/vnd.api+json'}

    data = {'data': {'type': 'jobs',
              'attributes': {'name': '',
                             'includeModel': False,
                             'tags': [tag],
                             'excludeTags': [],
                             'maxResources': None,
                             'forQualification': False,
                             'projectId': args.project_id,
                             'projectResourceIds': []}}}
    r = make_request(url, headers=headers, json=data)
    data = r.json()['data']
    del data['relationships']
    print(data)
    return


def list_jobs(args):
    global logger
    logger = settings.get_logger()
    url = f'/jobs/?filter[project]={args.project_id}&sort=-id&page[size]=100'
    r = make_request(url)
    data = r.json()['data']
    for j in data:
        del(j['relationships'])
    print(json.dumps(data))
    return


def export_job(args):
    global logger
    logger = settings.get_logger()
    type = 'target'
    if args.raw:
        type='raw'
    url = f'/jobs/{args.job_id}/download/?export_type={type}&all_judgements=false'
    r = make_request(url)
    data = r.json()
    print(data)
    return
