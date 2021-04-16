import json, requests

from django.conf import settings

from djoptimizely.models import OptimizelyDataFile


def _get_datafile_object(optimizely_env):
    o, _ = OptimizelyDataFile.objects.get_or_create(
        environment=optimizely_env
    )
    return o

def _get_datafile_object_for_current_env():
    return _get_datafile_object(settings.OPTIMIZELY_ENVIRONMENT)

def _update_datafile_object(o, url):
    response = requests.get(url)
    if response:
        json = response.json()
        o.project_id = json['projectId']
        o.current_revision = json['revision']
        o.json = json
        o.save()    

def _update_datafile_for_primary_env(env, data):
    url = data.get('cdn_url')
    if env and url:
        o = _get_datafile_object(env)
        _update_datafile_object(o, url)

def get_datafile():
    o = _get_datafile_object_for_current_env()
    if o.json:
        return json.dumps(o.json)
    return None

def update_datafile_for_current_env():
    if settings.OPTIMIZELY_DATAFILE_URL:
        o = _get_datafile_object_for_current_env()
        _update_datafile_object(o, settings.OPTIMIZELY_DATAFILE_URL)

def update_datafile_with_payload(payload):
    data = payload.get('data')
    if data:
        env = data.get('environment')
        if env == settings.OPTIMIZELY_ENVIRONMENT:
            _update_datafile_for_primary_env(env, data)
        else:
            update_datafile_for_current_env()
