import io
import json
import logging
import socket
import threading
import zipfile
import time
from queue import Queue

import requests
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

from biolib.compute_node.socker_listener_thread import SocketListenerThread
from biolib.compute_node.socket_sender_thread import SocketSenderThread
from biolib.compute_node.compute_process.biolib_docker_client import BiolibDockerClient
from biolib.compute_node.compute_process.mappings import Mappings, path_without_first_folder
from biolib.compute_node.compute_process.utils import ComputeProcessException
from biolib.compute_node.utils import get_package_type, SystemExceptionCodes, enclave_remote_hosts
from biolib.biolib_binary_format import AttestationDocument, SavedJob, SystemStatusUpdate, ModuleInput, ModuleOutput,\
    RsaEncryptedAesPackage, AesEncryptedPackage

try:
    from biolib.compute_node.compute_process.nsm_util import NSMUtil
except ImportError:
    pass

DEFAULT_BUFFER_SIZE = 1024
SOCKET_HOST = '127.0.0.1'


class ComputeProcess:
    def __init__(self, socket_port, is_running_in_enclave):
        try:
            self.is_running_in_enclave = is_running_in_enclave
            self.biolib_logger = logging.getLogger('biolib')
            if self.is_running_in_enclave:
                self.socket_port = 5005
                self.nsm_util = NSMUtil()
                self.aes_key_buffer = b''
                self.biolib_logger.setLevel(logging.DEBUG)
            else:
                self.socket_port = socket_port
            self.received_messages_queue = Queue()
            self.messages_to_send_queue = Queue()
            self.biolib_docker_client = BiolibDockerClient(self.is_running_in_enclave, self.messages_to_send_queue)
            self.access_token = ''
            self.biolib_host = ''
            self.ecr_proxy = ''
            self.enclave_ecr_token = ''
            self.job_id = ''
            self.remote_hostnames = []
            self.runtime_zip_data = None
            self.module = None
            self.locks = {
                'runtime_zip': threading.Lock(),
                'remote_host_proxies': threading.Lock(),
                'image': threading.Lock()
            }

        except Exception as exception:
            raise ComputeProcessException(exception,
                                          SystemExceptionCodes.FAILED_TO_INIT_COMPUTE_PROCESS_VARIABLES.value,
                                          self.messages_to_send_queue) from exception

        self.biolib_docker_client.create_networks()
        if self.is_running_in_enclave:
            self.biolib_docker_client.start_remote_host_proxies(enclave_remote_hosts, self.locks['remote_host_proxies'])
            # Block until all proxies are created
            self.locks['remote_host_proxies'].acquire()
            self.locks['remote_host_proxies'].release()

        self.connect_to_parent()

    def run(self):
        self.biolib_logger.debug("Started Compute Process")
        while True:
            try:
                package = self.received_messages_queue.get()
                if package == b'STOP':
                    self.biolib_docker_client.delete_old_state()
                    break

                package_type = get_package_type(package)
                if package_type == 'RsaEncryptedAesPackage':
                    encrypted_aes_key, iv, _, encrypted_data = RsaEncryptedAesPackage(package).deserialize()
                    self.aes_key_buffer = self.nsm_util.decrypt(encrypted_aes_key)
                    aes_key = AES.new(self.aes_key_buffer, AES.MODE_GCM, iv)

                    package = aes_key.decrypt(encrypted_data)
                    package_type = get_package_type(package)

                if package_type == 'SavedJob':
                    runtime_zip_link = self.get_runtime_zip_link_and_set_fields_from_job_package(package)
                    if runtime_zip_link:
                        self.send_status_update(progress=25, log_message='Downloading Source Files...')
                        self.get_runtime_zip(runtime_zip_link)

                    if self.remote_hostnames:
                        self.send_status_update(progress=35,
                                                log_message='Starting Remote Hosts...')
                        self.biolib_docker_client.start_remote_host_proxies(self.remote_hostnames,
                                                                            self.locks['remote_host_proxies'])

                elif package_type == 'ModuleInput':
                    module_input = ModuleInput(package).deserialize()
                    self.start_compute(module_input, self.job_id)

                else:
                    self.biolib_logger.warning(f'Package type from parent was not recognized: {package}')

                self.received_messages_queue.task_done()
            except ComputeProcessException:
                continue

            except Exception as exception:
                raise ComputeProcessException(exception, SystemExceptionCodes.UNKOWN_COMPUTE_PROCESS_ERROR.value,
                                              self.messages_to_send_queue) from exception

    def start_compute(self, module_input, job_id):
        self.block_until_data_is_available_for_compute()
        if self.module['environment'] == 'biolib-app':
            job = self.get_job_for_external_app()
            job_id = job['public_id']
            module_input_with_runtime_code = self.add_runtime_zip_and_command_to_module_input(module_input)

            if 'client_side_executable_zip' in job['app_version']:
                self.get_runtime_zip(job['app_version']['client_side_executable_zip'])

            self.module = self.get_module_from_name(job['app_version']['modules'], 'main')
            self.start_compute(module_input_with_runtime_code, job_id)
            return

        self.send_status_update(progress=55, log_message='Pulling images...')
        self.biolib_docker_client.pull_image(self.module['image_uri'], self.access_token, job_id,
                                             self.locks['image'], self.ecr_proxy, self.enclave_ecr_token)
        threading.Thread(target=self._compute, args=(module_input,)).start()

    def _compute(self, module_input):
        # Block until the image has been pulled
        self.locks['image'].acquire()
        self.send_status_update(progress=70, log_message='Computing...')
        start_time = time.time()

        self.biolib_docker_client.create_compute_container(
            image=f'{self.ecr_proxy}/{self.module["image_uri"]}',
            command=f'{self.module["command"]} {" ".join(module_input["arguments"])}',
            working_dir=self.module['working_directory']
        )

        # Also pass arguments so we can parse $ variables when mapping later
        self.biolib_docker_client.set_mappings(
            self.module['input_files_mappings'],
            self.module['source_files_mappings'],
            self.module['output_files_mappings'],
            module_input['arguments']
        )

        if self.runtime_zip_data:
            self.biolib_docker_client.map_and_copy_runtime_files_to_container(self.runtime_zip_data)

        self.biolib_docker_client.map_and_copy_input_files_to_container(module_input['files'])

        stdout, stderr, exit_code, mapped_output_files = self.biolib_docker_client.run_container()

        try:
            module_output = ModuleOutput().serialize(stdout, stderr, exit_code, mapped_output_files)
            if self.is_running_in_enclave:
                module_output_to_send = self.wrap_in_aes_encrypted_package(module_output)
            else:
                module_output_to_send = module_output

            self.biolib_logger.debug(f'Compute time: {time.time() - start_time}')
            self.messages_to_send_queue.put(module_output_to_send)

        except Exception as exception:
            raise ComputeProcessException(exception,
                                          SystemExceptionCodes.FAILED_TO_SERIALIZE_AND_SEND_MODULE_OUTPUT.value,
                                          self.messages_to_send_queue) from exception

    def connect_to_parent(self):
        try:
            if self.is_running_in_enclave:
                parent_socket = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)  # pylint: disable=no-member
                parent_socket.connect((3, int(self.socket_port)))

            else:
                parent_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                parent_socket.connect((SOCKET_HOST, int(self.socket_port)))

        except Exception as exception:
            raise ComputeProcessException(exception,
                                          SystemExceptionCodes.FAILED_TO_CONNECT_TO_WORKER_THREAD_SOCKET.value,
                                          self.messages_to_send_queue) from exception

        try:
            SocketListenerThread(parent_socket, self.received_messages_queue).start()
            SocketSenderThread(parent_socket, self.messages_to_send_queue).start()
        except Exception as exception:
            raise ComputeProcessException(exception,
                                          SystemExceptionCodes.FAILED_TO_START_SENDER_THREAD_OR_RECEIVER_THREAD.value,
                                          self.messages_to_send_queue) from exception

        try:
            if self.is_running_in_enclave:
                attestation_document = self.nsm_util.get_attestation_doc()
            else:
                attestation_document = b'Running locally'
        except Exception as exception:
            raise ComputeProcessException(exception, SystemExceptionCodes.FAILED_TO_GET_ATTESTATION_DOCUMENT.value,
                                          self.messages_to_send_queue) from exception

        self.messages_to_send_queue.put(AttestationDocument().serialize(attestation_document))

    def get_runtime_zip_link_and_set_fields_from_job_package(self, package):
        try:
            saved_job_json_string = SavedJob(package).deserialize()
            saved_job = json.loads(saved_job_json_string)

            remote_hosts = saved_job['job']['app_version']['remote_hosts']
            self.remote_hostnames = [remote_host['hostname'] for remote_host in remote_hosts]
            self.job_id = saved_job['job']['public_id']
            self.biolib_host = saved_job['BIOLIB_HOST']
            if self.biolib_host == 'https://biolib.com':
                self.ecr_proxy = 'containers.biolib.com'
            else:
                self.ecr_proxy = 'containers.staging.biolib.com'

            if 'enclave_ecr_token' in saved_job:
                self.enclave_ecr_token = saved_job['enclave_ecr_token']

            if 'access_token' in saved_job:
                self.access_token = saved_job['access_token']

            module_name = saved_job['module_name']
            self.module = self.get_module_from_name(saved_job['job']['app_version']['modules'], module_name)

            if 'client_side_executable_zip' in saved_job['job']['app_version']:
                return saved_job['job']['app_version']['client_side_executable_zip']
            else:
                return ''

        except Exception as exception:
            raise ComputeProcessException(exception, SystemExceptionCodes.FAILED_TO_DESERIALIZE_SAVED_JOB.value,
                                          self.messages_to_send_queue) from exception

    def get_job_for_external_app(self):
        try:
            data = {'app_version_id': self.module['image_uri']}
            if self.access_token:
                headers = {'Authentication': f'Bearer {self.access_token}'}
            else:
                headers = {}
            req = requests.post(f'{self.biolib_host}/api/jobs/', json=data, headers=headers)
        except Exception as exception:
            raise ComputeProcessException(exception, SystemExceptionCodes.FAILED_TO_CONTACT_BACKEND_TO_CREATE_JOB.value,
                                          self.messages_to_send_queue) from exception

        if req.status_code != 201:
            raise ComputeProcessException(Exception(req.content), SystemExceptionCodes.FAILED_TO_CREATE_NEW_JOB.value,
                                          self.messages_to_send_queue)
        return req.json()

    def add_runtime_zip_and_command_to_module_input(self, module_input):
        # TODO: Figure out if we ever forward output mappings correctly (Do we only the mapping of the base image?)
        # TODO: Reuse much of the make_runtime_tar logic in BiolibDockerClient
        try:
            if self.runtime_zip_data:
                runtime_zip = zipfile.ZipFile(io.BytesIO(self.runtime_zip_data))
                source_mappings = Mappings(self.module['source_files_mappings'], module_input['arguments'])
                for zip_file_name in runtime_zip.namelist():
                    file_path = '/' + path_without_first_folder(zip_file_name)
                    mapped_file_names = source_mappings.get_mappings_for_path(file_path)
                    for mapped_file_name in mapped_file_names:
                        file_data = runtime_zip.read(zip_file_name)
                        module_input['files'].update({mapped_file_name: file_data})

            for command_part in reversed(self.module['command'].split()):
                module_input['arguments'].insert(0, command_part)

        except Exception as exception:
            raise ComputeProcessException(exception, SystemExceptionCodes.FAILED_TO_CREATE_NEW_JOB.value,
                                          self.messages_to_send_queue) from exception
        return module_input

    def get_runtime_zip(self, runtime_zip_link):
        # TODO: Implement caching of runtime zip
        try:
            self.locks['runtime_zip'].acquire()
            threading.Thread(target=self._download_runtime_zip_from_s3, args=[runtime_zip_link]).start()
        except Exception as exception:
            raise ComputeProcessException(exception,
                                          SystemExceptionCodes.FAILED_TO_START_RUNTIME_ZIP_DOWNLOAD_THREAD.value,
                                          self.messages_to_send_queue) from exception

    def _download_runtime_zip_from_s3(self, runtime_zip_link):
        start_time = time.time()
        self.biolib_logger.debug(f"Downloading runtime zip from s3 link: {runtime_zip_link}")
        try:
            self.runtime_zip_data = requests.get(runtime_zip_link).content
        except Exception as exception:
            raise ComputeProcessException(exception, SystemExceptionCodes.FAILED_TO_DOWNLOAD_RUNTIME_ZIP.value,
                                          self.messages_to_send_queue) from exception
        self.biolib_logger.debug(f'Downloading runtime zip took: {time.time() - start_time}s')
        self.locks['runtime_zip'].release()

    def block_until_data_is_available_for_compute(self):
        # Block until the required data is available
        try:
            for lock_name, lock in self.locks.items():
                self.biolib_logger.debug(f"Waiting for {lock_name}")
                lock.acquire()
                lock.release()
        except Exception as exception:
            raise ComputeProcessException(exception, SystemExceptionCodes.FAILED_TO_GET_REQUIRED_DATA_FOR_COMPUTE.value,
                                          self.messages_to_send_queue) from exception

    def get_module_from_name(self, modules, module_name):
        for module in modules:
            if module['name'] == module_name:
                return module
        raise Exception(f"Could not find module with name {module_name} in given modules")

    def wrap_in_aes_encrypted_package(self, package):
        iv = get_random_bytes(12)
        aes_key = AES.new(self.aes_key_buffer, AES.MODE_GCM, iv)
        encrypted_package, tag = aes_key.encrypt_and_digest(package)
        aes_encrypted_package = AesEncryptedPackage().serialize(iv, tag, encrypted_package)
        return aes_encrypted_package

    def send_status_update(self, progress, log_message):
        try:
            status_update_package = SystemStatusUpdate().serialize(progress, log_message)
            self.biolib_logger.info(log_message)
            self.messages_to_send_queue.put(status_update_package)
        except Exception as exception:
            raise ComputeProcessException(exception, SystemExceptionCodes.FAILED_TO_SEND_STATUS_UPDATE.value,
                                          self.messages_to_send_queue) from exception
