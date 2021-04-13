import datetime
import os
import platform


class Logger:

    def __init__(self, logger):
        self.logger = logger

    def emit(self, msg, app_label):
        message = self.__enrichlog("INFO", msg)
        response = self.__send(app_label, message)
        return {"emit": response,
                "message": message}

    @staticmethod
    def __enrichlog(level_code, msg):
        return {
            "uname": list(platform.uname()),
            "python": platform.python_version(),
            "pid": os.getpid(),
            "level_code": level_code,
            "msg": msg,
            "timestamp": str(datetime.datetime.now()),
        }

    def __send(self, label, msg):
        return str(self.logger.emit(label, msg)).lower()
