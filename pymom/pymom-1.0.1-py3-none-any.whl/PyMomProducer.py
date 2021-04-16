#!/usr/bin/env python3

import datetime
from pykafka import KafkaClient
from pymom.PyMomMessage import PyMomMessage
from pymom.PyMomError import PyMomError

# This is a wrapper for a Kafka producer.  It encapsulates the logic of
# connecting to Kafka and producing messages.


class PyMomProducer:
    """ PyMomProducer encapsulates the logic for producing Kafka messages. """

    def __init__(self,bootstrap_brokers,topic_name):
        self.bootstrap_brokers = bootstrap_brokers
        self.topic_name = topic_name
        self.message = PyMomMessage(topic_name)
        self.producer = None

    def connect(self):
        """
        Connect to Kafka.  It's important to separate this functionality
        from the init method to ensure that it works when forked to a new
        process.
        """
        client = KafkaClient(hosts=self.bootstrap_brokers)
        topic = client.topics[self.topic_name]

        self.producer = topic.get_producer(linger_ms=0,sync=True)

    def write(self,id,payload):
        if self.producer is None:
            self.connect()

        try:
            key, message = self.message.wrap(payload,id)
            self.producer.produce(message,key,timestamp=datetime.datetime.now())
        except Exception as error:
            raise PyMomError("Unable to write message:  ({}) {} ({})"
                             .format(msg_id, payload, error))
