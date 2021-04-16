#!/usr/bin/env python3

import sys
import logging
from pymom.PyMomAbstractConsumer import PyMomAbstractConsumer
from pymom.PyMomRecoverableError import PyMomRecoverableError
from pymom.PyMomUnrecoverableError import PyMomUnrecoverableError
from pymom.PyMom import PyMom

# This class is an example of how to use PyMom to monitor topics.  It
# listens for messages on the specified topic and writes them out, just
# like the Kafka command line consumer.

class PyMomMonitor(PyMomAbstractConsumer):
    """ PyMomMonitor is a PyMom handler for topic monitoring. """

    def __init__(self):
        self.logger = logging.getLogger('PyMom')

    def on_message(self,message):
        """ Process messages. """
        id = message['id']
        payload = message['payload']
        self.logger.info("Received message:  ({}) {}".format(id,payload))


if __name__ == "__main__":
    if len(sys.argv) == 3:
        monitor = PyMomMonitor()
        pymom = PyMom()
        
        pymom.register(handler,sys.argv[1],sys.argv[2])

        print("Monitoring topic {} with consumer group {}."
              .format(sys.argv[1],sys.argv[2]))
        pymom.run()
    
        print("PyMomMonitor terminated.")
    else:
        print("Usage:  " + sys.argv[0] + " <topic-name> <consumer-group>")

    sys.exit(0)
