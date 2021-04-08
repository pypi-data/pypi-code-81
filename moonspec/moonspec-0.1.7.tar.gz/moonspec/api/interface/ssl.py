import logging
import socket
import ssl
from typing import Optional, Union, Any

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.x509 import Certificate

LOGGER = logging.getLogger('moonspec')


class SSLApi:
    @staticmethod
    def get_remote_x509(host: str, port: int, verify: bool = True, timeout_ms: int = 1000) \
            -> Union[Optional[Certificate], bool]:
        """

        :param host:
        :param port:
        :param verify:
        :param timeout_ms:
        :return: Instance of Certificate, None if certificate can't be retrieved, or False if verify=True, and
                    certificate is invalid.
        """

        context = ssl.create_default_context()

        if verify:
            context.check_hostname = True
            context.verify_mode = ssl.CERT_REQUIRED
        else:
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

        try:
            connection = socket.create_connection((host, port))
            connection.settimeout(timeout_ms / 1000)
        except BaseException as e:
            LOGGER.info('Failed to retrieve remote certificate for %s:%d - %s', host, port, str(e))
            LOGGER.debug('Network error', exc_info=e)
            return None

        try:
            sock = context.wrap_socket(connection, server_hostname=host)
            sock.settimeout(timeout_ms / 1000)
        except ssl.SSLCertVerificationError as e:
            LOGGER.debug('Certificate verification failed for %s:%d - %s', host, port, str(e))
            return False
        except BaseException as e:
            LOGGER.warning('Failed to retrieve certificate for %s:%d', host, port, exc_info=e)
            return None

        try:
            der_cert = sock.getpeercert(True)
        except BaseException as e:
            LOGGER.warning('Failed to retrieve remote certificate for %s:%d', host, port, exc_info=e)
            return None
        finally:
            sock.close()

        if der_cert is None:
            LOGGER.warning('Failed to retrieve remote certificate for %s:%d', host, port)
            return None

        backend: Any = default_backend()  # type: ignore

        return x509.load_der_x509_certificate(der_cert, backend)
