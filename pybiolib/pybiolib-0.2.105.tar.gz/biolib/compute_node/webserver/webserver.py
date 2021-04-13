import json
import logging
import os
import time
import base64
import subprocess
from typing import Dict
from flask import Flask, request, Response, jsonify
from flask_cors import CORS
from biolib.biolib_binary_format import SavedJob
from biolib.compute_node.webserver import webserver_utils
from biolib.compute_node.webserver import webserver_config
from biolib.compute_node.webserver.gunicorn_flask_application import GunicornFlaskApplication

# Disable warning about using the "global" statement for the rest of this file
# pylint: disable=global-statement

biolib_logger = logging.getLogger('biolib')

# Global constants
DEV_MODE = os.getenv('COMPUTE_NODE_ENV') == 'dev'
EIF_PATH = ''
BIOLIB_HOST = ''
JOB_ID_TO_COMPUTE_STATE_DICT: Dict = {}
UNASSIGNED_COMPUTE_PROCESSES = []

app = Flask(__name__)
CORS(app)


@app.before_first_request
def start_running_job_shutdown_timer():
    if EIF_PATH and not DEV_MODE:
        # Cancel the long general timer and replace with shorter shutdown timer
        subprocess.run(['sudo', 'shutdown', '-c'], check=False)
        subprocess.Popen(['sudo', 'shutdown', f'+{webserver_config.COMPUTE_NODE_RUNNING_JOB_SHUTDOWN_TIME_MINUTES}'])


def shutdown_after_response():
    biolib_logger.debug("Shutting down...")
    if not DEV_MODE:
        subprocess.run(['sudo', 'shutdown', 'now'], check=False)


@app.route('/hello/')
def hello():
    return 'Hello'


@app.route('/v1/job/', methods=['POST'])
def start_job():
    global JOB_ID_TO_COMPUTE_STATE_DICT, BIOLIB_HOST
    saved_job = json.loads(request.data.decode())

    if not webserver_utils.validate_saved_job(saved_job):
        return jsonify({'job': 'Invalid job'}), 400

    job_id = saved_job['job']['public_id']
    saved_job['BIOLIB_HOST'] = BIOLIB_HOST

    compute_state = webserver_utils.get_compute_state(UNASSIGNED_COMPUTE_PROCESSES)
    JOB_ID_TO_COMPUTE_STATE_DICT[job_id] = compute_state

    if EIF_PATH:
        job_remote_hosts = [host['hostname'] for host in saved_job['job']['app_version']['remote_hosts']]
        webserver_utils.start_vsock_proxies(remote_hosts=job_remote_hosts)
        saved_job['enclave_ecr_token'] = os.getenv('ENCLAVE_ECR_TOKEN', None)

    saved_job_bbf_package = SavedJob().serialize(json.dumps(saved_job))
    send_package_to_compute_process(job_id, saved_job_bbf_package)

    if EIF_PATH:
        return Response(base64.b64encode(compute_state['attestation_document']), status=201)
    else:
        return '', 201


@app.route('/v1/job/<job_id>/start/', methods=['POST'])
def start_compute(job_id):
    module_input_package = request.data
    send_package_to_compute_process(job_id, module_input_package)
    return '', 201


@app.route('/v1/job/<job_id>/status/')
def status(job_id):
    # TODO Implement auth token
    global JOB_ID_TO_COMPUTE_STATE_DICT
    current_status = JOB_ID_TO_COMPUTE_STATE_DICT[job_id]['status'].copy()

    if current_status['status_updates']:
        JOB_ID_TO_COMPUTE_STATE_DICT[job_id]['status']['status_updates'] = []

    # Check if any error occured
    if 'error_code' in current_status:
        if EIF_PATH:
            error_response = app.response_class(response=json.dumps(current_status),
                                                status=201,
                                                mimetype='application/json')
            error_response.call_on_close(shutdown_after_response)
            return error_response
        else:
            # Remove failed job
            JOB_ID_TO_COMPUTE_STATE_DICT.pop(job_id)

    return jsonify(current_status)


@app.route('/v1/job/<job_id>/result/')
def result(job_id):
    global JOB_ID_TO_COMPUTE_STATE_DICT
    if JOB_ID_TO_COMPUTE_STATE_DICT[job_id]['result']:
        result_data = JOB_ID_TO_COMPUTE_STATE_DICT[job_id]['result']
        result_response = Response(result_data)

        if EIF_PATH:
            result_response.call_on_close(shutdown_after_response)
        else:
            # Remove finished job
            JOB_ID_TO_COMPUTE_STATE_DICT.pop(job_id)

        return result_response
    else:
        return '', 404


def send_package_to_compute_process(job_id, package_bytes):
    global JOB_ID_TO_COMPUTE_STATE_DICT
    message_queue = JOB_ID_TO_COMPUTE_STATE_DICT[job_id]['messages_to_send_queue']
    message_queue.put(package_bytes)


def start_webserver(port, host, specified_biolib_host, specified_eif_path=None):
    global EIF_PATH, BIOLIB_HOST, UNASSIGNED_COMPUTE_PROCESSES, JOB_ID_TO_COMPUTE_STATE_DICT
    BIOLIB_HOST = specified_biolib_host

    if specified_eif_path:
        EIF_PATH = specified_eif_path

    if EIF_PATH and not DEV_MODE:
        subprocess.Popen(['sudo', 'shutdown', f'+{webserver_config.COMPUTE_NODE_AUTO_SHUTDOWN_TIME_MINUTES}'])

    def worker_exit(server, worker):  # pylint: disable=unused-argument
        active_compute_states = list(JOB_ID_TO_COMPUTE_STATE_DICT.values()) + UNASSIGNED_COMPUTE_PROCESSES
        biolib_logger.info(f"Sending kill signal to {len(active_compute_states)} compute processes")
        if active_compute_states:
            for compute_state in active_compute_states:
                if compute_state['worker_thread']:
                    compute_state['worker_thread'].terminate()
            time.sleep(4)
        return

    def post_fork(server, worker):  # pylint: disable=unused-argument
        global UNASSIGNED_COMPUTE_PROCESSES, EIF_PATH
        biolib_logger.info("Started Webserver")
        webserver_utils.start_compute_process(UNASSIGNED_COMPUTE_PROCESSES, EIF_PATH)

    options = {
        'bind': f'{host}:{port}',
        'workers': 1,
        'post_fork': post_fork,
        'worker_exit': worker_exit,
        'timeout': webserver_config.GUNICORN_REQUEST_TIMEOUT,
        'graceful_timeout': 4
    }

    # Log to file when running on EC2
    if EIF_PATH:
        options.update({
            'errorlog': webserver_config.LOG_FILE_PATH,
            'capture_output': True
        })

    GunicornFlaskApplication(app, options).run()
