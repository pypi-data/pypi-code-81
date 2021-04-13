from ninjarpc.Helpers.reconnect import reconnect_on_lost_connection
from ninjarpc.QueueManagers import QueueManagerInterface
from pika import BlockingConnection, ConnectionParameters, PlainCredentials
from pika.exceptions import AMQPChannelError, ConnectionClosed

import logging

logger = logging.getLogger(__name__)
logging.getLogger("pika").setLevel(logging.WARNING)


class RabbitMQ(QueueManagerInterface):

    def __init__(self,
                 host="127.0.0.1",
                 port=5672,
                 username="guest",
                 password="guest",
                 vhost="/",
                 heartbeat=0,
                 ):

        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.vhost = vhost
        self.heartbeat = heartbeat
        self.send_connection = None
        self.send_channel = None
        self.recv_connection = None
        self.recv_channel = None
        self.listening_queues = None
        self.arrived_messages = list()
        self.initialized_response_queues = dict()
        self.initialized_service_queues = dict()
        self.service_consumption_initialized = False
        self.response_consumption_initialized = False

    def connect(self):
        self.initialized_response_queues = dict()
        self.initialized_service_queues = dict()

        credentials = PlainCredentials(self.username, self.password)
        parameters = ConnectionParameters(host=self.host, port=self.port,
                                          virtual_host=self.vhost, credentials=credentials,
                                          heartbeat=self.heartbeat)

        self.send_connection = BlockingConnection(parameters=parameters)
        self.send_channel = self.send_connection.channel()

        self.recv_connection = BlockingConnection(parameters=parameters)
        self.recv_channel = self.recv_connection.channel()

        logger.info("RabbitMq connections established.")
        return

    def disconnect(self):
        self.send_channel.close()
        self.send_connection.close()

        self.recv_channel.close()
        self.recv_connection.close()
        return

    def set_listening_queues(self, queue_names):
        self.listening_queues = queue_names
        return

    def init_service_consumption(self):
        if self.listening_queues is None:
            return

        for queue_name in self.listening_queues:
            self.init_service_queue(queue_name)
            self.recv_channel.basic_consume(on_message_callback=self.callback, auto_ack=True, queue=queue_name)
        self.service_consumption_initialized = True

        return

    def init_response_consumption(self):
        if self.listening_queues is None:
            return

        for queue_name in self.listening_queues:
            self.init_response_queue(queue_name)
            self.recv_channel.basic_consume(on_message_callback=self.callback, auto_ack=True, queue=queue_name)

        self.response_consumption_initialized = True
        return

    def callback(self, ch, method, properties, body):

        self.arrived_messages.append(body)
        return

    def wait(self):
        for queue_name in self.listening_queues:
            for method_frame, properties, body in self.recv_channel.consume(queue_name,
                                                                            inactivity_timeout=2,
                                                                            auto_ack=True):

                # Escape out of the loop after inactivity_timeout
                if body is None:
                    break

            # Cancel the consumer and return any pending messages
            self.recv_channel.cancel()
        return

    def wait_with_timeout(self):
        try:
            self.wait()
        except AMQPChannelError as e:
            logger.error("AMQPChannelError with the comsumer. Error message: {}".format(e))

        except ConnectionClosed as e:
            logger.error("Connection closed with the consumer. Error message: {}".format(e))

            self.connect()
            if not self.response_consumption_initialized:
                self.init_response_consumption()
            if not self.service_consumption_initialized:
                self.init_service_consumption()

            self.recv_channel.start_consuming()
        return

    def get_next(self):
        if len(self.arrived_messages) > 0:
            return self.arrived_messages.pop(0)

        return None

    @reconnect_on_lost_connection()
    def publish(self, queue_name, msg):

        self.send_channel.basic_publish(exchange="", routing_key=queue_name, body=msg)

        logger.debug("Message publised to {} queue".format(queue_name))

        return

    @reconnect_on_lost_connection()
    def init_service_queue(self, queue_name):

        if queue_name in self.initialized_service_queues.keys():
            return
        self.send_channel.queue_declare(queue=queue_name, auto_delete=True)
        self.initialized_service_queues[queue_name] = 1
        return

    def init_response_queue(self, queue_name):
        if queue_name in self.initialized_response_queues.keys():
            return
        self.send_channel.queue_declare(queue=queue_name, auto_delete=True, arguments={"x-expires": 60000})
        self.initialized_response_queues[queue_name] = 1
        return
