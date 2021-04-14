import json
import logging
import sys

from .RequestIdProvider import RequestIdProvider


class Logger(logging.LoggerAdapter):
    def __init__(
        self,
        request_id_provider: RequestIdProvider,
        channel="socrates-api",
        api_version="",
        stream=sys.stdout,
    ):
        logger = logging.getLogger(channel)
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(stream)
        handler.setLevel(logging.INFO)
        format = "[%(asctime)s] %(name)s.%(levelname)s: %(message)s"
        dateformat = "%Y-%m-%dT%H:%M:%S%z"
        formatter = logging.Formatter(fmt=format, datefmt=dateformat)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        self.__request_id_provider = request_id_provider
        self.__api_version = api_version

        super().__init__(logger, {})

    def process(self, msg, kwargs):
        data = {"data": kwargs, "meta": self.__get_meta()}

        # ensure single line log
        msg = msg.replace("\r", "\\r").replace("\n", "\\n")

        msg += " " + json.dumps(data)

        return msg, {}

    def __get_meta(self):
        return {
            "requestId": self.__request_id_provider.get_request_id(),
            "apiVersion": self.__api_version,
        }
