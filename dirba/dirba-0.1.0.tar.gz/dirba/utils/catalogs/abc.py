import logging
from abc import ABC, abstractmethod
from typing import Dict, TypeVar, Type, Union, NewType, Optional
from urllib import parse as url_parse

import aiohttp.client
import asyncache
import pydantic
import cachetools

import requests

from ..catalogs.exceptions import CatalogException

CatalogValue = TypeVar('CatalogValue', bound=pydantic.BaseModel)
CatalogId = NewType('CatalogId', int)


class AbstractCatalog(ABC):
    """
    Класс для работы с сервисом каталогов

    Особенностью класса является двухуровневый кэш.

    Кэш первого уровня отвечает за получение определённого значения, этот кэш имеет TTL,
    для возможности получения новых категорий при обновлении каталога.

    Кэш второго уровня содержит в себе имеющиеся в каталоге значения
    и он не подлежит обновлению при штатной работе (предполагается,
     что каталоги не изменяют своего содержания, а только добавляют значения)
    """
    CACHE_DURATION = 120

    def __init__(self, catalog_value_class: Type[CatalogValue], catalog_service_url: str):
        """
        Информация о каталоге должна быть представлена в виде
        общего url'a по которому можно запросить информацию по любому каталогу, например,
        http://catalogservice.com/catalogs/ куда будет подставлен ваш каталог
        http://catalogservice.com/catalogs/{catalogname}

        :param catalog_value_class: класс, использующийся для сериализации значений каталога
        :param catalog_service_url: url сервиса каталогов по которому можно получить информацию о каталоге
        """
        self.catalog_service_url = catalog_service_url
        self.catalog_value_class = catalog_value_class
        self.catalog_values: Optional[Dict[CatalogId, CatalogValue]] = dict()
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def catalog_name(self) -> str:
        """
        Получение названия каталога
        """
        pass

    def build_url(self) -> str:
        """
        Сборка запроса на сервис каталогов для запроса значений **текущего** каталога
        """
        return url_parse.urljoin(self.catalog_service_url, self.catalog_name())

    @abstractmethod
    def parse_catalog_response(self, data: Union[dict, list]) -> Dict[CatalogId, CatalogValue]:
        """
        Извлечение значений каталога из ответа сервиса каталогов

        :param data: данные, полученные из json ответа сервиса каталогов
        :return: значения каталогов
        """
        pass

    async def get_catalog_data(self) -> dict:
        """
        Получение данных с сервиса каталогов
        raises: CatalogException: при неудачном запросе
        """
        async with aiohttp.client.ClientSession(timeout=aiohttp.client.ClientTimeout(10)) as session:
            response = await session.get(self.build_url())
            if response.status != 200:
                raise CatalogException(f'Request to catalog service {self.build_url()} '
                                       f'failed with {response.status}')
            data = await response.json()

            return data

    def get_catalog_data_sync(self) -> dict:
        """
        Получение данных с сервиса каталогов в синхронном варианте
        raises: CatalogException: при неудачном запросе
        """
        response = requests.get(self.build_url())
        if response.status_code != 200:
            raise CatalogException(f'Request to catalog service {self.build_url()} '
                                   f'failed with {response.status_code}')
        return response.json()

    async def load_catalog(self) -> Dict[CatalogId, CatalogValue]:
        """
        Подгрузка актуальных значений каталога

        :raises: CatalogException: при невозможности получения значений с каталога
        :return: полученные значения каталога
        """
        try:
            data = await self.get_catalog_data()
            self.catalog_values = self.parse_catalog_response(data)
        except Exception as e:
            raise CatalogException("Failed to load catalog values") from e

        self.logger.debug(f'loaded values from remote catalog. loaded ids: '
                          f'{tuple(self.catalog_values.keys())}')

        return self.catalog_values

    def load_catalog_sync(self) -> Dict[CatalogId, CatalogValue]:
        """
        Подгрузка актуальных значений каталога

        :raises: CatalogException: при невозможности получения значений с каталога
        :return: полученные значения каталога
        """
        try:
            data = self.get_catalog_data_sync()
            self.catalog_values = self.parse_catalog_response(data)
        except Exception as e:
            raise CatalogException("Failed to load catalog values") from e

        self.logger.debug(f'loaded values from remote catalog. loaded ids: '
                          f'{tuple(self.catalog_values.keys())}')

        return self.catalog_values

    @cachetools.cached(cache=cachetools.TTLCache(maxsize=64, ttl=CACHE_DURATION))
    def get_value_sync(self, catalog_id: int) -> Optional[CatalogValue]:
        """
        Получение значения из каталога.

        При отсутствии значения в текущей версии каталога будет предпринята попытка
        повторного получения значений из каталогов
        (чтобы не заливать сервис каталогов запросами, на этой функции висит TTL кэш)

        :param catalog_id: идентификатор значения каталога
        """
        # noinspection PyTypeChecker
        value = self.catalog_values.get(catalog_id)
        if not value:
            try:
                self.logger.debug(f'value with id {catalog_id} not found; attempt to reload catalog')
                self.load_catalog_sync()
            except CatalogException as e:
                self.logger.error(f'failed to get values from catalog', exc_info=True,
                                  extra={'catalog_id': catalog_id, 'catalog_url': self.build_url()})
            # noinspection PyTypeChecker
            return self.catalog_values.get(catalog_id)
        else:
            self.logger.debug(f'value {catalog_id} already loaded get from local')
            return value

    @asyncache.cached(cache=cachetools.TTLCache(maxsize=64, ttl=CACHE_DURATION))
    async def get_value(self, catalog_id: int) -> Optional[CatalogValue]:
        """
        Получение значения из каталога.

        При отсутствии значения в текущей версии каталога будет предпринята попытка
        повторного получения значений из каталогов
        (чтобы не заливать сервис каталогов запросами, на этой функции висит TTL кэш)

        :param catalog_id: идентификатор значения каталога
        """
        # noinspection PyTypeChecker
        value = self.catalog_values.get(catalog_id)
        if not value:
            try:
                self.logger.debug(f'value with id {catalog_id} not found; attempt to reload catalog')
                await self.load_catalog()
            except CatalogException as e:
                self.logger.error(f'failed to get values from catalog', exc_info=True,
                                  extra={'catalog_id': catalog_id, 'catalog_url': self.build_url()})
            # noinspection PyTypeChecker
            return self.catalog_values.get(catalog_id)
        else:
            self.logger.debug(f'value {catalog_id} already loaded get from local')
            return value
