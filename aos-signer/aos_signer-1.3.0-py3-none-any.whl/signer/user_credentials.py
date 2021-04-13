#
#  Copyright (c) 2018-2019 Renesas Inc.
#  Copyright (c) 2018-2019 EPAM Systems Inc.
#

from os.path import join, exists, expanduser, isabs

import OpenSSL

from aos_signer.service_config.service_configuration import ServiceConfiguration
from aos_signer.signer.errors import SignerConfigError


class UserCredentials(object):

    DEFAULT_USER_CREDENTIALS_FOLDER = join(expanduser("~"), '.aos/security')

    def __init__(self, config: ServiceConfiguration):
        self._config = config
        self._sign_key_path = None
        self._sign_cert_path = None
        self._upload_key_path = None
        self._upload_cert_path = None

    @property
    def sign_key_path(self):
        return self._sign_key_path

    @property
    def sign_cert_path(self):
        return self._sign_cert_path

    @property
    def upload_key_path(self):
        return self._upload_key_path

    @property
    def upload_cert_path(self):
        return self._upload_cert_path

    def find_sign_key_and_cert(self):
        self._sign_key_path = self.__find_user_cred_file(self._config.build.sign_key, 'build->sign_key')
        self._sign_cert_path = self.__find_user_cred_file(
            self._config.build.sign_certificate, 'build->sign_certificate')

    def find_upload_key_and_cert(self):
        if self._config.publish.tls_key is not None:
            self._upload_key_path = self.__find_user_cred_file(
                self._config.publish.tls_key, 'publish->tls_key')
        else:
            self._upload_key_path = self.__find_user_cred_file(
                self._config.build.sign_key, 'build->sign_key')

        if self._config.publish.tls_certificate is not None:
            self._upload_cert_path = self.__find_user_cred_file(
                self._config.publish.tls_certificate, 'publish -> sign_certificate')
        else:
            self._upload_cert_path = self.__find_user_cred_file(
                self._config.build.sign_certificate, 'build -> sign_key')

    def __find_user_cred_file(self, config_file_name: str, config_entry: str) -> str:
        """Search for file by absolute path, in `meta` folder or in default keys folder.

        Args:
            config_file_name (str): Filename or absolute file path.
            config_entry (str): Place in config to show error to user.
        Raises:
            SignerConfigError: If received absolute path and file not found or received relative path and file not
                               found nor in meta neither in aos folders.
        Returns:
            str: Path to existing file
        """
        path = config_file_name
        if isabs(path):
            if exists(path):
                return path
            else:
                raise SignerConfigError('{} is set to absolute path but file not found.'.format(config_entry))

        for search_dir in (self._config.DEFAULT_META_FOLDER, self.DEFAULT_USER_CREDENTIALS_FOLDER):
            path = join(search_dir, config_file_name)
            if exists(path):
                return path
        raise SignerConfigError(
                'Configured [{}] file is set to [{}], but file not found neither in [{}] nor in [{}] directory.'.format(
                    config_entry,
                    config_file_name,
                    self._config.DEFAULT_META_FOLDER,
                    self.DEFAULT_USER_CREDENTIALS_FOLDER
                )
            )

    @staticmethod
    def __validate_key_cert_pair(key_path, cert_path):
        """Check key and certificate are in valid format and certificate is derived from the key.

        Args:
            key_path (str): Path to key file.
            cert_path (str): Path to certificate file.
        Raises:
            SignerConfigError: In case of any certificate or key error.
        Returns:
            None: if no errors
        """
        with open(cert_path, "rb") as c, open(key_path, "rb") as k:
            cert_content = c.read()
            key_content = k.read()

        try:
            private_key_obj = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, key_content)
        except OpenSSL.crypto.Error:
            raise SignerConfigError('Private key {} is not correct'.format(key_path))

        try:
            cert_obj = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert_content)
        except OpenSSL.crypto.Error:
            raise SignerConfigError('Certificate {} is not correct'.format(cert_path))

        context = OpenSSL.SSL.Context(OpenSSL.SSL.TLSv1_2_METHOD)
        context.use_privatekey(private_key_obj)
        context.use_certificate(cert_obj)
        try:
            context.check_privatekey()
        except OpenSSL.SSL.Error:
            SignerConfigError('Certificate public key is not derived from the private key')
