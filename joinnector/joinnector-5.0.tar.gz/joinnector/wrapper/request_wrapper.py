# pylint: disable=attribute-defined-outside-init

from joinnector.client.request_client import RequestClient


class RequestWrapper(object):
    def init(self, key, secret, mode):
        self.process_common_wrapper(key, secret, mode)

    def process_common_wrapper(self, key, secret, mode):
        self.request_client = RequestClient(
            key=key, secret=secret, mode=mode)

    def get_wrapper(self):
        return self.request_client


request_wrapper = RequestWrapper()
