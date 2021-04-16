#!/usr/bin/env python3
import logging.config
import json
from os import path

from pykafka import KafkaClient
from pymom.PyMomRecoverableError import PyMomRecoverableError
from pymom.PyMomUnrecoverableError import PyMomUnrecoverableError

# Get the logger specified
log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logger.config')
logging.config.fileConfig(fname=log_file_path, disable_existing_loggers=True)
logger = logging.getLogger("PyMomConsumer")

# This is a wrapper for a Kafka consumer.  It encapsulates the logic of
# connecting to Kafka and consuming messages.

class PyMomConsumer:
    """ PyMomConsumer encapsulates the logic for consuming Kafka messages. """

    def __init__(self, bootstrap_brokers, consumer, consumer_group, topic_name):
        self.bootstrap_brokers = bootstrap_brokers
        self.consumer = consumer
        self.consumer_group = consumer_group
        self.topic_name = topic_name
        self.kafka_consumer = None
        self.messages_processed = 0

    def connect(self):
        """
        Connect to Kafka.  It's important to separate this functionality
        from the init method to ensure that it works when forked to a new
        process.
        """
        client = KafkaClient(hosts=self.bootstrap_brokers)
        topic = client.topics[self.topic_name]

        self.kafka_consumer \
            = topic.get_balanced_consumer(self.consumer_group,
                                          managed=True,
                                          auto_commit_enable=False,
                                          auto_start=True,
                                          reset_offset_on_start=False)

    def reset_connection(self):
        """ Try to reset the connection. """
        reset = False
        try:
            self.kafka_consumer.stop()
            self.kafka_consumer.start()
            reset = True
        except Exception as e:
            logger.error("Error resetting connection:  {}".format(e))

        return reset

    def extract_content(self, message):
        """ Get the content out of the JSON message. """
        content = None
        try:
            content = json.loads(message.value.decode('utf-8'))
        except Exception as e:
            logger.error("Error decoding message ({}):  {}".format(message, e))

        return content

    def process_message(self, content):
        """ Process the message content. """
        success = True

        try:
            logger.info("PyMom calling on_message...")
            self.consumer.on_message(content)

            logger.info("PyMom on_message completed.")
            self.kafka_consumer.commit_offsets()
        except PyMomRecoverableError as recoverable:
            logger.warning("Recoverable error:  {}".format(recoverable))
            # Offset explicitly not committed to allow retry.
        except PyMomUnrecoverableError as unrecoverable:
            logger.error("Unrecoverable error:  {}".format(unrecoverable))
            self.kafka_consumer.commit_offsets()
        except Exception as error:
            logger.error("Unknown error:  {} on message {}"
                         .format(error, content))
            success = False
            # Offset explicitly not committed, likely client error.

        return success

    def listen(self):
        """ Listen for messages. """
        self.messages_processed = 0

        # The infinite loop to continue reading Kafka Msgs off the Bus
        # If this loop breaks, then we will not be reading msgs anymore
        for message in self.kafka_consumer:
            if message is not None:
                logger.info("PyMom message received.")

                content = self.extract_content(message)
                if content is not None:
                    logger.info("PyMom message content extracted")

                    if self.process_message(content):
                        self.messages_processed += 1

                        logger.info("PyMom message processed")
                    else:
                        logger.warning("PyMom message failed to process:  {}"
                                       .format(message))

                        # Need to make sure we don't have infinite loops
                        # for msgs - Fail, commit, and move on
                        self.kafka_consumer.commit_offsets()
                else:
                    logger.warning("Unable to parse content from message:  {}"
                                   .format(message))

                    # Need to make sure we don't have infinite loops for
                    # msgs - Fail, commit, and move on
                    self.kafka_consumer.commit_offsets()

    def run(self):
        """ Call the listen method and handle errors where possible. """
        self.connect()
        # TODO: Need to discuss the infinite loop - Maybe we shouldn't
        # fail all the time?
        # TODO: Maybe we will want to fail after so many msgs failed?
        while True:
            try:
                logger.info("PyMom listening...")
                self.listen()
            except Exception as e:
                logger.error("PyMom unknown consumer error:  {}".format(e))

            if self.reset_connection():
                logger.info("PyMom connection reset.")
            else:
                logger.info("PyMom unable to reset connection, reconnecting.")
                self.connect()
