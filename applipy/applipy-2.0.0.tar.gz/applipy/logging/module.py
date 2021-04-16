import logging
from typing import List

from applipy.application.module import Module
from applipy.config.config import Config


class LoggingModule(Module):

    def __init__(self, config: Config):
        self.config = config

    def configure(self, bind, register):
        logging.basicConfig(**self.config.get('logging.config', {}))
        logger = logging.getLogger(self.config.get('app.name'))

        logging_level = self.config.get('logging.level')
        if logging_level:
            logger.setLevel(logging_level)

        def configure_logger(
                handlers: List[logging.Handler]
        ) -> logging.Logger:
            for handler in handlers:
                logger.addHandler(handler)

            return logger

        bind(configure_logger)
