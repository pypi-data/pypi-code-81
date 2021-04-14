from .Outcome import Outcome


class Success(Outcome):
    def __init__(self, data: dict):
        self.__data = data

    def get_data(self):
        return self.__data
