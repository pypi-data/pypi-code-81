import logging
import uuid
from abc import ABC, abstractmethod
from asyncio.events import AbstractEventLoop
from typing import Type, Optional, Tuple

import aiohttp
import aiomisc
import sentry_sdk

from ...models.abc import AbstractModel, Predict
from .shared import KafkaConfig
from .producer import AbstractKafkaProducer
from .consumer import AbstractKafkaConsumer
from .topic_schemas import LoaderMessage, AnalysisResult, AnalysisMessage, ModelOutput


class AbstractBaseKafkaRunner(AbstractKafkaConsumer, AbstractKafkaProducer):
    """
    Класс для запуска ML моделей в apache kafka
    """

    def __init__(self, model: AbstractModel, connection_config: KafkaConfig, from_topic_begin=False):
        """
        Создание экземляра runner'a.

        У класса должно быть определено свойство InputModel, для сериализации поступающих данных.
        У класса должно быть определено свойство OutputModel, для сериализации отправляемых данных.
        :param connection_config: конфигурация для работы с kafka
        :param from_topic_begin: обрабатывать данные с начала очереди
        :param model: ML модель для определения категории материала
        """
        AbstractKafkaConsumer.__init__(self, connection_config, from_topic_begin)
        AbstractKafkaProducer.__init__(self, connection_config)

        self.from_topic_begin = from_topic_begin
        self.model = model
        self.kafka_config = connection_config

        self.logger = logging.getLogger(self.__class__.__name__)

    # noinspection PyMethodOverriding
    async def start(self):
        await AbstractKafkaProducer.start(self, trigger_start=False)
        await AbstractKafkaConsumer.start(self, trigger_start=False)

        self.start_event.set()

    async def stop(self, exception: Exception = None):
        await AbstractKafkaConsumer.stop(self, exception)
        await AbstractKafkaProducer.stop(self, exception)

    @abstractmethod
    def pack_model_answer(self, message: AbstractKafkaConsumer.InputModel,
                          predict: Predict) -> Optional[AbstractKafkaProducer.OutputModel]:
        """
        Собирает сообщение для отправки в шину из входящего сообщения и одной из оценок модели.

        Здесь же может быть инкапсулирована бизнес логика, связанная с обработкой результатов работы модели.
        Допускаются ситуации, в которых ответов модели не нужно отправлять, в таком случае можно вернуть
        `None`
        """
        pass

    async def _pre_process(
            self,
            message: AbstractKafkaConsumer.InputModel
    ) -> Optional[AbstractKafkaConsumer.InputModel]:
        """
        Хук, выполняющихся  перед обработкой сообщения бизнес логикой.

        :param message: входное сообщение
        :return: при возвращении None материал не будет обработан
        """
        return message

    async def _post_process(
            self,
            message: AbstractKafkaProducer.OutputModel
    ) -> Optional[AbstractKafkaConsumer.InputModel]:
        """
        Хук, выполняющихся  после обработкой сообщения бизнес логикой и **перед отправкой**.

        :param message: отправляемое сообщение
        :return: при возвращении None материал не будет обработан
        """
        return message

    async def process(self, message: AbstractKafkaConsumer.InputModel):
        message = await self._pre_process(message)
        if not message:
            self.logger.debug(f'message rejected on pre process; message: {message}')
            return

        if not self.is_adorable(message):
            return

        with sentry_sdk.start_transaction(op='predict', name='model_predict') as transaction:
            # noinspection PyUnresolvedReferences
            model_result = await self.model.async_call(message)
            self.logger.info(f'model produced {model_result}')
            for predict in model_result:
                packed_result = self.pack_model_answer(message, predict)
                if packed_result is None:
                    continue
                self.logger.info(f'packed {packed_result}')

                packed_result = await self._post_process(packed_result)
                if not packed_result:
                    self.logger.debug(f'message rejected on post process; message: {packed_result}')
                    return

                await self.send_message(packed_result)

    @abstractmethod
    def is_adorable(self, input_message: AbstractKafkaConsumer.InputModel) -> bool:
        """
        Проверка сообщения на применимость данной модели к нему
        :param input_message: входящее сообщение
        :return: True если сообщение должно быть обработано, иначе False
        """
        pass


class TextBaseKafkaRunner(AbstractBaseKafkaRunner):
    """
    Класс для работы с текстовыми данными в kafka_runners
    """

    def __init__(self, model: AbstractModel, connection_config: KafkaConfig, loop: AbstractEventLoop, data_api_url: str,
                 from_topic_begin=True):
        super().__init__(model, connection_config, loop, from_topic_begin=from_topic_begin)
        self.data_api_url = data_api_url

    def is_adorable(self, input_message: 'InputModel') -> bool:
        return input_message.type_content == 'text'

    def pack(self, input_message: 'InputModel', predict: Predict) -> 'OutputModel':
        if predict.score == 0:
            self.logger.info('Skipping predict with null score')
            return None
        model_output = ModelOutput(category=predict.category, estimate=predict.score)
        analysis_result = AnalysisResult(type_content='text', content_ref=input_message.result, model=model_output)
        message = self.OutputModel(uid_query=input_message.uid_query, uid_analysis=uuid.uuid4(),
                                   author=self.model.author(), uid_filter_link=input_message.uid_filter_link,
                                   uid_loaded_data=input_message.uid_loaded_data, uid_loader=input_message.uid_loader,
                                   uid_search=input_message.uid_search,
                                   query_id=input_message.query_id, driver_id=input_message.driver_id,
                                   category_id=input_message.category_id, type_id=input_message.type_id,
                                   result=analysis_result)

        return message

    async def extract_model_feature(self, input_message: 'InputModel') -> dict:
        text_url, text = await self.get_text(input_message.result)
        return {'text': text}

    @property
    def InputModel(self) -> Type[LoaderMessage]:
        return LoaderMessage

    @property
    def OutputModel(self) -> Type[AnalysisMessage]:
        return AnalysisMessage

    TEXT = str
    TEXT_URL = str

    @aiomisc.asyncbackoff(10, 30, 0.1)
    async def get_text(self, text_id: int) -> Tuple[TEXT_URL, TEXT]:
        """
        Метод получения url текста и самого текста.
        :param text_id:
        :type text_id: int
        :param api_path: расположение API (url)
        :type api_path: str
        :return: url текста, сам текст
        :rtype: tuple[str, str]
        """
        async with aiohttp.ClientSession() as session:
            text_url = self.data_api_url + str(text_id)
            response = await session.get(text_url)

            if response.status != 200:
                raise ConnectionError(f"Error via connection with data api")

            data = await response.json()
            text = data["content"]

            return text_url, text
