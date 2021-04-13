"""log helper"""

import logging
from termcolor import colored

fmt = colored('[%(asctime)s]', 'blue') + \
      colored('%(levelname)s:', 'green') + \
      colored('%(message)s', 'white')

logging.basicConfig(level=logging.DEBUG, format=fmt, datefmt="%m-%d %H:%M:%S")

class LoggerWriter:
    _log_file_exists = False

    def __init__(self, filename='log.txt'):
        if LoggerWriter._log_file_exists:
            return
        fHandler = logging.FileHandler(filename, mode="w")
        fmt = '[%(asctime)s] %(levelname)s: %(message)s'
        formatter = logging.Formatter(fmt, datefmt="%y-%m-%d %H:%M:%S")
        fHandler.setLevel(logging.DEBUG)
        fHandler.setFormatter(formatter)
        logging.getLogger().addHandler(fHandler)
        LoggerWriter._log_file_exists = True

def log(*args):
    msglist = ["{}".format(x) for x in args]
    return ' '.join(msglist)

def LOG_DEBUG(*args):
    logging.debug(log(*args))

def LOG_INFO(*args):
    logging.info(log(*args))

def LOG_WARNING(*args):
    logging.warning(log(*args))

def LOG_ERROR(*args):
    logging.error(log(*args))
