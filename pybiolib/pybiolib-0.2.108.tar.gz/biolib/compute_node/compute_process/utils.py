import logging
from queue import Queue

from biolib.biolib_binary_format import SystemException

biolib_logger = logging.getLogger('biolib')


class ComputeProcessException(Exception):
    def __init__(self, original_error: Exception, biolib_error_code, messages_to_send_queue: Queue):
        super().__init__()

        system_exception_package = SystemException().serialize(biolib_error_code)
        messages_to_send_queue.put(system_exception_package)

        biolib_logger.error(original_error)
