from abc import abstractmethod
from typing import Optional, TypeVar, Type, Any
import logging

import aiomisc
import orjson
import pydantic
import sentry_sdk
from aiokafka import AIOKafkaProducer

from dirba.runners.kafka_runners.shared import KafkaConfig

OutputType = TypeVar('OutputType', bound=pydantic.BaseModel)


class AbstractKafkaProducer(aiomisc.Service):
    OutputModel: Type[OutputType] = None

    on_error_wait = 0.2

    def __init__(self, connection_config: KafkaConfig, **kwargs):
        """
        Создание экземляра producer'a. У класса должно быть определено свойство OutputModel,
         для сериализации отправляемых данных.

        :param connection_config: конфигурация для работы с kafka; input_topic необязателен
        """
        super().__init__(**kwargs)
        if not self.OutputModel:
            raise TypeError("You should specify OutputModel type")

        self.kafka_config = connection_config
        if not self.kafka_config.output_topic:
            raise ValueError("Kafka output topic should be specified in config")

        self.logger = logging.getLogger(self.__class__.__name__)

        self.producer: Optional[AIOKafkaProducer] = None

    def _create_producer(self):
        return AIOKafkaProducer(client_id=self.kafka_config.group_id,
                                loop=self.loop, bootstrap_servers=self.kafka_config.bootstrap_servers,
                                value_serializer=orjson.dumps)

    async def start(self, trigger_start=True):
        if self.producer is None:
            self.producer = self._create_producer()
        else:
            raise Exception("Only single run is allowed for producer")

        await self.producer.start()

        await self.on_startup()
        self.logger.info(f'started up {self.kafka_config.input_topic}')

        if trigger_start:
            self.start_event.set()

    async def stop(self, exception: Exception = None):
        if self.producer is not None:
            await self.producer.stop()

    @abstractmethod
    async def on_startup(self):
        """
        Необязательный к реализации хук, который выполняется до запуска producer'a
        """
        pass

    async def send_message(self, message: OutputModel):
        """
        Отправка сообщения в топик.

        По умолчанию, принимается объект, условленного в рамках producer'a типа, однако сюда может быть
        передан любой объект, который будет принудительно сериализован к типу OutputModel с помощью pack,
         если он не является его экземпляром.

         :raises: TypeError: при несоответствии типа сообщения и невозможности сериализации
        """
        if not isinstance(message, self.OutputModel):
            try:
                message = self.pack(message)
            except Exception as e:
                raise TypeError(f"Failed to pack message {type(message)} to {self.OutputModel}") from e

        with sentry_sdk.start_transaction(name="produce message", op="produce") as transaction:
            await self.producer.send(self.kafka_config.output_topic, message.dict())

    def pack(self, data: Any) -> OutputModel:
        """
        Функция по упаковке данных в формат сообщения для отправки в топик.

        Функция автоматически вызывается, если при отправке сообщения не был
         передан объект соответствующего типа
        """
        raise NotImplemented("Packing data to output model is not implemented")
