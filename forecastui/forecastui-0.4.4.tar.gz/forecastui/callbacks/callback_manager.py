import requests
from ..utility import Store

class CallbackManager:

    def __init__(self, callback):
        self.__callback = callback
        self.__history = {}
        self.current_index = 0

    def __call__(self, parameter):
        parameter = parameter.rstrip("\x00 ")
        value = self.__callback(parameter)
        if isinstance(value, list):
            index = min(len(value)-1, self.current_index)
            value = value[index]
        self.__register(parameter, value)
        return value

    def unlock(self, value):
        self.__callback.unlock(value)

    def stop(self):
        self.unlock(None)

    def __register(self, parameter_string, value):

        parameter = parameter_string.lower()
        splitted = parameter.split()

        d = self.__history

        while len(splitted) > 1:
            key = splitted.pop(0)
            if key not in d.keys():
                d[key] = {}
            d = d[key]

        last_key = splitted.pop(0)
        if isinstance(d.get(last_key), list):
            d[last_key].append(value)
        else:
            d[last_key] = []
            d[last_key].append(value)
        print("Set {} with value {}".format(parameter_string, value))
        requests.get("http://127.0.0.1:{}".format(Store.port) + '/api/board/parameter', params={"name": parameter_string, "value": value})

    def getHistory(self):
        return self.__history