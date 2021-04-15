# -*- encoding: utf-8 -*-
'''
@文件    :rabbitma_tool.py
@说明    :针对rabbitmq进行的效率化封装
@时间    :2021/03/02 10:25:38
@作者    :caimiao@kingsoft.com
@版本    :0.1
'''

import time
from typing import Union
from inspect import isfunction
from threading import Lock
import pika
from contextlib import contextmanager
from ..logger_helper import LoggerTimedRotating 

@contextmanager
def with_pika_connection(host: str, port: int, username: str, password: str, vhost: str="/") -> pika.BlockingConnection:
    '''
    受上下文管理可以自动释放的消息队列connection
    '''
    credentials = pika.PlainCredentials(username, password)
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=host, port=port, virtual_host=vhost, credentials=credentials
    ))
    
    try:
        yield connection
    finally:
        connection.close()
        print("connection closed")

@contextmanager
def with_pika_channel_consumer(host:str, port:int, username:str, password:str, vhost:str="/") -> pika.adapters.blocking_connection.BlockingChannel:
    '''
    受上下文管理可以自动释放的消息队列channel
    '''
    with with_pika_connection(host, port, username, password, vhost) as connection:
        channel = connection.channel()
        try:
            yield channel
        finally:
            print("channel completed")

class Callbacker(object):
    '''
    消息处理回调器
    '''
    def __init__(self, auto_ack:bool = True):
        '''
        是否需要自动发送处理响应
        '''
        self._auto_ack = auto_ack

    def handler(self, ch, method, properties, body):
        '''
        注册回调函数
        '''
        raise NotImplementedError('callbacker handler must be implements in subclass')
    
    def run(self, ch, method, properties, body):
        '''
        消息回调
        '''
        try:
            hr = self.handler(ch, method, properties, body)
            if self._auto_ack and hr: 
                ch.basic_ack(delivery_tag = method.delivery_tag)
        except Exception as e:
            LoggerTimedRotating.getInstance().error(e)
        

class Producer():
    '''
    消息生产者
    '''
    def __init__(self, host: str, port: int , username: str, password: str, exchange:str, routing_key:str, durable:bool=True, vhost="/", reconnectable:bool=False):
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._exchange = exchange
        self._routing_key = routing_key
        self._vhost = vhost
        self._reconnectedable = reconnectable
        self._durable = durable
        self.initProducerGenerator()

    def initProducerGenerator(self):
        '''
        初始化生产者生成器
        '''
        if self._reconnectedable:
            self._msg_producer = self.StartReconnectProduce()
        else:
            self._msg_producer = self.StartTopicProduce()
        self._msg_producer.send(None)

    def closeProducer(self):
        '''
        关闭生产者
        '''
        self._msg_producer.close()

    def PushMessage(self, msg_list: list):
        '''
        加入消息
        '''
        if self._msg_producer:
            for msg in msg_list:
                self._msg_producer.send(msg)
        else:
            _e = "Message Producer Not Initialize!"
            print(_e)
            LoggerTimedRotating.getInstance().error(_e)
    
    def StartReconnectProduce(self):
        """
        可重连的主题模式生产者工作状态
        """
        msg_item = None
        while True:
            try:
                with with_pika_connection(self._host, self._port, self._username, self._password, self._vhost) as _connection:
                    _channel = _connection.channel()
                    _channel.exchange_declare(exchange=self._exchange, exchange_type="topic")
                    _message_delivery_mode = 2 if self._durable else 1
                    while True:
                        msg_item = yield msg_item
                        if msg_item:
                            _channel.basic_publish(exchange=self._exchange, 
                                                    routing_key=self._routing_key,
                                                    body=msg_item,
                                                    properties=pika.BasicProperties(
                                                            delivery_mode = _message_delivery_mode
                                                        )
                                                    )
                            print(f"Send Msg {msg_item} \n")
            except Exception as e:
                LoggerTimedRotating.getInstance().error(e)
                time.sleep(2)
            
        print("Topic Produce Quit")

    def StartTopicProduce(self):
        '''
        开始进入主题模式生产者工作状态
        '''
        msg_item = None
        with with_pika_connection(self._host, self._port, self._username, self._password, self._vhost) as _connection:
            _channel = _connection.channel()
            _channel.exchange_declare(exchange=self._exchange, exchange_type="topic")
            _message_delivery_mode = 2 if self._durable else 1
            while True:
                msg_item = yield msg_item
                if msg_item:
                    _channel.basic_publish(exchange=self._exchange, 
                                            routing_key=self._routing_key,
                                            body=msg_item,
                                            properties=pika.BasicProperties(
                                                    delivery_mode = _message_delivery_mode
                                                )
                                            )
                    print(f"Send Msg {msg_item} \n")
            
        print("Topic Produce Quit")

class ConsumerReconnectable():
    '''
    支持自动重连的消息队列消费者
    '''
    def __init__(self, host: str, port: int, username: str, password: str, vhost="/"):
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._vhost = vhost
        self._stopping = False

    def StartTopicConsumer(self, callback: Union[callable, Callbacker], exchange: str, routing_key:str, queue: str='', basic_qos:int = 1):
        '''
        以主题交换机方式开启一个消息消费者
        :param callback: callable 消费者的回调函数，可以是一个函数，也可以是Callbacker类的子类
        :param exchange: str 消息交换机
        :param routing_key: str 消息绑定键
        :param queue: str 队列名称，当队列名称为空（匿名）时，队列自动删除，且不做消息持久化处理，如果队列名不为空，
        :param basic_qos: int 队列单次获取消息的个数
        '''
        # 命名队列默认设置为消息需要存档
        if queue:
            _exclusive = False
        else:
            _exclusive = True
        while not self._stopping:
            try:
                with with_pika_channel_consumer(self._host, self._port, self._username, self._password, self._vhost) as channel:
                    channel.exchange_declare(exchange=exchange, exchange_type='topic')
                    _queuename = channel.queue_declare(queue, exclusive=_exclusive).method.queue
                    channel.queue_bind(exchange=exchange, 
                    queue=_queuename, 
                    routing_key=routing_key)

                    _callback_func = None
                    
                    if isfunction(callback):
                        _callback_func = callback
                    elif issubclass(callback.__class__, Callbacker):
                        _callback_func = callback.run
                    channel.basic_consume(
                        _queuename,
                        _callback_func,
                        auto_ack=False
                    )
                    channel.start_consuming()
            except Exception as e:
                LoggerTimedRotating.getInstance().error(e)
                time.sleep(2)