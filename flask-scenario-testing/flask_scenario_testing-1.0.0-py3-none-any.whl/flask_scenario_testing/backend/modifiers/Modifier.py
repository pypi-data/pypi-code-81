import abc


class Modifier(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def identifier(self):
        pass

    @abc.abstractmethod
    def modify(self, fun, endpoint_name, args):
        pass
