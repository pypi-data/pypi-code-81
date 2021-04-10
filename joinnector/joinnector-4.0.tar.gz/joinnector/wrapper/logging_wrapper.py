# pylint: disable=attribute-defined-outside-init

from joinnector.client.logging_client import LoggingClient


class LoggingWrapper(object):
    def init(self):
        self.process_common_wrapper()

    def process_common_wrapper(self):
        self.logging_client = LoggingClient()

    def get_wrapper(self):
        return self.logging_client


logging_wrapper = LoggingWrapper()
