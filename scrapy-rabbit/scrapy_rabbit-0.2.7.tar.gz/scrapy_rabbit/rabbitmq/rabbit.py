# -*- coding: utf-8 -*-
# Author: Eamonn
# Email: china.eamonn@gmail.com
# Link: https://elanpy.com

from requests import get
from pika import PlainCredentials
from pika import BlockingConnection
from pika import ConnectionParameters
from pika import BasicProperties
from logging import getLogger
from scrapy_rabbit.conf import conf

logger = getLogger(__name__)


class RabbitConnect(object):
    """
    RabbitMq消息队列操作
    """

    def __init__(self, scrapy_object=None):
        """
        初始化，并创建连接对象
        """
        self.__rabbit_username = scrapy_object.rabbit_username if scrapy_object.rabbit_username else conf.rabbit_username
        self.__rabbit_password = scrapy_object.rabbit_password if scrapy_object.rabbit_password else conf.rabbit_password
        self.__rabbit_host = scrapy_object.rabbit_host if scrapy_object.rabbit_host else conf.rabbit_host
        self.__rabbit_port = scrapy_object.rabbit_port if scrapy_object.rabbit_port else conf.rabbit_port
        self.__rabbit_vhost = scrapy_object.rabbit_vhost if scrapy_object.rabbit_vhost else conf.rabbit_vhost

        self.priority_queue = scrapy_object.priority_queue if scrapy_object else False

        credentials = PlainCredentials(username=self.__rabbit_username,
                                       password=self.__rabbit_password)
        self.__connector = BlockingConnection(
            ConnectionParameters(host=self.__rabbit_host,
                                 port=self.__rabbit_port,
                                 credentials=credentials,
                                 heartbeat=0),
        )
        self.__channel = self.__connector.channel()

    def connect(self):
        """返回连接对象"""
        return self.__connector, self.__channel

    def produce(self, request, queue, priority, channel=None):
        """生产"""
        if channel:
            channel.basic_publish(
                exchange='',
                routing_key=queue,
                body=request,
                properties=BasicProperties(
                    delivery_mode=2,
                    priority=priority
                )
            )
        else:
            self.__channel.basic_publish(
                exchange='',
                routing_key=queue,
                body=request,
                properties=BasicProperties(
                    delivery_mode=2,
                    priority=priority
                )
            )

    def consume(self, channel, queue, callback, prefetch_count, durable=True, max_priority=10):
        """消费"""
        if self.priority_queue:
            channel.queue_declare(queue=queue, durable=durable, arguments={"x-max-priority": max_priority})
        else:
            channel.queue_declare(queue=queue, durable=durable)
        channel.basic_qos(prefetch_count=prefetch_count)
        channel.basic_consume(
            on_message_callback=callback,
            queue=queue,
            auto_ack=False)
        channel.start_consuming()

    def queue_detail(self, queue_name):
        """查看队列当前数据量"""
        queue_name = queue_name.replace('/', '%2F')
        url = f'http://{self.__rabbit_host}:15672/api/queues/{self.__rabbit_vhost}/{queue_name}'
        response = get(url, auth=(self.__rabbit_username, self.__rabbit_password))
        if response.status_code != 200:
            return None
        dic = response.json()
        return {'ready': dic['messages_ready'], 'unconfirmed': dic['messages_unacknowledged'], 'total': dic['messages']}

    def queue_purge(self, queue_name):
        """清空队列"""
        self.__channel.queue_purge(queue_name)
        logger.info(f'{queue_name}  队列已清空')

    def queue_del(self, queue_name, if_unused=False, if_empty=True):
        """删除队列"""
        self.__channel.queue_delete(queue=queue_name, if_unused=if_unused, if_empty=if_empty)
        logger.info(f'{queue_name}  队列已删除')
