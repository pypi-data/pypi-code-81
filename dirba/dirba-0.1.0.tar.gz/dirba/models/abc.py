import logging
from typing import List, Union, TypeVar, Iterable
from abc import abstractmethod, ABC

import pydantic
import aiomisc

from ..utils.catalogs import CategoryCatalog
from ..utils.metrics.abc import MetricMock, AbstractMetric

CategoryDatasetName = str
CategoryName = str
CategoryId = Union[int, str]


class Predict(pydantic.BaseModel):
    """
    Объект для получения оценки от модели. В зависимости от
    типа модели, данный объект может быть дополнен другими полями
    """
    score: float
    category: CategoryId


class BinaryPredict(Predict):
    """
    Бинарная оценка
    """
    score: int = pydantic.Field(..., ge=0, le=1)


class Author(pydantic.BaseModel):
    name: str
    version: str


ModelInput = TypeVar('ModelInput')
PreprocessedInput = TypeVar('PreprocessedInput')


# TODO batch predict support
class AbstractModel(ABC):
    """
    Абстрактный класс для любой модели машинного обучения или нейронной
    сети
    """

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def __call__(self, input: ModelInput) -> List[Predict]:
        """
        Вызов модели для получения результата
        :param input:
        :return:
        """
        processed = self.preprocess(input)
        return self.predict(processed)

    @abstractmethod
    def author(self) -> Author:
        pass

    @aiomisc.threaded_separate
    def async_call(self, input: ModelInput) -> List[Predict]:
        return self.__call__(input)

    @abstractmethod
    def preprocess(self, data: ModelInput) -> PreprocessedInput:
        """
        Обрабатывает данные для последующей отправки в модель.

        Данный метод должен содержать всю предобработку для объекта, поступившего на оценку.

        В случае с запуском через kafka сюда попадёт сериализованное сообщение из топика

        :param data: объект, который необходимо обработать
        :return: объект, готовый для отправки на получение оценок
        """
        pass

    @abstractmethod
    def predict(self, features: PreprocessedInput) -> Iterable[Predict]:
        """
        Метод для получения оценки модели.

        :param features: сериализованный объект
        :return: список оценок от модели
        """
        pass


class AbstractProhibitedModel(AbstractModel, ABC):
    """
    Абстрактный класс для моделей, работающих с категориями АИС ПОИСК
    """
    metric = MetricMock()

    def __init__(self, category_catalog: CategoryCatalog):
        super().__init__()
        self.category_catalog = category_catalog

    def register_metric(self, metric: AbstractMetric):
        """
        Добавление реальной метрики к модели.

        Вызывается runner'ом при инициализации
        :param metric: используемая метрика
        :return:
        """
        self.logger.info(f'metric: {metric} was set to the model {self.author()}')
        self.metric = metric
