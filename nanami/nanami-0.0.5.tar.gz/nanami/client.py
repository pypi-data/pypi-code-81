
import sys
import json
import atexit
import logging
from io import StringIO

from nanami.utils import logger, post, QUEUE_API_URL, check_auth

log_stream = StringIO()
error_logger = logging.getLogger()
logging.basicConfig(stream=log_stream)

def at_exit_func():
    error_message = log_stream.getvalue().strip()
    if len(error_message) > 0:
        project = set_status(status='failure', error_message=error_message)
        if project:
            post(f"{project['localhost']}/message", data={
                'project': project,
                'status': 'failure',
            })
            post(f"{project['localhost']}/running", data={
                'project': project,
            })


def exception_hook(exc_type, exc_value, exc_traceback):
    error_logger.error(
        "Uncaught exception",
        exc_info=(exc_type, exc_value, exc_traceback)
    )

sys.excepthook = exception_hook
atexit.register(at_exit_func)

def read_project_info():
    try:
        with open('/workspace/nanami.json') as json_file:
            project_info = json.loads(json_file.read())
            return project_info
    except:
        raise FileNotFoundError("nanami.json is not found.")

def set_status(status, error_message=None):
    project = read_project_info()
    apikey = project['apikey']

    result = post(f"{QUEUE_API_URL}/status", data={
        'apikey': apikey,
        'queue_info': project['queue_info'],
        'status': status,
        'error_message': error_message
    })
    if result:
        if not result['success']:
            print(f'Failed to set {status}.')
        else:
            if result['dequeue']:
                logger.info("Nanami will dequeue queue_id.")
                return project
    else:
        print(f'[API Error] : {QUEUE_API_URL}/status')

    return None

def start():
    logger.info('[Nanami Start!]')
    project = set_status(status='running')
    if project:
        post(f"{project['localhost']}/message", data={
            'project': project,
            'status': 'running',
        })

def end():
    logger.info('[Nanami End!]')
    project = set_status(status='success')
    if project:
        post(f"{project['localhost']}/message", data={
            'project': project,
            'status': 'success',
        })
        post(f"{project['localhost']}/running", data={
            'project': project,
        })