import os.path
import time
import json

from . import Logger

class Config:
    def __init__(self):
        self.logger = Logger.Logger(self.__class__.__name__).getLogger()
        config_file_location = os.getenv('CAS_CONFIG', '/opt/config.json')
        try:
            with open(config_file_location) as config_file:
                try:
                    config = json.load(config_file)
                except Exception as e:
                    raise Exception("Failed to parse config file. {}".format(e))

                if "trigger" not in config or "action" not in config:
                    raise Exception("Failed to parse config file. Missing required trigger or action")

                if len(config["trigger"]) == 0:
                    self.logger.warn("No trigger defined! Please check config file.")

                if len(config["action"]) == 0:
                    self.logger.warn("You have no actions defined. Please check config file.")

                for trigger in config["trigger"]:
                    if "action" not in trigger or len(trigger["action"]) <= 0:
                        self.logger.warn("You have no actions defined in trigger {}."
                                         " Please check config file.".format(trigger["name"]))
                    else:
                        for action in trigger["action"]:
                            if action not in config["action"]:
                                self.logger.warn("Action {} in trigger {} is not defined."
                                                 " Please check config file.".format(action, trigger["name"]))

                self.config = config
        except OSError:
            raise Exception("Can't open config file. Please check mount point")
        self.logger.info("Successfully loaded config.json")
        self.logger.info("Config file last modified: {}".format(time.ctime(os.path.getmtime(config_file_location))))
        if "version" in self.config:
            self.logger.info("Config file version: {}".format(self.config["version"]))
        else:
            self.logger.info("Config file version: No version key found")

    def getConfig(self):
        return self.config
