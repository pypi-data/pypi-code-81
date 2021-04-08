# pylint: skip-file TODO: Remove this line
import sys
import socket
import json
import subprocess
import base64
import os
import threading
import io
import random
import docker
import requests
import shlex
import string
import zipfile
import logging
import tarfile
import shutil
import os
import time
import boto3
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

from biolib.compute_node.enclave.enclave_server import get_keys
from biolib.compute_node.enclave.mappings import Mappings, path_without_first_folder
from biolib.compute_node.parent import parent_config
from biolib.compute_node.enclave.biolib_binary_format import ModuleInput
from asyncio import IncompleteReadError


from time import sleep


class BiolibException(Exception):
    pass


def run_client(locks, cloud_job):
    while True:
        try:
            run_cloud_job(locks, cloud_job)

        except BiolibException as bl_error:
            if not locks['cloud_job_state'].locked():
                locks['cloud_job_state'].acquire()
            print(bl_error)
            cloud_job['error'] = json.dumps({'detail': str(bl_error)})

        except Exception as e:
            if not locks['cloud_job_state'].locked():
                locks['cloud_job_state'].acquire()
            print(e)
            log_error(e)
            cloud_job['error'] = json.dumps({'detail': "The Cloud Job was not completed. An unknown error occured"})


def run_cloud_job(locks, cloud_job):
    if not cloud_job['socket_connection']:
        if cloud_job['eif_path']:
            cloud_job['socket_connection'] = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
        else:
            cloud_job['socket_connection'] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s = cloud_job['socket_connection']

    locks['cloud_job_state'].acquire()
    log_status(message='Saving module state', progress=5, cloud_job=cloud_job)
    cloud_job_state = cloud_job['cloud_job_state']
    module = cloud_job_state['module']
    locks['cloud_job_state'].release()

    if not cloud_job['eif_path']:
        # Check if we need to call an external app before starting the compute thread
        if module['environment'] == 'biolib-app':
            caller_remote_hosts = cloud_job['cloud_job_state']['remote_hosts']
            caller_runtime_zip = cloud_job['cloud_job_state']['runtime_zip']
            job = get_job_for_external_app(module, access_token=cloud_job['access_token'], biolib_host=cloud_job['biolib_host'])
            locks['input_data'].acquire()
            log_status(message='Downloading source files', progress=10, cloud_job=cloud_job)
            runtime_zip_data, runtime_zip_size = download_runtime_zip(caller_runtime_zip)
            add_runtime_files_and_command_to_input(cloud_job, runtime_zip_data, runtime_zip_size)
            cloud_job['cloud_job_state']['module'] = job['app_version']['modules'][0]
            cloud_job['cloud_job_state']['remote_hosts'] = caller_remote_hosts
            cloud_job['cloud_job_state']['runtime_zip'] = job['app_version']['client_side_executable_zip']
            locks['input_data'].release()
            if locks['cloud_job_state'].locked():
                locks['cloud_job_state'].release()
            run_cloud_job(locks, cloud_job)
            return

        elif module['environment'] == 'biolib-custom':
            raise BiolibException('Biolib does not yet support execution of WASM outside the browser')

    log_status(message='Pulling images', progress=10, cloud_job=cloud_job)
    image_bytes, image_uri = pull_image(module['image_uri'], cloud_job)

    if not cloud_job['compute_listener_started']:
        if cloud_job['eif_path']:
            log_status(message='Starting encrypted enclave', progress=20, cloud_job=cloud_job)
            start_and_connect_to_enclave(s, cloud_job)

            log_status(message='Sending images to enclave', progress=35, cloud_job=cloud_job)
            send_image_data_to_enclave(s, image_bytes)

            log_status(message='Creating attestation document', progress=50, cloud_job=cloud_job)
            send_request(s, {'route': 'do_attestation'})
            cloud_job['attestation_document_b64'] = s.recv(parent_config.ATTESTATION_DOC_BUFFER_SIZE).decode()
            locks['attestation'].release()
            log_status(message='Attestation document ready', progress=55, cloud_job=cloud_job)

        else:
            subprocess.Popen(['biolib', 'listen'])
            sleep(2)
            retries = 0
            while s.connect_ex(('127.0.0.1', parent_config.ENCLAVE_PORT)) != 0:
                if retries > 20:
                    raise BiolibException("Could not connect to compute node")
                retries += 1
                sleep(1)

        cloud_job['compute_listener_started'] = True

    locks['input_data'].acquire()
    log_status(message='Sending the encrypted data to Enclave', progress=60, cloud_job=cloud_job)
    send_input_data_to_enclave(s, cloud_job['encrypted_input_data'], keys=cloud_job['input_keys'],
                               rsa_key_hex=cloud_job['rsa_key_hex'])
    locks['input_data'].release()

    runtime_zip = cloud_job_state.get('runtime_zip')
    encrypted_result, result_keys = run_docker_application_in_enclave(s, image_uri, module, cloud_job, runtime_zip)
    cloud_job['encrypted_result'] = encrypted_result
    cloud_job['result_keys'] = result_keys
    locks['result'].release()
    log_status(message='Result is ready', progress=100, cloud_job=cloud_job)

    # Make sure we wait for the next cloud_job
    if not locks['cloud_job_state'].locked():
        locks['cloud_job_state'].acquire()


def get_job_for_external_app(module, access_token, biolib_host):
    data = {'app_version_id': module['image_uri']}
    headers = {'Authentication': f'Bearer {access_token}'}
    r = requests.post(f'{biolib_host}/api/jobs/', json=data, headers=headers)
    if r.status_code != 201:
        raise BiolibException(f'Could not create new job for biolib-app {module["image_uri"]} on host {biolib_host}')
    return r.json()


def add_runtime_files_and_command_to_input(cloud_job, runtime_zip_data, runtime_zip_size):
    encrypted_input_data = cloud_job['encrypted_input_data']
    module = cloud_job['cloud_job_state']['module']
    aes_key_buffer, nonce = get_keys(cloud_job['input_keys'], nsm_util=None, rsa_key_hex=cloud_job['rsa_key_hex'])
    cipher = AES.new(aes_key_buffer, AES.MODE_GCM, nonce=nonce)
    serialized_input_data = cipher.decrypt(encrypted_input_data)
    module_input = ModuleInput(serialized_input_data).deserialize()

    if runtime_zip_data:
        runtime_zip = zipfile.ZipFile(io.BytesIO(runtime_zip_data))
        source_mappings = Mappings(module['source_files_mappings'], module_input['arguments'])
        for zip_file_name in runtime_zip.namelist():
            file_path = '/' + path_without_first_folder(zip_file_name)
            mapped_file_names = source_mappings.get_mappings_for_path(file_path)
            for mapped_file_name in mapped_file_names:
                file_data = runtime_zip.read(zip_file_name)
                module_input['files'].update({mapped_file_name: file_data})

    for command_part in reversed(module['command'].split()):
        module_input['arguments'].insert(0, command_part)

    serialized_input_data_with_runtime_files = ModuleInput().serialize(module_input['stdin'], module_input['arguments'], module_input['files'])
    nonce = get_random_bytes(12)
    cipher = AES.new(aes_key_buffer, AES.MODE_GCM, nonce=nonce)
    encrypted_input_data_with_runtime_files, tag = cipher.encrypt_and_digest(serialized_input_data_with_runtime_files)
    cloud_job['input_keys']['iv'] = nonce.hex()
    cloud_job['encrypted_input_data'] = encrypted_input_data_with_runtime_files


def start_and_connect_to_enclave(s, cloud_job):
    # Start the enclave
    subprocess.run(shlex.split(f"nitro-cli run-enclave --cpu-count 2 --memory 8192 --eif-path {cloud_job['eif_path']}"))

    # Get CID of running enclave from nitro cli
    log_status(message='Waiting for enclave to start', progress=25, cloud_job=cloud_job)

    enclave_cid = None
    while True:
        if isinstance(enclave_cid, str) and enclave_cid.isnumeric():
            break
        enclave_cid = subprocess.run(
            'nitro-cli describe-enclaves | jq -r ".[0].EnclaveCID"', 
            check=True, 
            stdout=subprocess.PIPE, 
            universal_newlines=True, 
            shell=True
        ).stdout.strip()
        sleep(0.1)

    # Sleep 4.5 seconds to let enclave start its socket correctly. Things break if we do not include this.
    sleep(4.5)
    log_status(message='Connecting to enclave', progress=30, cloud_job=cloud_job)
    
    # Retry until enclave is up and running
    retries = 0
    while s.connect_ex((int(enclave_cid), parent_config.ENCLAVE_PORT)) != 0:
        if retries > 20:
            raise BiolibException("Could not establish connection to enclave")
        retries += 1
        sleep(1)


def pull_image(repo_uri, cloud_job):
    try:
        docker_client = docker.from_env()
    except Exception as e:
        log_error(e)
        raise BiolibException("Failed to start docker client. Make sure docker is installed and started correctly")

    try:
        if cloud_job['eif_path']:
            # Log in to ECR
            client = boto3.client('ecr', region_name='eu-west-1')
            token = client.get_authorization_token(registryIds=[parent_config.BIOLIB_AWS_ECR_ID])
            password = base64.b64decode(token['authorizationData'][0]['authorizationToken']).decode().split(':')[-1]
            docker_client.login(username="AWS", password=password, registry=parent_config.BIOLIB_AWS_ECR_URL)
    
    except Exception as e:
        log_error(e)
        raise BiolibException("Failed to login to Biolib Container Registry")
    
    try:
        # Download image from ECR
        # Temporary hack to let scloud app depend on our tflite executor
        biolib_executor_app_version_id = os.environ.get("BIOLIB_EXECUTOR_APP_VERSION_ID", '')
        if biolib_executor_app_version_id and biolib_executor_app_version_id in repo_uri:
            repo_uri = os.environ.get("BIOLIB_SCLOUD_REPO", '')

        if cloud_job['eif_path']:
            image_uri = f'{parent_config.BIOLIB_AWS_ECR_URL}/{repo_uri}'
            image = docker_client.images.pull(image_uri)
            # Send image to enclave
            image_bytes = io.BytesIO()
            for chunk in image.save(named=True):
                image_bytes.write(chunk)

        else:
            if cloud_job['biolib_host'] == 'https://biolib.com':
                image_uri = f'containers.biolib.com/{repo_uri}'
            else:
                image_uri = f'containers.staging.biolib.com/{repo_uri}'

            try:
                docker_client.images.get(image_uri)
            except:
                auth_config = {'username': 'AWS', 'password': cloud_job['access_token']}
                docker_client.images.pull(image_uri, auth_config=auth_config)
            image_bytes = None

        # Pull the remote_hosts image if necessary
        if cloud_job['cloud_job_state']['remote_hosts']:
            try:
                docker_client.images.get('biolib/remote-host-proxy:latest')
            except:
                docker_client.images.pull('biolib/remote-host-proxy:latest')

    except Exception as e:
        log_error(e)
        raise BiolibException("Failed to pull docker image from Biolib Container")

    return (image_bytes, image_uri)


def send_image_data_to_enclave(s, image_bytes):
    try:
        send_request(s, {'route': "load_image", 'size': len(image_bytes.getbuffer())}, check=True)
        send_bytes_to_enclave(s, image_bytes.getbuffer(), check=True)
    except Exception as e:
        log_error(e)
        raise BiolibException("Failed to send image to enclave")


def send_input_data_to_enclave(s, input_data, keys, rsa_key_hex):
    try:
        send_request(s, {'route': "load_data", 'size': len(input_data), 'keys': keys, 'rsa_key_hex': rsa_key_hex}, check=True)
        send_bytes_to_enclave(s, input_data, check=True)
    except Exception as e:
        log_error(e)
        raise BiolibException("Failed to send input data to enclave")


def download_runtime_zip(runtime_zip):
    runtime_zip_data = None
    runtime_zip_size = None
    if runtime_zip:
        r = requests.get(runtime_zip)
        if not r.status_code == 200:
            raise BiolibException("Failed to download runtime zip")
        runtime_zip_data = r.content
        runtime_zip_size = len(r.content)
    return runtime_zip_data, runtime_zip_size


def run_docker_application_in_enclave(s, image_uri, module, cloud_job, runtime_zip=None):
    log_status(message='Downloading source files', progress=70, cloud_job=cloud_job)
    if runtime_zip:
        runtime_zip_data, runtime_zip_size = download_runtime_zip(runtime_zip)
    else:
        runtime_zip_data = None
        runtime_zip_size = None

    log_status(message='Starting computation in enclave', progress=75, cloud_job=cloud_job)

    if cloud_job['cloud_job_state']['remote_hosts']:
        remote_hostnames = [remote_host['hostname'] for remote_host in cloud_job['cloud_job_state']['remote_hosts']]
    else:
        remote_hostnames = []
    
    try:
        send_request(s, {
                'route': "start_compute", 
                'image': image_uri,
                'working_dir': module.get('working_directory'),
                'input_mappings': module.get('input_files_mappings', []), 
                'source_mappings': module.get('source_files_mappings', []),
                'output_mappings': module.get('output_files_mappings', []),
                'module_name': module.get('name'),
                'remote_hostnames': remote_hostnames,
                'command': module.get('command', ''),
                'runtime_zip_size': runtime_zip_size,
            })

    except Exception as e:
        log_error(e)
        raise BiolibException("Failed to send compute request to enclave")

    if runtime_zip_data:
        try:
            check_ok(s)
            send_bytes_to_enclave(s, runtime_zip_data, check=True)
        except Exception as e:
            log_error(e)
            raise BiolibException("Failed to send runtime zip to enclave")

    log_status(message='Computing...', progress=80, cloud_job=cloud_job)

    try:
        result_request = json.loads(s.recv(parent_config.DEFAULT_BUFFER_SIZE).decode())
        s.send("OK".encode())
        log_status(message='Getting result from enclave...', progress=95, cloud_job=cloud_job)
        encrypted_result = readexactly(s, result_request['size'])
    except Exception as e:
        log_error(e)
        raise BiolibException("Failed to run the container in the enclave")
    
    return (encrypted_result, result_request['keys'])


def check_ok(c):
    if c.recv(parent_config.OK_BUFFER_SIZE).decode() != 'OK':
        raise Exception('OK failed')


def send_request(s, request, check=False):
    s.send(json.dumps(request).encode())
    if check:
        check_ok(s)


def send_bytes_to_enclave(s, byte_obj, check=False):
    s.sendall(byte_obj)
    if check:
        check_ok(s)


def readexactly(sock: socket.socket, num_bytes: int) -> bytes:
    buf = bytearray(num_bytes)
    pos = 0
    while pos < num_bytes:
        n = sock.recv_into(memoryview(buf)[pos:])
        if n == 0:
            raise IncompleteReadError(bytes(buf[:pos]), num_bytes)
        pos += n
    return bytes(buf)


def log_status(message, progress, cloud_job):
    biolib_logger = logging.getLogger('biolib')
    biolib_logger.debug(message)
    cloud_job['status_and_progress'] = {'message': message, 'progress': progress}


def log_error(error_message):
    biolib_logger = logging.getLogger('biolib')
    biolib_logger.error(error_message)
