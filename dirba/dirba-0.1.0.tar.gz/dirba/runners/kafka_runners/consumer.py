from abc import abstractmethod
from typing import Optional, TypeVar, Type, Any
import asyncio
import logging

import aiomisc
import orjson
import pydantic
import sentry_sdk
from aiokafka import AIOKafkaConsumer, ConsumerRecord

from dirba.runners.kafka_runners.shared import KafkaConfig

InputType = TypeVar('InputType', bound=pydantic.BaseModel)


class AbstractKafkaConsumer(aiomisc.Service):
    InputModel: Type[InputType] = None

    on_error_wait = 0.2

    def __init__(self, connection_config: KafkaConfig, from_topic_begin=False, **kwargs):
        """
        Создание экземляра consumer'a. У класса должно быть определено свойство InputModel,
         для сериализации поступающих данных.

        :param connection_config: конфигурация для работы с kafka; output_topic необязателен
        :param from_topic_begin: обрабатывать данные с начала очереди
        """
        aiomisc.Service.__init__(self, **kwargs)
        if not self.InputModel:
            raise TypeError("You should specify InputModel type")

        self.from_topic_begin = from_topic_begin
        self.kafka_config = connection_config
        if not self.kafka_config.input_topic:
            raise ValueError("Kafka input topic should be specified in config")

        self.logger = logging.getLogger(self.__class__.__name__)

        self.consumer: Optional[AIOKafkaConsumer] = None

    def _create_consumer(self) -> AIOKafkaConsumer:
        return AIOKafkaConsumer(self.kafka_config.input_topic,
                                loop=self.loop, bootstrap_servers=self.kafka_config.bootstrap_servers,
                                group_id=self.kafka_config.group_id,
                                value_deserializer=orjson.loads,
                                auto_offset_reset="earliest" if self.from_topic_begin else 'latest',
                                auto_commit_interval_ms=1000)

    @abstractmethod
    async def on_startup(self):
        """
        Необязательный к реализации хук, который выполняется до запуска consumer'a
        """
        pass

    @abstractmethod
    async def process(self, message: InputModel):
        """
        Обработка полученного сообщения.

        Обработка выполняется после сериализации к указанному виду сообщения.
        """
        pass

    async def start(self, trigger_start=True):
        if self.consumer is None:
            self.consumer = self._create_consumer()
        else:
            raise Exception("Only single run is allowed for consumer")

        await self.on_startup()
        self.logger.info(f'started up {self.kafka_config.input_topic}')

        await self.consumer.start()
        self.logger.info(f'start consuming {self.kafka_config.input_topic}')

        if trigger_start:
            self.start_event.set()

        try:
            async for msg in self.consumer:
                await self._consume(msg)
        finally:
            self.logger.info('stopping')
            await self.consumer.stop()
            self.logger.info('consume stopped')

    async def stop(self, exception: Exception = None):
        if self.consumer is not None:
            await self.consumer.stop()

    async def _consume(self, msg: ConsumerRecord):
        err_extra_info = {
            'raw_message': msg.value, 'topic': msg.topic,
            'partition': msg.partition, 'offset': msg.offset
        }

        self.logger.debug(f'consumed on: {msg.topic=}, {msg.partition=}, {msg.offset=},'
                          f' {msg.key=} {msg.timestamp=}; value: {msg.value}')

        try:
            record = self.InputModel(**msg.value)
            with sentry_sdk.start_transaction(name="consume data", op="consume") as transaction:
                await self.process(record)
        except pydantic.ValidationError:
            self.logger.error(f'unable to parse kafka message', extra=err_extra_info)
            await asyncio.sleep(self.on_error_wait)
        except Exception as e:
            self.logger.error(f'Error processing message: {e}', exc_info=True, extra=err_extra_info)
            await asyncio.sleep(self.on_error_wait)
