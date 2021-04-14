from threading import Thread
from time import sleep
import configparser
import logging
from pathlib import Path
from os import getcwd


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class LogLevelUpdater(metaclass=Singleton):
    def __init__(self):
        self.loggers = []
        self.threads = []
        self.create_thread = False
        self.log_levels = {'info': logging.INFO, 'debug': logging.DEBUG, "error": logging.ERROR,
                           'critical': logging.CRITICAL, 'warning': logging.WARNING}
        self.config_file = str(self.findConfigFileInPath())
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)
        self.filelevel = self.config["Default"].get("filelevel", '').lower().strip() or 'debug'
        self.channellevel = self.config["Default"].get("channellevel", '').lower().strip() or 'info'
        self.saveJson = None
        self.getSaveJson()

    @staticmethod
    def findConfigFileInPath():
        lConfigFilename = "run_setting.ini"
        lConfigPath = Path(getcwd()).joinpath(lConfigFilename)
        if lConfigPath.exists():
            return lConfigPath

        lConfigPath = Path(getcwd()).parent.joinpath(lConfigFilename)
        if lConfigPath.exists():
            return lConfigPath

        print(f"Error: Can't locate run_setting.ini in {getcwd()} or parent folder. Please check working directory of "
              f"this python instance. should be /fasifu/ or /fasifu/tests.")

    def updateLogLevel(self):
        for logger in self.loggers:
            for handler in logger.handlers:
                if isinstance(handler, logging.FileHandler):
                    handler.setLevel(self.log_levels[self.filelevel])
                elif isinstance(handler, logging.StreamHandler):
                    handler.setLevel(self.log_levels[self.channellevel])
            logger.propogate = False
        print("File log level:", self.filelevel)
        print("Channel log level:", self.channellevel)

    def checkAndUpdateLogLevel(self):
        while True:
            sleep(60)
            self.config.read(self.config_file)
            new_filelevel = self.config["Default"].get("filelevel", '').lower().strip() or 'info'
            new_channellevel = self.config["Default"].get("channellevel", '').lower().strip() or 'info'
            if not new_channellevel == self.channellevel and not new_filelevel == self.filelevel:
                self.channellevel = new_channellevel
                self.filelevel = new_filelevel
                self.updateLogLevel()

            self.getSaveJson()

    def getSaveJson(self):
        # Reading and updating json flag
        self.saveJson = self.config["Default"].get("saveJson") or False
        if self.saveJson.lower().strip() == 'true':
            self.saveJson = True
        else:
            self.saveJson = False

    def startThread(self):
        self.updateLogLevel()
        if not self.threads and self.create_thread:
            t = Thread(target=self.checkAndUpdateLogLevel)
            t.daemon = True
            t.start()
            self.threads.append(t)
