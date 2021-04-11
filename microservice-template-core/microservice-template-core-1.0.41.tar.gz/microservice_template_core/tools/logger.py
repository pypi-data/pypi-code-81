import logging
import datetime
from microservice_template_core.settings import LoggerConfig, ServiceConfig
import logging_loki
from multiprocessing import Queue

logger = None


class VerboseFilter(logging.Filter):

    def filter(self, record: logging.LogRecord) -> bool:
        if not hasattr(record, 'traceback'):
            record.traceback = ""
        return True


class VerboseFormatter(logging.Formatter):

    def formatMessage(self, record: logging.LogRecord) -> str:
        base_message = f'{datetime.datetime.now()} - {record.name} - {record.levelname} - {record.message}'
        if hasattr(record, 'exception'):
            base_message = base_message + f'\nException: {getattr(record, "exception")}'
        if hasattr(record, 'traceback'):
            base_message = base_message + f'\nTraceback: {getattr(record, "traceback")}'

        return base_message


def get_logger():
    global logger
    if not logger:
        logger = logging.getLogger(ServiceConfig.SERVICE_NAME)
        logger.setLevel(LoggerConfig.LOG_LEVEL)
        log_format = logging.Formatter('[%(levelname)s] - %(message)s')

        loki_handler = logging_loki.LokiQueueHandler(
            Queue(-1),
            url=f"http://{LoggerConfig.LOKI_SERVER}:{LoggerConfig.LOKI_PORT}/loki/api/v1/push",
            tags={"service": ServiceConfig.SERVICE_NAME},
            version="1",
        )
        loki_handler.setFormatter(log_format)

        console_handler = logging.StreamHandler()

        logger.addHandler(loki_handler)
        logger.addHandler(console_handler)

    return logger

