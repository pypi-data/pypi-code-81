import datetime
from typing import Union, Dict, Optional, List, Type

import pydantic

from .abc import AbstractCatalog, CatalogId, CatalogValue


class CatalogValueSchema(pydantic.BaseModel):
    id: CatalogId
    value: str
    description: Optional[str]
    created_at: datetime.datetime
    order_num: Optional[int]


class CatalogSchema(pydantic.BaseModel):
    id: int
    name: str
    description: Optional[str]
    values: List[CatalogValueSchema]


class CategoryCatalog(AbstractCatalog):
    """
    Класс для работы с каталогом категорий
    """

    def __init__(self, catalog_service_url: str):
        """
        Информация о каталоге должна быть представлена в виде
        общего url'a по которому можно запросить информацию по любому каталогу, например,
        http://catalogservice.com/catalogs/ куда будет подставлен ваш каталог
        http://catalogservice.com/catalogs/{catalogname}

        :param catalog_service_url: url сервиса каталогов по которому можно получить информацию о каталоге
        """
        super().__init__(CatalogValueSchema, catalog_service_url)

    def catalog_name(self) -> str:
        return 'category'

    def parse_catalog_response(self, data: Union[dict, list]) -> Dict[CatalogId, CatalogValue]:
        catalog = CatalogSchema(**data)

        return {value.id: value for value in catalog.values}
