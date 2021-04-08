"""Aracnid Logger class module.

Note:
    To find pesky log messages from imported modules, run this code from the
    main module:

    loggerlist = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    print(loggerlist)
"""
import json
import logging
import logging.config
import os
import sys

# initialize module variables
NOTSET = logging.NOTSET
DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL

LOGGING_CONFIG_FILE_DEFAULT = 'logging_config.json'
LOGGING_FORMATTER_DEFAULT = 'default'

class Logger:
    """Provides a customized logger.

    If the configuration directory is not specified, the logging
    configuration file must be in the command directory,
    the same as the main calling application/function.

    Environment Variables:
        LOGGING_CONFIG_FILE: The name (and maybe relative path) of the
            logging configuration file.
        LOGGING_CONFIG_DIR: The directory that contains the logging
            configuration file.
        LOGGING_FORMATTER: Selected formatter specified in the config file.

    Attributes:
        logging_path: Full path to the logging configuration file.
        logging_dir: Directory containing the logging configuration file.
        logging_filename: Filename of the logging configuration file.
        formatter: Name of the formatter in use.
        logger: Python logger object.
    """
    def __init__(self, name, config_filename=None, config_dir=None, formatter=None):
        """Initializes the logger.

        Args:
            name: Name of the calling module.
            config_filename: Filename of the logging configuration file.
            config_dir: Directory containing the logging configuration file.
            formatter: Name of the formatter to use, specified in the logging
                configuration file.
        """

        if name == '__main__':
            # set the logging config filename
            self.set_logging_config_filename(config_filename)

            # set the logging config directory
            self.set_logging_config_dir(config_dir)

            # set the logging formatter
            self.set_logging_formatter(formatter)

            # read the config file
            self.logging_path = os.path.join(
                self.logging_dir,
                self.logging_filename)
            with open(self.logging_path, 'rt') as file:
                logging_config = json.load(file)

            # update the formatter
            logging_config['handlers']['console']['formatter'] = self.formatter

            # load the logger configuration
            logging.config.dictConfig(logging_config)

            # set the logger
            self.logger = logging.getLogger()

        else:
            self.logger = logging.getLogger(name)

    def set_logging_config_filename(self, config_filename=None):
        """Sets the configuration filename attribute.

        Args:
            config_filename: The configuration filename.
        """
        # set the filename from the argument
        self.logging_filename = config_filename

        # set the filename from the environment
        if not self.logging_filename:
            self.logging_filename = os.environ.get('LOGGING_CONFIG_FILE')

        # use default config filename
        if not self.logging_filename:
            self.logging_filename = LOGGING_CONFIG_FILE_DEFAULT

    def set_logging_config_dir(self, config_dir=None):
        """Sets the configuration directory attribute.

        Args:
            config_dir: The directory that contains the configuration file.
        """
        # set the dir from the argument
        self.logging_dir = config_dir

        # set the dir from the environment
        if not self.logging_dir:
            self.logging_dir = os.environ.get('LOGGING_CONFIG_DIR')

        # use default config dir
        if not self.logging_dir:
            command_dir = os.path.dirname(sys.argv[0])
            self.logging_dir = os.path.join(os.getcwd(), command_dir)

    def set_logging_formatter(self, formatter=None):
        """Sets the logging formatter attribute.

        Args:
            formatter: Name of the formatter to use, specified in the logging
                configuration file.
        """
        # set the formatter from the argument
        self.formatter = formatter

        # set the formatter from the environment
        if not self.formatter:
            self.formatter = os.environ.get('LOGGING_FORMATTER')

        # use default formatter
        if not self.formatter:
            self.formatter = LOGGING_FORMATTER_DEFAULT

    def get_logger(self):
        """Returns the python logger object.
        """
        return self.logger
