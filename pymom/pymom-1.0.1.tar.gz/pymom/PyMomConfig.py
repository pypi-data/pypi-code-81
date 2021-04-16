#!/usr/bin/env python3

import sys
import os
import configparser

# PyMomConfig contains all the logic for retrieving configuration
# information for the PyMom components.  The core purpose is to turn
# configuration data into methods that are guaranteed to return some
# value (the sanity of those values is up to the author of the config
# file).
#
# If only there were a language that treats data as code....

# The constants for PyMom configuration.

KAFKA_BOOTSTRAP_BROKERS = 'kafka-bootstrap-brokers'
ZOOKEEPER_SERVERS = 'zookeeper-servers'
DATADOG_NAMESPACE = 'datadog-namespace'


class PyMomConfig:
    """ PyMomConfig encapsulates all PyMom configuration. """

    CONFIG_FILE_ENV = 'PYMOM_CONFIG_FILE'
    
    def __init__(self,config_file = None):
        if config_file is None:
            try:
                config_file = os.environ[self.CONFIG_FILE_ENV]
            except KeyError:
                config_file = None
                raise

        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.validate()

    def validate(self):
        """ Validate the configuration parameters. """
        DEFAULT_KEYS = {KAFKA_BOOTSTRAP_BROKERS,
                        ZOOKEEPER_SERVERS,
                        DATADOG_NAMESPACE}

        default_keys = set(self.config['DEFAULT'].keys())
        if not len(DEFAULT_KEYS.difference(default_keys)) == 0:
            raise KeyError("Missing one or more configuration values.")

    def bootstrap_brokers(self):
        return self.config['DEFAULT'][KAFKA_BOOTSTRAP_BROKERS]

    def zookeeper_servers(self):
        return self.config['DEFAULT'][ZOOKEEPER_SERVERS]

    def datadog_namespace(self):
        return self.config['DEFAULT'][DATADOG_NAMESPACE]


if __name__ == "__main__":
    if len(sys.argv) <= 2:
        config = None
        if len(sys.argv) == 1:
            config = PyMomConfig()
        else:
            config = PyMomConfig(sys.argv[1])
            
        print("Bootstrap brokers = " + config.bootstrap_brokers())
        print("Zookeeper servers = " + config.zookeeper_servers())
    else:
        print("Usage:  " + sys.argv[0] + " <config-file>")
