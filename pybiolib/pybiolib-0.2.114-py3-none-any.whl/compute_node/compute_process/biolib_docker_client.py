import subprocess
import threading
import time
import tarfile
import zipfile
import logging
import os
import io

import docker
from docker.errors import ImageNotFound, APIError

from biolib.compute_node.compute_process import compute_process_config
from biolib.compute_node.compute_process.mappings import Mappings, path_without_first_folder
from biolib.compute_node.compute_process.utils import ComputeProcessException
from biolib.compute_node.utils import SystemExceptionCodes, random_string


class BiolibDockerClient():
    """
    An abstraction to manage and run biolib docker containers
    """

    def __init__(self, is_running_in_enclave, messages_to_send_queue):
        self.is_running_in_enclave = is_running_in_enclave
        self.messages_to_send_queue = messages_to_send_queue
        self.biolib_logger = logging.getLogger('biolib')
        self.docker_api_client = docker.APIClient(base_url=compute_process_config.DOCKER_SOCKET_PATH)
        self.docker_client = docker.from_env()
        self.container = None
        self.container_id = None
        self.source_mappings = None
        self.input_mappings = None
        self.output_mappings = None
        self.arguments = None
        self.biolib_logger = logging.getLogger('biolib')
        self.proxies = []
        self.remote_hostnames = []
        self.random_docker_id = random_string(15)
        self.internal_network = None
        self.public_network = None
        self.compute_process_dir = os.path.dirname(os.path.realpath(__file__))
        self.runtime_tar_path = f'{self.compute_process_dir}/tars/runtime_{self.random_docker_id}.tar'
        self.input_tar_path = f'{self.compute_process_dir}/tars/input_{self.random_docker_id}.tar'

    def delete_old_state(self):
        tar_time = time.time()
        for path_to_delete in [self.input_tar_path, self.runtime_tar_path]:
            if os.path.exists(path_to_delete):
                os.remove(path_to_delete)
        self.biolib_logger.debug(f"Deleted tars in: {time.time() - tar_time}")

        proxy_time = time.time()
        for proxy in self.proxies:
            proxy['container'].remove(force=True)
        self.biolib_logger.debug(f"Deleted proxies in: {time.time() - proxy_time}")

        container_time = time.time()
        if self.container:
            if self.container.status != 'exited':
                self.container.stop()
            self.container.remove()
        self.biolib_logger.debug(f"Deleted compute container in: {time.time() - container_time}")

        network_time = time.time()
        if self.internal_network:
            self.internal_network.remove()
        if self.public_network:
            self.public_network.remove()
        self.biolib_logger.debug(f"Deleted networks in: {time.time() - network_time}")

    def create_networks(self):
        try:
            self.internal_network = self.docker_client.networks.create(
                name='biolib-sandboxed-network-' + self.random_docker_id,
                internal=True,
                driver="bridge"
            )
            self.public_network = self.docker_client.networks.create(
                name='biolib-proxy-network-' + self.random_docker_id,
                internal=False,
                driver="bridge"
            )
        except Exception as exception:
            raise ComputeProcessException(exception, SystemExceptionCodes.FAILED_TO_CREATE_DOCKER_NETWORKS.value,
                                          self.messages_to_send_queue) from exception

    def start_remote_host_proxies(self, remote_hostnames, remote_host_lock: threading.Lock):
        try:
            remote_host_lock.acquire()

            # The enclave currently always has the remote-host-proxy image
            if not self.is_running_in_enclave:
                try:
                    self.docker_client.images.get('biolib/remote-host-proxy:latest')
                except ImageNotFound:
                    self.biolib_logger.debug('Pulling remote host docker image...')
                    self.docker_client.images.pull('biolib/remote-host-proxy:latest')

            nr_of_desired_remote_hosts = len(self.proxies) + len(remote_hostnames)
            threading.Thread(target=self._release_remote_hosts_proxies_lock_when_all_created,
                             args=(nr_of_desired_remote_hosts, remote_host_lock)).start()

            # This allows the function to be called multiple times with different hosts in an enclave
            last_used_vsock_port = 8000 + len(self.proxies)
            last_used_local_port = 64000 + len(self.proxies)

            for host_id, hostname in enumerate(remote_hostnames):
                if self.is_running_in_enclave:
                    vsock_port = last_used_vsock_port + host_id
                    local_port = last_used_local_port + host_id
                    forwarder_cid = '3'
                    self.biolib_logger.debug(f"Starting traffic forwarder forwarding to port {local_port} "
                                             f"for hostname {hostname}")
                    subprocess.Popen(['python3', f'{self.compute_process_dir}/traffic_forwarder.py', str(local_port),
                                      forwarder_cid, str(vsock_port)])
                else:
                    local_port = None

                threading.Thread(target=self._start_remote_host_proxy, args=(hostname, local_port)).start()

        except Exception as exception:
            raise ComputeProcessException(exception, SystemExceptionCodes.FAILED_TO_START_REMOTE_HOST_PROXIES.value,
                                          self.messages_to_send_queue) from exception

    def _release_remote_hosts_proxies_lock_when_all_created(self, nr_of_desired_remote_hosts,
                                                            remote_host_lock: threading.Lock):
        # Block until all remote hosts proxies has been created
        # TODO: Maybe write this with locks
        start_time = time.time()
        while len(self.proxies) != nr_of_desired_remote_hosts:
            time.sleep(0.1)
            continue

        try:
            if self.is_running_in_enclave:
                hosts_file = open('/etc/hosts', 'a')
                for proxy in self.proxies:
                    hosts_file.write(f'\n{proxy["ip"]} {proxy["hostname"]}')
                hosts_file.close()
            remote_host_lock.release()
        except Exception as exception:
            raise ComputeProcessException(exception,
                                          SystemExceptionCodes.FAILED_TO_REDIRECT_ENCLAVE_TRAFFIC_TO_PROXIES.value,
                                          self.messages_to_send_queue) from exception

        self.biolib_logger.debug(f'Starting remote hosts proxies took: {time.time() - start_time}s')

    def _start_remote_host_proxy(self, remote_hostname, local_traffic_forwarder_port=None):
        try:
            if self.is_running_in_enclave:
                extra_hosts = {remote_hostname: self.public_network.attrs['IPAM']['Config'][0]['Gateway']}
            else:
                extra_hosts = None

            proxy_container = self.docker_client.containers.create(
                image='biolib/remote-host-proxy:latest',
                network=self.internal_network.name,
                publish_all_ports=True,
                name='biolib-remote-hosts-proxy-' + remote_hostname + '-' + self.random_docker_id,
                extra_hosts=extra_hosts,
                detach=True
            )
        except Exception as exception:
            raise ComputeProcessException(exception, SystemExceptionCodes.FAILED_TO_CREATE_PROXY_CONTAINER.value,
                                          self.messages_to_send_queue) from exception

        try:
            if self.is_running_in_enclave:
                upstream_http_port = local_traffic_forwarder_port
                upstream_https_port = local_traffic_forwarder_port
            else:
                upstream_http_port = 80
                upstream_https_port = 443

            nginx_config = f"""
                events {{}}
                error_log /dev/stdout info;
                stream {{
                    upstream forward-http {{
                        server {remote_hostname}:{upstream_http_port};
                    }}
                    upstream forward-https {{
                        server {remote_hostname}:{upstream_https_port};
                    }}
                    server {{
                        listen     80;
                        proxy_pass forward-http;
                    }}
                    server {{
                        listen     443;
                        proxy_pass forward-https;
                    }}
                }}
            """
            tar_name = f'{self.compute_process_dir}/tars/remote_hosts_{self.random_docker_id}_{remote_hostname}.tar'
            remote_host_tar = tarfile.open(tar_name, 'w')
            nginx_conf_path = '/etc/nginx/nginx.conf'
            self.add_file_to_tar(remote_host_tar, nginx_conf_path, nginx_conf_path, nginx_config.encode())
            remote_host_tar.close()
            remote_hosts_tar_data = open(tar_name, 'rb').read()
            self.docker_api_client.put_archive(proxy_container.id, '/', remote_hosts_tar_data)
        except Exception as exception:
            raise ComputeProcessException(exception, SystemExceptionCodes.FAILED_TO_CONFIGURE_ALLOWED_REMOTE_HOST.value,
                                          self.messages_to_send_queue) from exception

        try:
            self.docker_api_client.start(proxy_container.id)
            self.public_network.connect(proxy_container.id)

            proxy_container.reload()
            proxy_container_ip = proxy_container.attrs['NetworkSettings']['Networks'][self.internal_network.name][
                'IPAddress']
            self.proxies.append({
                'container': proxy_container,
                'ip': proxy_container_ip,
                'hostname': remote_hostname,
            })
            os.remove(tar_name)
        except Exception as exception:
            raise ComputeProcessException(exception, SystemExceptionCodes.FAILED_TO_CONFIGURE_ALLOWED_REMOTE_HOST.value,
                                          self.messages_to_send_queue) from exception

    def pull_image(self, image_uri, access_token, job_id, image_lock: threading.Lock(), ecr_proxy, enclave_ecr_token):
        try:
            image_lock.acquire()
            threading.Thread(target=self._pull, args=(image_uri, access_token, job_id, image_lock, ecr_proxy,
                                                      enclave_ecr_token)).start()
        except Exception as exception:
            raise ComputeProcessException(exception, SystemExceptionCodes.FAILED_TO_START_IMAGE_PULLING_THREAD.value,
                                          self.messages_to_send_queue) from exception

    def _pull(self, image_uri, access_token, job_id, image_lock, ecr_proxy, enclave_ecr_token):
        try:
            start_time = time.time()
            image_uri = f'{ecr_proxy}/{image_uri}'

            try:
                self.docker_client.images.get(image_uri)
            except ImageNotFound:
                if enclave_ecr_token:
                    tokens = f'{enclave_ecr_token},{job_id}'
                    auth_config = {'username': 'AWS', 'password': tokens}
                else:
                    tokens = f'{access_token},{job_id}'
                    auth_config = {'username': 'AWS', 'password': tokens}
                self.docker_client.images.pull(image_uri, auth_config=auth_config)

            self.biolib_logger.debug(f"Pulled image in: {time.time() - start_time}")
            image_lock.release()
        except Exception as exception:
            raise ComputeProcessException(exception, SystemExceptionCodes.FAILED_TO_PULL_DOCKER_IMAGE.value,
                                          self.messages_to_send_queue) from exception

    def set_mappings(self, input_mappings, source_mappings, output_mappings, arguments):
        self.input_mappings = input_mappings
        self.source_mappings = source_mappings
        self.output_mappings = output_mappings
        self.arguments = arguments

    def create_compute_container(self, image, command, working_dir):
        try:
            if self.proxies:
                extra_hosts = {proxy['hostname']: proxy['ip'] for proxy in self.proxies}
            else:
                extra_hosts = {}

            self.container = self.docker_client.containers.create(
                image=image,
                command=command,
                working_dir=working_dir,
                network=self.internal_network.name,
                extra_hosts=extra_hosts
            )
            self.container_id = self.container.id
        except Exception as exception:
            raise ComputeProcessException(exception,
                                          SystemExceptionCodes.FAILED_TO_START_COMPUTE_CONTAINER.value,
                                          self.messages_to_send_queue) from exception

    def run_container(self):
        try:
            self.docker_api_client.start(self.container_id)

            exit_code = self.docker_api_client.wait(self.container_id)['StatusCode']

            stdout = self.docker_api_client.logs(self.container_id, stdout=True, stderr=False)
            stderr = self.docker_api_client.logs(self.container_id, stdout=False, stderr=True)

            mapped_output_files = self.get_output_files()
            return stdout, stderr, exit_code, mapped_output_files

        except Exception as exception:
            raise ComputeProcessException(exception, SystemExceptionCodes.FAILED_TO_RUN_COMPUTE_CONTAINER.value,
                                          self.messages_to_send_queue) from exception

    def add_file_to_tar(self, tar, current_path, mapped_path, data):
        if current_path.endswith('/'):
            # Remove trailing slash as tarfile.addfile appends it automatically
            tarinfo = tarfile.TarInfo(name=mapped_path[:-1])
            tarinfo.type = tarfile.DIRTYPE
            tar.addfile(tarinfo)

        else:
            tarinfo = tarfile.TarInfo(name=mapped_path)
            file_like = io.BytesIO(data)
            tarinfo.size = len(file_like.getvalue())
            tar.addfile(tarinfo, file_like)

    def make_input_tar(self, files):
        input_tar = tarfile.open(self.input_tar_path, 'w')
        input_mappings = Mappings(self.input_mappings, self.arguments)
        for path, data in files.items():
            # Make all paths absolute
            if not path.startswith('/'):
                path = '/' + path

            mapped_file_names = input_mappings.get_mappings_for_path(path)
            for mapped_file_name in mapped_file_names:
                self.add_file_to_tar(tar=input_tar, current_path=path, mapped_path=mapped_file_name, data=data)

        input_tar.close()

    def make_runtime_tar(self, runtime_zip_data):
        runtime_tar = tarfile.open(self.runtime_tar_path, 'w')
        runtime_zip = zipfile.ZipFile(io.BytesIO(runtime_zip_data))
        source_mappings = Mappings(self.source_mappings, self.arguments)

        for zip_file_name in runtime_zip.namelist():
            # Make paths absolute and remove root folder from path
            file_path = '/' + path_without_first_folder(zip_file_name)
            mapped_file_names = source_mappings.get_mappings_for_path(file_path)
            for mapped_file_name in mapped_file_names:
                file_data = runtime_zip.read(zip_file_name)
                self.add_file_to_tar(tar=runtime_tar, current_path=zip_file_name, mapped_path=mapped_file_name,
                                     data=file_data)

        runtime_tar.close()

    def map_and_copy_input_files_to_container(self, files):
        try:
            self.make_input_tar(files)
            input_tar_bytes = open(self.input_tar_path, 'rb').read()
            self.docker_api_client.put_archive(self.container_id, '/', input_tar_bytes)
        except Exception as exception:
            raise ComputeProcessException(exception,
                                          SystemExceptionCodes.FAILED_TO_COPY_INPUT_FILES_TO_COMPUTE_CONTAINER.value,
                                          self.messages_to_send_queue) from exception

    def map_and_copy_runtime_files_to_container(self, runtime_zip_data):
        try:
            self.make_runtime_tar(runtime_zip_data)
            runtime_tar_bytes = open(self.runtime_tar_path, 'rb').read()
            self.docker_api_client.put_archive(self.container_id, '/', runtime_tar_bytes)
        except Exception as exception:
            raise ComputeProcessException(exception,
                                          SystemExceptionCodes.FAILED_TO_COPY_RUNTIME_FILES_TO_COMPUTE_CONTAINER.value,
                                          self.messages_to_send_queue) from exception

    def get_output_files(self):
        try:
            input_tar = tarfile.open(self.input_tar_path)
            input_tar_filelist = input_tar.getnames()

            if os.path.exists(self.runtime_tar_path):
                runtime_tar = tarfile.open(self.runtime_tar_path)
                runtime_tar_filelist = runtime_tar.getnames()
            else:
                runtime_tar = None

            mapped_output_files = {}
            for mapping in self.output_mappings:
                try:
                    tar_bytes_generator, _ = self.docker_api_client.get_archive(self.container_id, mapping['from_path'])
                except APIError:
                    self.biolib_logger.warning(f'Could not get output from path {mapping["from_path"]}')
                    continue

                tar_bytes_obj = io.BytesIO()
                for chunk in tar_bytes_generator:
                    tar_bytes_obj.write(chunk)

                tar = tarfile.open(fileobj=io.BytesIO(tar_bytes_obj.getvalue()))
                for file in tar.getmembers():
                    file_obj = tar.extractfile(file)

                    # Skip empty dirs
                    if not file_obj:
                        continue
                    file_data = tar.extractfile(file).read()

                    # Remove parent dir from tar file name and prepend from_path.
                    # Except if from_path is root '/', that works out of the box
                    if mapping['from_path'].endswith('/') and mapping['from_path'] != '/':
                        file_name = mapping['from_path'] + path_without_first_folder(file.name)

                    # When getting a file use the from_path.
                    # This is due to directory info (absolute path) being lost when using get_archive on files
                    else:
                        file_name = mapping['from_path']

                    # Filter out unchanged input files
                    if file_name in input_tar_filelist and input_tar.extractfile(file_name).read() == file_data:
                        continue

                    # Filter out unchanged source files if provided
                    if runtime_tar and file_name in runtime_tar_filelist and runtime_tar.extractfile(
                            file_name).read() == file_data:
                        continue

                    mapped_file_names = Mappings([mapping], self.arguments).get_mappings_for_path(file_name)
                    for mapped_file_name in mapped_file_names:
                        mapped_output_files[mapped_file_name] = file_data

        except Exception as exception:
            raise ComputeProcessException(exception, SystemExceptionCodes.FAILED_TO_RUN_COMPUTE_CONTAINER.value,
                                          self.messages_to_send_queue) from exception

        return mapped_output_files
