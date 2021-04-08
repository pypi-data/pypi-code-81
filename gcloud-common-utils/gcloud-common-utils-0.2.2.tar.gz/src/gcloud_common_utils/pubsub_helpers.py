import logging
import signal
from typing import Callable

from google.api_core.exceptions import DeadlineExceeded
from google.cloud.pubsub_v1 import SubscriberClient
from nivacloud_logging.log_utils import LogContext, generate_trace_id


class SigHandler:
    def __init__(self):
        self.running = True
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        logging.info("Received stop signal, set 'running' to false", extra={'signum': signum, 'frame': frame})
        self.running = False


def _create_message_ack_fn(subscriber: SubscriberClient, subscription_path: str, ack_id: str) -> Callable:
    def ack_message():
        logging.info("Acking message", extra={"ack_id": ack_id})
        subscriber.acknowledge(subscription_path, [ack_id])

    return ack_message


def _pull_and_handle_message(subscriber, subscription_path, message_handler):
    """Pulls one message and calls the message handler, Return whether this subscription is currently doing work"""
    response = subscriber.pull(subscription=subscription_path, max_messages=1, timeout=2)
    if not response or len(response.received_messages) == 0:
        raise DeadlineExceeded('Raising DeadlineExceeded to emulate cloud pubsub behaviour '
                               'from local pubsub emulator')
    received_message = response.received_messages[0]
    # creating the ack callback with ack_id as a function scoped variable
    ack_callback = _create_message_ack_fn(subscriber, subscription_path, received_message.ack_id)
    message_handler(received_message.message, ack_callback)


def subscribe_synchronously(project_id: str, subscription_name: str, callback: Callable):
    """
    Creates a pubsub synchronous subscription function for a given project_id and subscription name.

    Example usage:

    def message_handler(message, ack_callback):
        # do something with message

        # acknowledge message when done
        ack_callback()

    subscription_name = f"signals2tsb-{environment}-{signal_list_topic}"
    subscribe_synchronously(project_id=project_id, subscription_name=subscription_name, callback=message_handler)
    """
    sig_handler = SigHandler()
    subscriber = SubscriberClient()
    subscription_path = subscriber.subscription_path(project=project_id, subscription=subscription_name)

    def subscribe(message_handler: Callable):
        while sig_handler.running:
            with LogContext(trace_id=generate_trace_id()):
                try:
                    _pull_and_handle_message(subscriber, subscription_path, message_handler)
                except DeadlineExceeded:
                    logging.debug("Received deadline exceeded event when polling, this is expected if no messages")
                    pass

    with LogContext(subscription_path=subscription_path):
        logging.info("Set up subscription")
        # subscribing to events, one message at a time
        subscribe(callback)
