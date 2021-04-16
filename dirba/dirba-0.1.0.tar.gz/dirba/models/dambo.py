from typing import List

import pydantic

from .abc import AbstractProhibitedModel, Predict, Author
from ..runners.kafka_runners.topic_schemas import LoaderMessage
from dirba.utils.catalogs import CategoryCatalog


class DamboInput(pydantic.BaseModel):
    text: str


class DamboModel(AbstractProhibitedModel):
    def __init__(self, category_catalog: CategoryCatalog):
        super().__init__(category_catalog)
        self.category_catalog.load_catalog_sync()

    def predict(self, features: DamboInput) -> List[Predict]:
        return [Predict(score=1, category=i) for i in self.category_catalog.catalog_values]

    def preprocess(self, features: LoaderMessage) -> DamboInput:
        return DamboInput(text='dambooooooooooooo')

    def author(self) -> Author:
        return Author(name='dambo', version='0.0.1')
