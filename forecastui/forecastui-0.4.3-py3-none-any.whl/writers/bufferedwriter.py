import csv
from threading import Thread, Lock
from .writer import AbstractWriter

class BufferedWriter(AbstractWriter):

    def __init__(self, pathToFile):
        self.__buffer = []
        self.__mutex = Lock()
        self.__path = pathToFile
        self.__stream = None
        self.__writer = None

    def __enter__(self):
        return self.open()

    def __exit__(self, *exc):
        self.close()

    def open(self):
        self.__stream = open(self.__path, mode='w', newline='\n', encoding='utf-8')
        self.__writer = csv.writer(self.__stream, delimiter=',')
        return self

    def close(self):
        if self.__stream is None:
            return False
        self.__write()
        self.__stream.close()
        return True

    def write(self, row):
        self.__mutex.acquire(blocking=True)
        try:
            self.__buffer.append(row)
        finally:
            self.__mutex.release()

    def writerows(self, rows):
        self.__mutex.acquire(blocking=True)
        try:
            self.__buffer.extend(rows)
        finally:
            self.__mutex.release()

    def __write(self):
        self.__mutex.acquire(blocking=True)
        try:
            self.__writer.writerows(self.__buffer)
            self.__buffer.clear()
        finally:
            self.__mutex.release()
