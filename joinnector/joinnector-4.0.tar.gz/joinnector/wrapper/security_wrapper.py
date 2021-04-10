# pylint: disable=attribute-defined-outside-init

from joinnector.client.security_client import SecurityClient


class SecurityWrapper(object):
    def init(self):
        self.process_common_wrapper()

    def process_common_wrapper(self):
        self.security_client = SecurityClient()

    def get_wrapper(self):
        return self.security_client


sucurity_wrapper = SecurityWrapper()
