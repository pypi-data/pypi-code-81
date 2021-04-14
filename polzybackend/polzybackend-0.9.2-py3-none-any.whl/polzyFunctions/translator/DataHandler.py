import os
import json
import codecs
import threading
from polzyFunctions.GlobalConstants import GlobalConstants
from logging import getLogger

logger = getLogger(GlobalConstants.loggerName)
lock = threading.Lock()  # to make class thread safe


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Data(metaclass=Singleton):
    """
    This is class is used to store language data. It was made to enhance performance.
    This is a singleton and thread safe class, because of this it loads json file
    only when the class is first initiated, later all the time it returns the same data.
    This also means that any changes made on language_data.json on runtime will not affect the program until restart.
    """
    def __init__(self):
        logger.debug("Language translation backend module initialized - buffered")
        self.data = self.get_data(os.path.join(os.path.dirname(os.path.abspath(__file__)), "language_data.json"))

    @staticmethod
    def get_data(fileNameAndPath):
        with codecs.open(fileNameAndPath, 'r') as file:
            data = json.load(file)
        return data
