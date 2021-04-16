from abc import abstractmethod
from typing import Optional

from ...models.abc import AbstractProhibitedModel
from .strict_runner import AbstractStrictBaseKafkaRunner
from ...utils.catalogs import CategoryCatalog
from ...utils.metrics.material_metric import MaterialMetric
from .shared import KafkaConfig


class AbstractKafkaRunner(AbstractStrictBaseKafkaRunner):
    """
    Основной класс для запуска моделей с помощью apache kafka.

    Класс адаптирован под работу с категориальными оценками

    Имеет под капотом:
     - корректную обработку ошибок
     - профайлинг операций с помощью sentry
     - сбор метрик по категориям и их экспорт для prometheus
    """
    InputModel = AbstractStrictBaseKafkaRunner.InputModel
    OutputModel = AbstractStrictBaseKafkaRunner.OutputModel

    model: AbstractProhibitedModel

    def __init__(self, model: AbstractProhibitedModel, connection_config: KafkaConfig, category_catalog: CategoryCatalog,
                 consume_incorrect_categories: bool = True, produce_incorrect_categories: bool = True,
                 from_topic_begin=False):
        """
        Создание экземляра runner'a

        :param model: ML модель для определения категории материала
        :param connection_config: конфигурация для работы с kafka
        :param from_topic_begin: обрабатывать данные с начала очереди
        :param category_catalog: объект для работы с каталогом категорий
        :param consume_incorrect_categories: передавать модели сообщения с неверной категорией
        :param produce_incorrect_categories: отправлять сообщения от моделей с неверной категорией
        """
        super().__init__(model, connection_config, category_catalog)
        self.from_topic_begin = from_topic_begin
        self.produce_incorrect_categories = produce_incorrect_categories
        self.consume_incorrect_categories = consume_incorrect_categories
        self.material_metric = MaterialMetric()
        self.model.register_metric(self.material_metric)

    async def _pre_process(self, message: InputModel) -> Optional[InputModel]:
        # noinspection PyProtectedMember
        self.material_metric._reset()
        return await super()._pre_process(message)

    async def _post_process(self, message: OutputModel) -> Optional[OutputModel]:
        message = await super()._post_process(message)
        if message:
            input_category = await self.category_catalog.get_value(message.category_id)
            result_category = await self.category_catalog.get_value(message.result.model.category)

            # noinspection PyProtectedMember
            self.material_metric._set_default_values(
                category=result_category.id, category_name=result_category.value,
                query_category=input_category.id, query_category_name=input_category.value,
                content_type=message.result.type_content, model_name=message.author.name,
                model_version=message.author.version)

            # noinspection PyProtectedMember
            self.material_metric._inc()

        return message

    @abstractmethod
    def is_adorable(self, input_message: InputModel) -> bool:
        """
        Проверка сообщения на применимость данной модели к нему
        :param input_message: входящее сообщение
        :return: True если сообщение должно быть обработано, иначе False
        """
        pass
