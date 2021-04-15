import logging
import time
import subprocess
import json
import datetime
from socket import gethostname, gethostbyname
import os
import requests

from biolib.compute_node.worker_thread import WorkerThread
from biolib.compute_node import utils
from biolib.compute_node.webserver import webserver_config

biolib_logger = logging.getLogger('biolib')


def get_compute_state(unassigned_compute_processes):
    if len(unassigned_compute_processes) == 0:
        start_compute_process(unassigned_compute_processes)

    return unassigned_compute_processes.pop()


def start_compute_process(unassigned_compute_processes, eif_path=None):
    compute_state = {
        'status': {
            'status_updates': [
                {
                    'progress':  10,
                    'log_message': 'Initializing'
                }
            ],
        },
        'result': None,
        'attestation_document': b'',
        'received_messages_queue': None,
        'messages_to_send_queue': None,
        'worker_process': None
    }
    WorkerThread(compute_state, eif_path).start()
    while True:
        if compute_state['attestation_document']:
            break
        time.sleep(1)

    if eif_path:
        start_vsock_proxies(use_enclave_hosts=True)
        report_availability()

    unassigned_compute_processes.append(compute_state)


def start_vsock_proxies(remote_hosts=None, use_enclave_hosts=False):
    if use_enclave_hosts:
        remote_hosts = utils.enclave_remote_hosts
        baseport = 8000
    else:
        # Enclave remote hosts are already running, so we need to use next set of available ports
        baseport = 8000 + len(utils.enclave_remote_hosts)

    vsock_proxy_binary = webserver_config.VSOCK_PROXY_PATH
    log_file = open(webserver_config.LOG_FILE_PATH, 'a')
    for host_id, host in enumerate(remote_hosts):
        biolib_logger.debug(f"Opening vsock-proxy on port {baseport + host_id} for hostname {host}")
        subprocess.Popen([vsock_proxy_binary, str(baseport + host_id), host, '443'], stdout=log_file,
                         stderr=log_file)


def validate_saved_job(saved_job):
    if 'app_version' not in saved_job['job']:
        return False

    if 'modules' not in saved_job['job']['app_version']:
        return False

    if 'access_token' not in saved_job:
        return False

    if 'module_name' not in saved_job:
        return False

    return True


def report_availability():
    dev_mode = os.getenv('COMPUTE_NODE_ENV') == 'dev'
    if not dev_mode:
        try:
            if biolib_logger.isEnabledFor(logging.DEBUG):
                bash_rc_content = open('/home/ec2-user/.bashrc', 'r').read()
                biolib_logger.debug(f'.bashrc at the start of Compute Node: {bash_rc_content}')

            node_public_id = os.getenv('BIOLIB_COMPUTE_NODE_PUBLIC_ID')
            auth_token = os.getenv('BIOLIB_COMPUTE_NODE_AUTH_TOKEN')
            biolib_host = os.getenv('BIOLIB_HOST')
            ip_address = gethostbyname(gethostname())
            data = {'public_id':node_public_id, 'auth_token':auth_token, 'ip_address':ip_address}
            biolib_logger.debug(f'Registering with {data} to host {biolib_host}')
            biolib_logger.debug(f'Registering at {datetime.datetime.now()}')
            req = requests.post(f'{biolib_host}/api/jobs/report_available/', json=json.dumps(data))
            if req.status_code != 200:
                raise Exception("Non 200 error code")

        except Exception as exception:  # pylint: disable=broad-except
            biolib_logger.error(f'Could not self register because of: {exception}')
            biolib_logger.debug("Self destructing")
            if not dev_mode:
                subprocess.run(['sudo', 'shutdown', 'now'], check=False)
