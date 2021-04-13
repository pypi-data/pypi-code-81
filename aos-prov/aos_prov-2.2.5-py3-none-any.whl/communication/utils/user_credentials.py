#
#  Copyright (c) 2018-2021 Renesas Inc.
#  Copyright (c) 2018-2021 EPAM Systems Inc.
#

from os.path import isfile

import OpenSSL
from colorama import Fore, Style

from aos_prov.communication.utils import SDK_SECURITY_PATH
from aos_prov.communication.utils.errors import UserCredentialsError


class UserCredentials(object):

    def __init__(self, cert_file_path: str, key_file_path: str):
        self._cert_file_path = cert_file_path
        self._key_file_path = key_file_path
        self._check_credentials_access()
        self._validate_credentials_format()
        self._cloud_url = self._extract_cloud_url()

    @property
    def cloud_url(self):
        return self._cloud_url

    @property
    def user_credentials(self):
        return self._cert_file_path, self._key_file_path

    def _check_credentials_access(self):
        """ Validate existence and access to user credential files

            Raises:
                UserCredentialsError: If credentials files are not found
            Returns:
                None
        """
        if not isfile(self._cert_file_path):
            text = (f"{Fore.RED}Can't find user certificate file...{Style.RESET_ALL}\n\n"
                    f"Copy file to the default directory: [{SDK_SECURITY_PATH}] \n"
                    f"or set path to the certificate file with argument: --cert \n"
                    f"(Example: aos-prov -u 127.0.0.1 --cert /path/to/certfile) \n")
            raise UserCredentialsError(text)

        if not isfile(self._key_file_path):
            text = (f"{Fore.RED}Can't find user key file...{Style.RESET_ALL}\n\n"
                    f"Copy file to the default directory: [{SDK_SECURITY_PATH}] \n"
                    f"or set path to the key file with argument: --key \n"
                    f"(Example: aos-prov -u 127.0.0.1 --key /path/to/keyfile) \n")
            raise UserCredentialsError(text)

    def _validate_credentials_format(self):
        """ Validate format of user credential files

            Raises:
                UserCredentialsError: If credentials files are in wrong format or with errors
            Returns:
                None
        """
        with open(self._cert_file_path, "rb") as c, open(self._key_file_path, "r") as k:
            cert_content = c.read()
            key_content = k.read()

        try:
            private_key_obj = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, key_content)
        except OpenSSL.crypto.Error:
            raise UserCredentialsError('private key is not correct')

        try:
            cert_obj = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert_content)
        except OpenSSL.crypto.Error:
            raise UserCredentialsError('Certificate is not correct: %s' % key_content)

        context = OpenSSL.SSL.Context(OpenSSL.SSL.TLSv1_2_METHOD)
        context.use_privatekey(private_key_obj)
        context.use_certificate(cert_obj)
        try:
            context.check_privatekey()
        except OpenSSL.SSL.Error:
            raise UserCredentialsError('User private key does not match certificate')

    def _extract_cloud_url(self):
        """Get the Cloud domain name from user certificate"""
        with open(self._cert_file_path, "rb") as cert:
            return OpenSSL.crypto.load_certificate(
                OpenSSL.crypto.FILETYPE_PEM,
                cert.read()
            ).get_subject().organizationName
