#!/usr/bin/env python3

import sys
import os
import uuid
import datetime
import json

# This is a convenience class for ensuring standard formatting of
# messages on Kafka.

class PyMomMessage:
    """
    PyMomMessage encapsulates a message written to or read from Kafka in
    a standard format.  It includes some convenience functions for
    creating and manipulating such messages.
    """

    def __init__(self,topic,message_type = None,version = None):
        self.topic = topic
        self.message_type = ''
        if message_type is not None:
            self.message_type = message_type
        self.version = "1.0"
        if version is not None:
            self.version = version

    def wrap(self,payload,id = None):
        """ Wrap the email message in a standard format. """
        if id is None:
            id = str(uuid.uuid4())

        wrapper = dict()
        wrapper['id'] = str(id)
        wrapper['event_type'] = self.event_type
        wrapper['version'] = self.version
        wrapper['timestamp'] = str(datetime.datetime.now())
        wrapper['payload'] = payload

        return (wrapper['id'].encode(encoding='utf-8'),
                json.dumps(wrapper).encode(encoding='utf-8'))


if __name__ == "__main__":
    message = PyMomMessage('pymom.test','test')
    key, wrapped = message.wrap('A test message.')
    print("key = " + str(key))
    print("wrapped message = " + str(wrapped))

    sys.exit(0)
