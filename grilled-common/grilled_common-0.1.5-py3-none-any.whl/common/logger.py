from abc import ABC, abstractmethod
import logging


class AbstractLogger(ABC):
    @abstractmethod
    def info(self, msg):
        pass

    @abstractmethod
    def error(self, msg):
        pass

    @abstractmethod
    def debug(self, msg):
        pass

    @abstractmethod
    def warn(self, msg):
        pass

    @abstractmethod
    def exception(self, msg):
        pass


class LoggingLogger(AbstractLogger):
    def __init__(self, module_name=None, **kwargs) -> None:
        logging.basicConfig(
            format="[%(asctime)s][%(levelname)s]: %(message)s",
            level=logging.INFO if not kwargs.get("debug") else logging.DEBUG,
        )
        self.module_name = f"[{module_name}]"

    def info(self, msg):
        if self.module_name is not None:
            msg = " ".join([self.module_name, msg])
        return logging.info(msg)

    def error(self, msg):
        if self.module_name is not None:
            msg = " ".join([self.module_name, msg])
        return logging.error(msg)

    def debug(self, msg):
        if self.module_name is not None:
            msg = " ".join([self.module_name, msg])
        return logging.debug(msg)

    def warn(self, msg):
        if self.module_name is not None:
            msg = " ".join([self.module_name, msg])
        return logging.warn(msg)

    def exception(self, msg):
        if self.module_name is not None:
            msg = " ".join([self.module_name, msg])
        return logging.exception(msg)