import logging

from pika.exceptions import ConnectionClosed, ConnectionWrongStateError, StreamLostError
from ninjarpc.QueueManagers import QueueManagerInterface

logger = logging.getLogger(__name__)
logging.getLogger("pika").setLevel(logging.WARNING)


def reconnect_on_lost_connection(exceptions=(ConnectionClosed, ConnectionWrongStateError, StreamLostError)):
    """
    Retry after reconnect.
    Retries the decorated function/method after reconnecting if any of the given `exceptions` are thrown
    :param exceptions: tuple of exceptions that trigger the reconnection & retry
    :return:
    """
    def decorator(func):
        def inner(self: QueueManagerInterface, *args, **kwargs):
            try:
                return func(self, *args, *kwargs)
            except exceptions as e:
                logger.error(f'RabbitMQ connection error: {e}')
                self.connect()

            return func(self, *args, *kwargs)
        return inner
    return decorator
