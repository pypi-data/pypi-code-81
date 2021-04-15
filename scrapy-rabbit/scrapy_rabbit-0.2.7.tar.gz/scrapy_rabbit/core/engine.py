# -*- coding: utf-8 -*-
# Author: Eamonn
# Email: china.eamonn@gmail.com
# Link: https://elanpy.com

import fuclib
import os
import scrapy
from scrapy_rabbit.conf import conf
from scrapy.utils.reqser import request_to_dict
from collections import Generator
from asyncio.events import new_event_loop
from asyncio.tasks import run_coroutine_threadsafe
from logging import getLogger
from threading import Thread
from scrapy_rabbit.http import Request
from scrapy_rabbit.utils import get_project_settings
from scrapy_rabbit.rabbitmq import RabbitConnect
from re import search
from pickle import dumps, loads
from pika import exceptions
from asyncio import set_event_loop
from time import ctime
from functools import partial
from traceback import print_exc
from scrapy_rabbit.http import random_ua
from scrapy_rabbit.settings import overridden_settings
import sys

sys.path.append(os.path.abspath('../..'))
sys.path.append(os.path.abspath('../../..'))

logger = getLogger(__name__)


class DaemonRun(Thread):
    def __init__(self, func, loop, scrapy_object, *args, **kwargs):
        super(DaemonRun, self).__init__(*args, **kwargs)
        self.connector, self.channel = RabbitConnect(scrapy_object=scrapy_object).connect()
        self.func = func
        self.loop = loop
        self.setDaemon(True)

    def run(self) -> None:
        self.func(self.loop)


class Engine(object):
    timeout = 180
    max_times = 3
    start_urls = list()
    custom_settings = dict()
    allow_status_code = list()

    priority_queue = False
    queue_purge = True
    name = None

    proxy = False

    def __init__(self, path, queue_name, way='auto', async_num=10):
        settings_base = get_project_settings()
        settings_copy = settings_base.copy()
        self.settings = dict(overridden_settings(settings_copy))

        self.path = path
        self.queue_name = queue_name
        self.way = way
        self.async_num = async_num

        self.rabbit_username = None
        self.rabbit_password = None
        self.rabbit_host = None
        self.rabbit_port = None
        self.rabbit_vhost = None

        self.mongo_host = None
        self.mongo_port = None
        self.mongo_database = None
        self.mongo_table = None
        self.mongo_username = None
        self.mongo_password = None
        self.mongo = None

        self.thread = None
        self.count = 0
        self.channel = None
        self.connector = None
        self.update_machine = None
        # self._settings = settings.__dict__

        self.request = None
        self.loop = None
        self.session = None
        self.loop = None

        self.rabbit = None

        self.RANDOM_USER_AGENT = self.settings.get('RANDOM_USER_AGENT')

        self.RETRY_ENABLED = self.settings.get('RETRY_ENABLED')
        self.RETRY_TIMES = self.settings.get('RETRY_TIMES')

    def get_proxy(self):
        proxy_res = fuclib.getIP()
        if proxy_res:
            return proxy_res['proxy']

    def close(self):
        pass

    def rabbit_connection(self):
        """rabbitmq连接"""
        self.rabbit = RabbitConnect(scrapy_object=self)
        return self.rabbit.connect()

    def produce(self, url=None, params=None, data=None, json=None, charset=None, cookies=None, method='get',
                headers=None, callback="parse", allow_redirects=True, meta=None, not_request=None, priority=1):
        """生产"""
        if not isinstance(callback, str):
            callback = callback.__name__
        if meta is None:
            meta = dict()
        if not_request or (isinstance(url, str) and not search(r"^https?://", url)):
            request = {'not_request': True,
                       'url': url,
                       'callback': callback,
                       'meta': meta
                       }
        else:
            if isinstance(url, dict):
                ret = url
                request = {
                    'url': ret['url'],
                    'params': ret.get('params'),
                    'data': ret.get('data', ret.get('body')),
                    'json': ret.get('json'),
                    'charset': ret.get('charset'),
                    'cookies': ret.get('cookies'),
                    'method': ret.get('method', 'GET'),
                    'headers': ret.get('headers'),
                    'callback': ret.get('callback') if ret.get('callback') else 'parse',
                    'allow_redirects': ret.get('allow_redirects') if ret.get('allow_redirects') else True,
                    'meta': ret.get('meta') if ret.get('meta') else {},
                    'url_encoded': True if '%' in ret['url'] else False,
                    'priority': ret.get('priority', 1),
                    'retry_times': ret.get('retry_times', 0)
                }
            else:
                request = {
                    'url': url,
                    'params': params,
                    'data': data,
                    'json': json,
                    'charset': charset,
                    'cookies': cookies,
                    'method': method,
                    'headers': headers,
                    'callback': callback,
                    'allow_redirects': allow_redirects,
                    'meta': meta,
                    'url_encoded': True if '%' in url else False,
                    'priority': priority
                }
        if self.RANDOM_USER_AGENT:
            request['headers']['User-Agent'] = random_ua()
        if request['data']:
            request['method'] = 'post'
        if self.timeout:
            request['time_out'] = self.timeout
        if self.thread:
            self.rabbit.produce(channel=self.thread.channel, request=dumps(request), queue=self.queue_name,
                                priority=request['priority'])
            pass
        else:
            self.rabbit.produce(request=dumps(request), queue=self.queue_name, priority=request['priority'])
        self.count += 1

        logger.info("(%s) %s 生产：%s" % (self.queue_name, self.count, request))

    def consume(self):
        """消费"""
        while True:
            try:
                # self.connector, self.channel = self.rabbit.sure_conn(self.queue_name, self.connector, self.channel)
                self.rabbit.consume(self.channel, self.queue_name, callback=self.callback,
                                    prefetch_count=self.async_num)

                break
            except exceptions.ConnectionClosed:
                self.connector, self.channel = self.rabbit_connection()
                print('-', "pika.exceptions.ConnectionClosed", ctime())

    async def deal(self, ch, method, properties, ret):
        try:
            self.routing(self.__getattribute__(ret['callback']), ret)
            self.connector.add_callback_threadsafe(partial(ch.basic_ack, method.delivery_tag))
        except Exception as e:
            print_exc()
            self.deal_error(e)

    def routing(self, function, *args, **kwargs):
        result_type = function(*args, **kwargs)
        if isinstance(result_type, Generator):
            for i in result_type:
                if isinstance(i, scrapy.Request):  # 通过yield过来的请求
                    request = self.decode_request(request_to_dict(i, self))
                    self.produce(request)
                elif isinstance(i, scrapy.Item):
                    self.pipeline(i)
                else:
                    raise
        elif isinstance(result_type, scrapy.Request):
            request = self.decode_request(request_to_dict(result_type, self))  # 通过return过来的请求
            self.produce(request)
        elif isinstance(result_type, scrapy.Item) or isinstance(result_type, dict):
            self.pipeline(result_type)

    def pipeline(self, item):
        pipeline_object = getattr(self, "pipelineObj")
        ret = pipeline_object.process_item(item, self)
        logger.debug("(%s) Item %s：%s" % (self.queue_name, pipeline_object.count, item))  # todo

    def decode_request(self, request: dict):
        """从scrapy传过来的Request对象部分键值为byte类型"""
        result = {}
        for k, v in request.items():
            if isinstance(k, bytes):
                new_k = k.decode()
            else:
                new_k = k
            if isinstance(v, bytes):
                new_v = v.decode()
            elif isinstance(v, dict):
                new_v = self.decode_request(v)
            elif isinstance(v, (list, tuple)):
                if len(v) > 1:
                    raise
                if not v:
                    new_v = ''
                else:
                    new_v = v[0].decode() if isinstance(v[0], bytes) else v[0]
            else:
                new_v = v
            result[new_k] = new_v
        return result

    def deal_error(self, e):
        if self.way == 'auto':
            names = ("error_type", "auto_frequency")
            values = (e.args[0], -1)
            logger.error("采集报错。", names, values)
        os._exit(1)

    def callback(self, ch, method, properties, body):
        """rabbit_mq回调函数"""
        if body:
            try:
                result = body.decode()
            except UnicodeDecodeError:
                result = body
        else:
            raise
        ret = loads(result)
        ret = self.before_request(ret)
        if 'not_request' in ret:
            logger.info('(%s) 消费：%s' % (self.queue_name, ret))
            coroutine = self.deal(ch, method, properties, ret)
            run_coroutine_threadsafe(coroutine, self.loop)
        else:
            # if not ret['headers']:
            #     ret['headers'] = {"User-Agent": fuclib.ezfuc.random_ua()}  # todo
            if self.proxy:
                proxy_res = fuclib.getIP()
                if proxy_res:
                    ret['proxies'] = proxy_res['proxy']
                    # ret['headers']["Proxy-Authorization"] = fuclib.proxyAuth
            logger.info('(%s) 消费：%s' % (self.queue_name, ret))

            coroutine = self.deal_resp(ch, method, properties, ret)
            run_coroutine_threadsafe(coroutine, self.loop)

    async def deal_resp(self, ch, method, properties, ret):
        """请求并回调处理响应函数"""
        try:
            response = await self.request.quest(self.session, ret)
            if response and (response.status_code in self.allow_status_code or response.status_code == 200):
                try:
                    self.routing(self.__getattribute__(ret['callback']), response)
                except Exception as e:
                    self.connector.add_callback_threadsafe(partial(ch.basic_nack, method.delivery_tag))
                    print_exc()
                    self.deal_error(e)
                self.connector.add_callback_threadsafe(partial(ch.basic_ack, method.delivery_tag))
            else:
                if self.RETRY_ENABLED:  # todo 重试方法需要重写
                    retry_times = ret.get('retry_times', 5)
                    if retry_times <= self.RETRY_TIMES:
                        if response:
                            logger.error("第 %s 次 (%s) 请求失败!返回状态码：%d,返回队列%s" % (
                                retry_times, self.name, response.status_code, ret))
                        else:
                            logger.error(
                                "第 %s 次 (%s) 请求报错!未返回消息,返回队列%s" % (retry_times, self.queue_name, self.queue_name))
                        ret['retry_times'] = retry_times + 1
                        self.produce(ret)
                        self.connector.add_callback_threadsafe(partial(ch.basic_ack, method.delivery_tag))
                else:
                    logger.info("(%s) 请求报错!未返回消息" % self.name)
                    self.produce(ret)
                    self.connector.add_callback_threadsafe(partial(ch.basic_ack, method.delivery_tag))
        except Exception as e:
            print_exc()
            self.deal_error(e)

    def start_requests(self):
        """抽象生产函数"""
        if self.start_urls:
            for url in self.start_urls:
                self.produce(url)

    def parse(self, response):
        """抽象解析函数"""
        pass

    def before_request(self, ret):
        """请求中间件"""
        return ret

    @staticmethod
    def run_forever(loop):
        """实时接收新事件"""
        set_event_loop(loop)
        loop.run_forever()

    def main(self):
        """启动函数"""
        # 配置文件初始化
        serious = [
            'rabbit_username',
            'rabbit_password',
            'rabbit_host',
            'rabbit_port',
            'rabbit_vhost',
            'mongo_host',
            'mongo_port',
            'mongo_database',
            'mongo_table',
            'mongo_username',
            'mongo_password'
        ]
        for i in serious:
            if hasattr(self, i) and getattr(self, i) is None:
                attr = getattr(conf, i)
                setattr(self, i, attr if attr else None)
        self.settings.update(self.custom_settings)
        # self._settings.setdefault('DOWNLOADER_MIDDLEWARES',
        #                           {'DOWNLOADER_MIDDLEWARES': {'frame.tools.middleware.DownloaderMiddleware': 1}})

        self.connector, self.channel = self.rabbit_connection()
        logger.info('rabbitmq配置：%s' % [self.rabbit_host, self.rabbit_port, self.rabbit_username])
        logger.info('mongodb配置：%s' % [self.mongo_host, self.rabbit_port, self.mongo_database])

        # # 脚本信息入库
        # self.update_machine = gethostbyname(gethostname())
        # logger.info("本机ip为：%s" % self.update_machine)
        # todo 保存脚本运行时间

        if self.way and (self.way == 'm' or self.way == 'auto'):
            if self.priority_queue:
                self.channel.queue_declare(queue=self.queue_name, durable=True,
                                           arguments={"x-max-priority": 10})  # todo 优先级队列自动切换
            else:
                self.channel.queue_declare(queue=self.queue_name, durable=True)
            if self.queue_purge:
                self.rabbit.queue_purge(self.queue_name)
            else:
                logger.info("继续生产!!!")
            self.routing(self.start_requests)

        if self.way and (self.way == 'w' or self.way == 'auto'):
            self.request = Request()
            self.loop = new_event_loop()
            self.session = self.loop.run_until_complete(self.request.new_session())

            self.thread = DaemonRun(self.run_forever, self.loop, self)
            self.thread.start()

            self.consume()

            run_coroutine_threadsafe(self.request.exit(self.session), self.loop)

            self.close()

        if not self.way or self.way not in ('m', 'w', 'auto'):
            raise

        self.channel.close()


Spider = Engine
