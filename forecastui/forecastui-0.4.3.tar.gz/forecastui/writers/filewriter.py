import csv
from .writer import AbstractWriter


class FileWriter(AbstractWriter):

    def __init__(self, logfile):
        self.__logFile = logfile
        self.__stream = None
        self.__writer = None

    def __enter__(self):
        if self.open():
            return self
        raise RuntimeError

    def __exit__(self, *exc):
        self.close()

    def open(self):
        self.__stream = open(self.__logFile.path, mode='w', newline='\n', encoding='utf-8')
        self.__writer = csv.writer(self.__stream, delimiter=',')
        return self.__stream and self.__writer

    def close(self):
        if self.__stream is None:
            return False
        self.__stream.close()
        return True

    def write(self, row):
        self.__writer.writerow(row)

    def writerows(self, rows):
        self.__writer.writerows(rows)
