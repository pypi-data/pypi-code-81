class ParameterValue:
    def __init__(self, name: str, value: float):
        self.__name = name
        self.__value = value

    def get_name(self):
        return self.__name

    def get_value(self):
        return self.__value
