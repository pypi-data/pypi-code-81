import os
import pathlib

class LogFile:

    def __init__(self, logs_folder, filename="log"):
        i = 0
        while os.path.exists(os.path.join(logs_folder, "{}{}.csv".format(filename, i))):
            i += 1
        self.__path = pathlib.Path(os.path.join(logs_folder, "{}{}.csv".format(filename, i)))

    @property
    def path(self):
        return str(self.__path)

    def size(self):
        return self.__path.stat().st_size

    def delete(self):
        self.__path.unlink()
