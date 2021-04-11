import logging
import random
import subprocess
import sys
import threading
import socket
from queue import Queue

from biolib.compute_node.socker_listener_thread import SocketListenerThread
from biolib.compute_node.socket_sender_thread import SocketSenderThread
from biolib.biolib_binary_format import AttestationDocument, SystemStatusUpdate, SystemException
from biolib.compute_node.utils import get_package_type, WorkerThreadException, SystemExceptionCodes
from biolib.compute_node.compute_process import compute_process_config

SOCKET_HOST = '127.0.0.1'


class WorkerThread(threading.Thread):
    def __init__(self, compute_state, eif_path=None):
        try:
            super().__init__()
            self.compute_state = compute_state
            self.eif_path = eif_path
            if self.eif_path:
                self.socket_port = 5005
            else:
                self.socket_port = random.choice(range(6000, 65000))
            self.socket = None
            self.connection = None
            self.compute_process = None
            self.connection_thread = None
            self.listener_thread = None
            self.sender_thread = None
            self.biolib_logger = logging.getLogger('biolib')
            self._start_and_connect_to_compute_process()

            self.biolib_logger.debug(f"WorkerThread connected to port {self.socket_port}")

        except Exception as exception:
            raise WorkerThreadException(exception, SystemExceptionCodes.FAILED_TO_INITIALIZE_WORKER_THREAD.value,
                                        worker_thread=self) from exception

    def run(self):
        try:
            while True:
                package = self.compute_state['received_messages_queue'].get()
                package_type = get_package_type(package)

                if package_type == 'AttestationDocument':
                    self.compute_state['attestation_document'] = AttestationDocument(package).deserialize()

                elif package_type == 'SystemStatusUpdate':
                    progress, log_message = SystemStatusUpdate(package).deserialize()
                    self.compute_state['status']['status_updates'].append({'progress': progress,
                                                                           'log_message': log_message})

                elif package_type == 'SystemException':
                    error_code = SystemException(package).deserialize()
                    self.compute_state['status']['error_code'] = error_code
                    self.biolib_logger.debug("Hit error. Terminating Worker Thread and Compute Process")
                    self.terminate()

                elif package_type == 'ModuleOutput' or package_type == 'AesEncryptedPackage':
                    self.compute_state['result'] = package
                    self.compute_state['status']['status_updates'].append({'progress': 95,
                                                                           'log_message': 'Result Ready'})
                    self.terminate()

                else:
                    raise Exception(f'Package type from child was not recognized: {package}')

                self.compute_state['received_messages_queue'].task_done()

        except Exception as exception:
            raise WorkerThreadException(exception, SystemExceptionCodes.FAILED_TO_HANDLE_PACKAGE_IN_WORKER_THREAD.value,
                                        worker_thread=self) from exception

    def _start_and_connect_to_compute_process(self):
        if self.eif_path:
            self.socket = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)  # pylint: disable=no-member
            cid = socket.VMADDR_CID_ANY  # pylint: disable=no-member
            self.socket.bind((cid, self.socket_port))
        else:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((SOCKET_HOST, self.socket_port))

        self.socket.listen()

        received_messages_queue = Queue()
        messages_to_send_queue = Queue()

        # Starting a thread for accepting connections before starting the process that should to connect to the socket
        self.connection_thread = threading.Thread(target=self._accept_new_socket_connection, args=[
            received_messages_queue,
            messages_to_send_queue
        ])
        self.connection_thread.start()

        if self.eif_path:
            self.compute_process = subprocess.Popen(['sudo', 'nitro-cli', 'run-enclave',
                                                     '--cpu-count',
                                                     compute_process_config.CPU_COUNT_TO_PROVISION_ENCLAVE,
                                                     '--memory',
                                                     compute_process_config.MEMORY_TO_PROVISION_ENCLAVE,
                                                     '--eif-path', self.eif_path])

        else:
            self.compute_process = subprocess.Popen(['biolib', 'start-compute-process', '--port',
                                                     str(self.socket_port)])

        self.compute_state['received_messages_queue'] = received_messages_queue
        self.compute_state['messages_to_send_queue'] = messages_to_send_queue
        self.compute_state['worker_thread'] = self

    def _accept_new_socket_connection(self, received_messages_queue, messages_to_send_queue):
        self.connection, _ = self.socket.accept()
        self.listener_thread = SocketListenerThread(self.connection, received_messages_queue)
        self.listener_thread.start()

        self.sender_thread = SocketSenderThread(self.connection, messages_to_send_queue)
        self.sender_thread.start()

    def terminate(self):
        if self.compute_process:
            self.biolib_logger.debug(f"Terminating Compute Process with PID {self.compute_process.pid}")
            self.compute_state['messages_to_send_queue'].put(b'STOP')

        if self.sender_thread:
            self.sender_thread.terminate()

        if self.listener_thread:
            self.listener_thread.terminate()

        if self.socket:
            self.socket.close()

        if self.connection:
            self.connection.close()

        self.biolib_logger.debug("Terminating Worker Thread")
        sys.exit()
