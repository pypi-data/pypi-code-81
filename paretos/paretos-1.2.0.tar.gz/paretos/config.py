from logging import Logger, LoggerAdapter
from typing import Optional, Union

from .DefaultLogger import DefaultLogger
from .exceptions import ConfigError
from .socrates.url_validator import is_valid_url


class Config(object):
    def __init__(
        self,
        customer_token: str = "",
        data_source_name: str = "sqlite:///paretos.sqlite3",
        socrates_url: str = "https://api.paretos.io/socrates/",
        logger: Optional[Union[Logger, LoggerAdapter]] = None,
        dashboard_host: str = "127.0.0.1",
        dashboard_port: str = "8080",
    ):
        self.__customer_token = customer_token
        self.__data_source_name = data_source_name
        self.__socrates_url = None
        self.__dashboard_host = dashboard_host
        self.__dashboard_port = dashboard_port

        self.__set_socrates_url(socrates_url)
        self.__logger = logger or DefaultLogger()

    def get_customer_token(self) -> str:
        return self.__customer_token

    def get_data_source_name(self) -> str:
        return self.__data_source_name

    def __set_socrates_url(self, api_url: str):
        if not is_valid_url(api_url):
            raise ConfigError(f"'{api_url}' is not a valid url")

        if api_url[len(api_url) - 1] != "/":
            api_url = api_url + "/"

        self.__socrates_url = api_url

    def get_api_url(self) -> str:
        return self.__socrates_url

    def get_logger(self) -> Logger:
        return self.__logger

    def get_dashboard_host(self) -> str:
        return self.__dashboard_host

    def get_dashboard_port(self) -> str:
        return self.__dashboard_port
