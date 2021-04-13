import abc


class QueueManagerInterface(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def connect(self):
        pass

    @abc.abstractmethod
    def disconnect(self):
        pass

    @abc.abstractmethod
    def publish(self, queue_name, message):
        pass

    @abc.abstractmethod
    def get_next(self):
        pass

    @abc.abstractmethod
    def wait_with_timeout(self):
        pass

    @abc.abstractmethod
    def init_service_queue(self, queue_name):
        pass

    @abc.abstractmethod
    def init_response_queue(self, queue_name):
        pass

    @abc.abstractmethod
    def init_service_consumption(self):
        pass

    @abc.abstractmethod
    def init_response_consumption(self):
        pass

    @abc.abstractmethod
    def set_listening_queues(self, queue_names):
        pass
