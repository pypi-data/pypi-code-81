import logging
import uuid

from ninjarpc import CallHandler, RemoteCommand
from ninjarpc.Exceptions import CallTimeoutException


logger = logging.getLogger(__name__)


class Client:

    def __init__(self, queue_manager, encoder, timeout=60):
        self.queue_manager = queue_manager
        self.queue_manager.connect()
        self.encoder = encoder
        self.client_id = str(uuid.uuid4())
        self.results = dict()
        self.timeout = timeout
        self.ongoing_calls = dict()

    def async_call(self, service_name, method_name, parameters=()):
        queue_name = "{}_{}".format(service_name, method_name)
        response_queue_name = "{}_{}".format(queue_name, self.client_id)
        command = RemoteCommand(service_name, method_name, parameters, response_queue_name)
        message = self.encoder.encode(command)
        # command
        self.queue_manager.init_service_queue(queue_name)

        self.queue_manager.publish(queue_name, message)

        logger.info("{} message published to queue {}".format(message, queue_name))

        self.queue_manager.set_listening_queues([response_queue_name])
        self.queue_manager.init_response_consumption()

        call = CallHandler(self, command, self.timeout)
        self.ongoing_calls[command.correlation_id] = call

        return call

    def wait(self):
        result = None
        while result is None:
            self.queue_manager.wait_with_timeout()
            self.check_timeouts()
            next_message = self.queue_manager.get_next()

            if next_message is not None:
                result = self.encoder.decode(next_message)
                self.results[result.correlation_id] = result
                del self.ongoing_calls[result.correlation_id]

        while self.queue_manager.get_next() is not None:
            logger.info(self.queue_manager.get_next())
            self.results[result.correlation_id] = result
            del self.ongoing_calls[result.correlation_id]

        return

    def is_result_arrived(self, correlation_id):
        if self.results.get(correlation_id) is None:
            return False
        else:
            return True

    def get_result(self, correlation_id):
        try:
            return self.results[correlation_id]
        except KeyError:
            return None

    def check_timeouts(self):
        if len(self.ongoing_calls) == 0:
            return

        for call in self.ongoing_calls.values():
            if call.is_timeouted():
                raise CallTimeoutException(call)
