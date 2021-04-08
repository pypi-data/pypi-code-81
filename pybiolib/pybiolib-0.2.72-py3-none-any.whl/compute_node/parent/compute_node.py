# pylint: skip-file TODO: Remove this line
from flask import Flask, request, Response
from flask.json import jsonify
from flask_cors import CORS, cross_origin
import requests
import threading
import json
import os
import logging
import datetime
from Crypto.PublicKey import RSA
from Crypto.IO import PEM
import gunicorn.app.base
# Needed to call gunicorn from Python (Results in import errors if removed)
from gunicorn import glogging
from gunicorn.workers import sync

import subprocess
from socket import gethostname, gethostbyname
from biolib.compute_node.parent.parent_client import run_client
from biolib.compute_node.parent import parent_config

app = Flask(__name__)
CORS(app)
biolib_logger = logging.getLogger('biolib')

# Global variables
locks = {lock_name: threading.Lock() for lock_name in ['attestation', 'cloud_job_state', 'input_data', 'result']}
cloud_job = {
    'status_and_progress': {'message': 'Starting', 'progress': 0},
    'biolib_host': '',
    'encrypted_result': '',
    'encrypted_input_data': '',
    'error': '',
    'access_token': '',
    'eif_path': '',
    'rsa_key_hex': '',
    'socket_connection': None,
    'input_keys': {},
    'result_keys': {},
    'cloud_job_state': {},
    'compute_listener_started': False,
    'attestation_document_b64': ''
}

dev_mode = True if os.environ.get('COMPUTE_NODE_ENV', '') == 'dev' else False

if dev_mode:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.ERROR)


def shutdown_after_response():
    if not dev_mode:
        biolib_logger.debug("Shutting down...")
        subprocess.run(['sudo', 'shutdown', 'now'])


@app.before_first_request
def initialize_parent_client():
    # Immediately acquire all locks to make sure blocking works correctly down the line
    biolib_logger.debug("Started Compute Node and locking locks")
    for lock in locks.values():
        lock.acquire()

    threading.Thread(target=run_client, args=(locks, cloud_job)).start()


@app.route('/')
def hello():
    return 'Hello World!'


@app.route('/save_cloud_job/', methods=['POST'])
def save_cloud_job():
    global cloud_job
    if cloud_job['encrypted_result'] or cloud_job['result_keys'] or cloud_job['error']:
        cloud_job.update({
            'encrypted_result': '',
            'result_keys': '',
            'error': ''
        })

    cloud_job['cloud_job_state'] = request.get_json()
    cloud_job['access_token'] = cloud_job['cloud_job_state']['access_token']
    locks['cloud_job_state'].release()

    if cloud_job['eif_path']:
        # Start self destruct timer
        if not dev_mode:
            subprocess.Popen(['sudo', 'shutdown', f'+{parent_config.COMPUTE_NODE_RUNNING_JOB_SHUTDOWN_TIME_MINUTES}'])

    else:
        rsa_key = RSA.generate(2048)
        cloud_job['rsa_key_hex'] = rsa_key.export_key().hex()
        public_key = rsa_key.publickey().export_key('DER')
        return public_key.hex(), 201

    return "", 201


@app.route('/get_attestation_document/')
def get_attestation_document():
    global cloud_job
    return jsonify({'attestation_document_base64': cloud_job['attestation_document_b64']}), 201


@app.route('/start_cloud_job/', methods=['POST'])
def start_cloud_job():
    global cloud_job
    cloud_job['encrypted_input_data'] = request.data
    cloud_job['input_keys'] = json.loads(request.headers['Keys'])
    locks['input_data'].release()
    locks['cloud_job_state'].acquire()
    return "", 201


@app.route('/status/')
def status():
    global cloud_job
    if cloud_job['error']:
        error_response = app.response_class(response=cloud_job['error'],
                                status=500,
                                mimetype='application/json')
        if cloud_job['eif_path']:
            error_response.call_on_close(shutdown_after_response)
        else:
            reset_cloud_job_state(cloud_job, locks)
        return error_response

    return jsonify(cloud_job['status_and_progress']), 200


@app.route('/result/')
@cross_origin(expose_headers=['Keys'])
def result():
    global cloud_job
    response = Response(cloud_job['encrypted_result'])
    response.headers['Keys'] = json.dumps(cloud_job['result_keys'])
    if cloud_job['eif_path']:
        response.call_on_close(shutdown_after_response)
    else:
        reset_cloud_job_state(cloud_job, locks)
    return response


def reset_cloud_job_state(cloud_job, locks):
    cloud_job.update({
        'status_and_progress': {'message': 'Starting', 'progress': 0},
        'encrypted_input_data': '',
        'rsa_key_hex': '',
        'input_keys': {},
        'cloud_job_state': {},
    })

    for lock in locks.values():
        if not lock.locked():
            lock.acquire()


class StandaloneApplication(gunicorn.app.base.BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(StandaloneApplication, self).__init__()

    # Needed to load the options
    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    # Needed to overload base class
    def load(self):
        return self.application


def start_flask_compute_node(port, host, biolib_host, eif_path=None):
    global cloud_job

    # Report availability and set general shutdown timer
    if not dev_mode and eif_path:
        subprocess.Popen(["sudo", "shutdown", f"+{parent_config.COMPUTE_NODE_SHUTDOWN_TIME_MINUTES}"])

        try:
            biolib_logger.debug(f'.bashrc at the start of Compute Node: {open("/home/ec2-user/.bashrc", "r").read()}')
            node_public_id = os.getenv('BIOLIB_COMPUTE_NODE_PUBLIC_ID')
            auth_token = os.getenv('BIOLIB_COMPUTE_NODE_AUTH_TOKEN')
            biolib_host = os.getenv('BIOLIB_HOST')
            ip_address = gethostbyname(gethostname())
            data = {'public_id':node_public_id, 'auth_token':auth_token, 'ip_address':ip_address}
            biolib_logger.debug(f'Registering with {data} to host {biolib_host}')
            biolib_logger.debug(f'Registering at {datetime.datetime.now()}')
            r = requests.post(f'https://{biolib_host}/api/jobs/report_available/', json=json.dumps(data))
            if r.status_code != 200:
                raise Exception("Non 200 error code")

        except Exception as e:
            biolib_logger.error(f'Could not self register because of: {e}')
            if not dev_mode:
                subprocess.run(['sudo', 'shutdown', 'now'])
            biolib_logger.debug("Self destructing")


    options = {
        'bind': f'{host}:{port}',
        'workers': 1,
    }

    if eif_path:
        cloud_job['eif_path'] = eif_path

    cloud_job['biolib_host'] = biolib_host

    StandaloneApplication(app, options).run()
