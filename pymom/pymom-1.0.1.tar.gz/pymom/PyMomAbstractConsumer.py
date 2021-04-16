#!/usr/bin/env python3

import sys
from abc import ABC, abstractmethod

# This is the abstract base class with the method that must be
# implemented to register a listener with the PyMom framework.

class PyMomAbstractConsumer(ABC):
    @abstractmethod
    def on_message(self,message):
        """
        This method is called when a message is received from Kafka.  The
        message will be in JSON format.  This method must return True if
        the message is processed successfully or False if the processing
        fails.
        """
        pass

