from typing import Optional
import uuid

from ..kafka_runners.shared import KafkaConfig
from .abstract_runner import AbstractBaseKafkaRunner
from .topic_schemas import LoaderMessage, AnalysisMessage, ModelOutput, AnalysisResult
from ...models.abc import AbstractModel, Predict
from ...utils.catalogs import CategoryCatalog


class AbstractStrictBaseKafkaRunner(AbstractBaseKafkaRunner):
    """
    Вариант работы с ML моделью, подразумевающий предварительную проверку на соответствие категорий
    """
    InputModel = LoaderMessage
    OutputModel = AnalysisMessage

    def __init__(self, model: AbstractModel, connection_config: KafkaConfig,
                 category_catalog: CategoryCatalog,
                 consume_incorrect_categories: bool = True,
                 produce_incorrect_categories: bool = True,
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
        super().__init__(model, connection_config, from_topic_begin)
        self.produce_incorrect_categories = produce_incorrect_categories
        self.consume_incorrect_categories = consume_incorrect_categories

        self.category_catalog = category_catalog

    async def _pre_process(self, message: InputModel) -> Optional[InputModel]:
        """
        Проверка на соответствие категории получаемых сообщений данным в сервисе каталогов
        :param message: входящее сообщение
        :return: исходное сообщение
        """
        category_info = await self.category_catalog.get_value(message.category_id)
        if not category_info:
            self.logger.error(f'Consume incorrect category {message.category_id} '
                              f'and {"consume" if self.consume_incorrect_categories else "skip"}',
                              extra={'topic': self.kafka_config.input_topic,
                                     'model': self.model.author(),
                                     'topic_message': message})

            if not self.consume_incorrect_categories:
                return

        return message

    async def _post_process(self, message: OutputModel) -> Optional[OutputModel]:
        """
        Проверка на соответствие категории, выданной моделью, данным в сервисе каталогов
        :param message: упакованное сообщение модели
        :return: исходное сообщение
        """
        model_category = message.result.model.category
        category_info = await self.category_catalog.get_value(model_category)
        if not category_info:
            self.logger.error(f'Model produce incorrect category {model_category} '
                              f'and {"produce" if self.produce_incorrect_categories else "skip"}',
                              extra={'topic': self.kafka_config.output_topic,
                                     'model': self.model.author(),
                                     'topic_message': message})

            if not self.produce_incorrect_categories:
                return

        return message

    def pack_model_answer(self, message: InputModel, predict: Predict) -> Optional[OutputModel]:
        input_data = message.dict(include={"uid_query", "query_id", "driver_id", "category_id", "type_id",
                                           "uid_search", "uid_filter_link", "uid_loader",
                                           "uid_loaded_data", "uid_analysis", })

        model_answer = ModelOutput(category=predict.category, estimate=predict.score)
        result = AnalysisResult(content_ref=message.result,
                                model=model_answer,
                                type_content=message.type_content)

        packed = self.OutputModel(uid_analysis=uuid.uuid4(),
                                  author=self.model.author(),
                                  result=result,
                                  **input_data)
        return packed
