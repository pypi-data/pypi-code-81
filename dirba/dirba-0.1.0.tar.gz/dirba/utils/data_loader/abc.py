import logging
from abc import abstractmethod, ABC
from typing import Tuple, TypeVar, Any, Type
from urllib import parse as url_parse

import pydantic
import requests
from requests import Response
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from dirba.utils.data_loader.exceptions import DataLoadException

ContentUrl = str
Content = TypeVar('Content')

SerializedContent = TypeVar('SerializedContent', bound=pydantic.BaseModel)


class AbstractDataLoader(ABC):
    """
    Заготовка для получения содержимого из сервиса данных
    """

    def __init__(self, service_url: str, timeout: float = 10.0):
        """
        Создание коннектора

        ссылка вида https://dataservice/api/v1/
        :param service_url: ссылка на сервис без указания сущности
        :param timeout: максимальное время ожидания запроса
        """
        self.timeout = timeout
        self.service_url = service_url

        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "OPTIONS"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session = requests.Session()
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def entity(self) -> str:
        """
        Название сущности
        """
        pass

    def build_url(self, entity_id: int) -> str:
        entity_url = url_parse.urljoin(self.service_url, self.entity())
        return entity_url + f'/{entity_id}'

    def load(self, entity_id: int) -> Tuple[Response, ContentUrl]:
        """
        Получение данных по запросу
        :param entity_id: идентификатор сущности
        :return:
        """
        url = self.build_url(entity_id=entity_id)
        try:
            response = self.session.get(url, timeout=self.timeout)
            return response, url
        except Exception as e:
            self.logger.error('failed to load data', extra={'data_id': entity_id,
                                                            'entity': self.entity(),
                                                            'result_url': url,
                                                            'with_timeout': self.timeout})
            raise DataLoadException(str(e)) from e

    @abstractmethod
    def extract_data(self, data_service_response: Response, url: ContentUrl) -> Any:
        """
        Извлекает данные из ответа от сервиса
        :param data_service_response: request.Response объект
        :param url: ссылка, по которой был выполнен запрос
        :return: данные сущности
        """
        pass

    def get_content(self, entity_id: int) -> Tuple[ContentUrl, Content]:
        """
        Получение содержимого сущности
        :param entity_id: id сущности
        :return:
        """
        response, url = self.load(entity_id)
        data = self.extract_data(response, url)
        return url, data

    def _extract_data_by_schema(self, response: Response, schema: Type[SerializedContent]) -> SerializedContent:
        """
        Извлечение данных из ответа сервиса в соответствии с схемой
        :param response: ответ от сервиса
        :param schema: схема для сериализации
        :return:
        """
        try:
            data = schema(**response.json())

            return data
        except pydantic.ValidationError as e:
            self.logger.error('incorrect data from service', extra={
                'response_data': response.content,
                'response_url': response.url,
                'response_status': response.status_code
            })
            raise ValueError("Incorrect data from service") from e
