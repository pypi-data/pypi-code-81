#!/usr/bin/env python3
import logging.config
import os
import sys
import multiprocessing
from os import path
from pathlib import Path

from pykafka import KafkaClient
from pymom.PyMomConfig import PyMomConfig
from pymom.PyMomProducer import PyMomProducer
from pymom.PyMomConsumer import PyMomConsumer
from pymom.PyMomError import PyMomError

# This is the framework for communicating with Kafka.  It encapsulates
# the logic of connecting to Kafka, consuming messages, and producing
# messages.  Clients register to receive messages with a class that
# derives from PyMomAbstractConsumer.

# Get the logger specified in the file
log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logger.config')
logging.config.fileConfig(fname=log_file_path, disable_existing_loggers=True)
logger = logging.getLogger("PyMom")


class PyMom:
    """ PyMom encapsulates the logic for interacting with Kafka. """

    def __init__(self):
        try:
            self.config = PyMomConfig()
        except Exception as error:
            raise PyMomError("Configuration error:  {}".format(error))
        
        self.consumers = list()

    def bootstrap_brokers(self):
        return self.config.bootstrap_brokers()

    def producer(self,topic_name):
        """ Return a PyMomProducer for the specified topic. """
        return PyMomProducer(self.config.bootstrap_brokers(),topic_name)

    def register(self,consumer,consumer_group,topic_name):
        """
        Register an object that inherits from PyMomAbstractConsumer to
        receive messages from Kafka.
        """
        self.consumers.append(PyMomConsumer(self.config.bootstrap_brokers(),
                                            consumer,
                                            consumer_group,
                                            topic_name))

    def run(self):
        if len(self.consumers) > 1:
            processes = list()
            for consumer in self.consumers:
                process = multiprocessing.Process(target=lambda: consumer.run())
                process.start()
                processes.append(process)
            for process in processes:
                count = 0
                process.join()
                count += 1
                logger.info("PyMom:  Process complete, {} remaining."
                      .format(len(processes) - count))
        elif len(self.consumers) == 1:
            logger.info("PyMom:  running a single consumer.")
            self.consumers[0].run()
        else:
            logger.error('"No consumers registered."')
            raise PyMomError("No consumers registered.")

