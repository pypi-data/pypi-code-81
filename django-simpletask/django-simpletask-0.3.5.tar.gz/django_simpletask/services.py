import logging
import json
import time
from urllib import parse as urlparse

import bizerror
import requests
from fastutils import sysutils
from fastutils import threadutils
from fastutils import threadutils

from django_apiview.pack import SimpleJsonResultPacker

logger = logging.getLogger(__name__)

class SimpleTaskProducer(threadutils.SimpleProducer):

    def __init__(self, task_server_url, task_server_aclkey, executorName, channel=None, batch_size=5, api_url_get_ready_tasks=None, response_packer=None, **kwargs):
        self.task_server_url = task_server_url
        self.task_server_aclkey = task_server_aclkey
        self.batch_size = batch_size
        self.channel = channel
        self.executorName = executorName
        self.api_url_get_ready_tasks = api_url_get_ready_tasks or urlparse.urljoin(self.task_server_url, "./getReadyTasks")
        self.response_packer = response_packer or SimpleJsonResultPacker()
        super().__init__(**kwargs)

    def produce(self):
        logger.info("SimpleTaskProducer do produce...")
        try:
            params = {
                "aclkey": self.task_server_aclkey,
                "executorName": self.executorName,
                "batchSize": self.batch_size,
                "channel": self.channel,
                "ts": time.time(),
            }
            logger.info("SimpleTaskProducer calling get_ready_tasks api: url={0}, params={1}".format(self.api_url_get_ready_tasks, params))
            response = requests.get(self.api_url_get_ready_tasks, params)
            logger.info("SimpleTaskProducer calling get_ready_tasks api got response: content={0}".format(response.content))
            tasks = self.response_packer.unpack(response.content)
            if tasks:
                logger.info("SimpleTaskProducer calling get_ready_tasks api parse the response and got the tasks: {0}".format(tasks))
            else:
                logger.info("SimpleTaskProducer calling get_ready_tasks api parse the response and got NO tasks...")
            return tasks
        except Exception as error:
            logger.exception("SimpleTaskProducer produce tasks failed: {0}".format(str(error)))
            return []

class SimpleTaskConsumer(threadutils.SimpleConsumer):

    def __init__(self, task_server_url, task_server_aclkey, executorName, task_id_field_name="id", api_url_do_task=None, response_packer=None, **kwargs):
        self.task_server_url = task_server_url
        self.task_server_aclkey = task_server_aclkey
        self.task_id_field_name = task_id_field_name
        self.executorName = executorName
        self.api_url_do_task = api_url_do_task or urlparse.urljoin(self.task_server_url, "./doTask")
        self.response_packer = response_packer or SimpleJsonResultPacker()
        super().__init__(**kwargs)

    def consume(self, task):
        logger.info("SimpleTaskConsumer do consume task: {0}".format(str(task)))
        try:
            params = {
                "ts": time.time(),
            }
            data = {
                "task": task,
                "aclkey": self.task_server_aclkey,
                "executorName": self.executorName,
            }
            logger.info("SimpleTaskConsumer calling do_task api: url={0}, params={1}".format(self.api_url_do_task, params))
            response = requests.post(self.api_url_do_task, params=params, json=data)
            logger.info("SimpleTaskConsumer calling do_task api got response: content={0}".format(response.content))
            result = self.response_packer.unpack(response.content)
            logger.info("SimpleTaskConsumer unpack response content and got result={0}".format(result))
            result
        except Exception as error:
            logger.exception("SimpleTaskConsumer consume task failed: error_message={0}".format(str(error)))
            return False

class ProxiedSimpleTaskConsumer(threadutils.SimpleConsumer):

    default_task_id_field_name = "id"

    def __init__(self, task_server_url, task_server_aclkey, executorName, task_id_field_name=None, api_url_get_task_info=None, api_url_report_success=None, api_url_report_error=None, response_packer=None, do_proxied_task_main=None, do_proxied_task_main_args=None, do_proxied_task_main_kwargs=None, **kwargs):
        self.task_server_url = task_server_url
        self.task_server_aclkey = task_server_aclkey
        self.executorName = executorName
        self.task_id_field_name = task_id_field_name or self.default_task_id_field_name
        self.api_url_get_task_info = api_url_get_task_info or urlparse.urljoin(self.task_server_url, "./getTaskInfo")
        self.api_url_report_success = api_url_report_success or urlparse.urljoin(self.task_server_url, "./reportSuccess")
        self.api_url_report_error = api_url_report_error or urlparse.urljoin(self.task_server_url, "./reportError")
        self.response_packer = response_packer or SimpleJsonResultPacker()
        self.do_proxied_task_main_callback = do_proxied_task_main
        self.do_proxied_task_main_callback_args = do_proxied_task_main_args or []
        self.do_proxied_task_main_callback_kwargs = do_proxied_task_main_kwargs or {}
        super().__init__(**kwargs)

    def consume(self, task):
        logger.info("ProxiedSimpleTaskConsumer do consume: task={}".format(task))
        try:
            info = self.get_task_info(task)
            result = self.do_task_main(task, info)
            self.report_success(task, result)
        except Exception as error:
            logger.exception("ProxiedSimpleTaskConsumer failed in consume main process: error_message={0}".format(str(error)))
            error = bizerror.BizError(error)
            try:
                self.report_error(task, error.code, error.message)
            except Exception as error:
                logger.exception("ProxiedSimpleTaskConsumer report error failed: error_message={0}".format(str(error)))

    def get_task_info(self, task):
        logger.info("ProxiedSimpleTaskConsumer doing get_task_info...")
        params = {
            "ts": time.time(),
        }
        data = {
            "task": task,
            "aclkey": self.task_server_aclkey,
        }
        logger.info("ProxiedSimpleTaskConsumer calling get_task_info api: url={0}, params={1}".format(self.api_url_get_task_info, params))
        response = requests.post(self.api_url_get_task_info, params=params, json=data)
        logger.info("ProxiedSimpleTaskConsumer call get_task_info api got response: content={0}".format(response.content))
        result = self.response_packer.unpack(response.content)
        logger.info("ProxiedSimpleTaskConsumer unpack response content and got result={0}".format(result))
        return result

    def do_task_main(self, task, info):
        logger.info("ProxiedSimpleTaskConsumer calling do_task_main...")
        if self.do_proxied_task_main_callback:
            logger.info("ProxiedSimpleTaskConsumer calling do_proxied_task_main_callback...")
            result = self.do_proxied_task_main_callback(task, info, *self.do_proxied_task_main_callback_args, **self.do_proxied_task_main_callback_kwargs)
            logger.info("ProxiedSimpleTaskConsumer call do_proxied_task_main_callback and got result={0}".format(result))
            return result
        else:
            logger.error("ProxiedSimpleTaskConsumer has NO do_proxied_task_main_callback and NOT reimplemented do_task_main method!")
            raise NotImplementedError()

    def report_success(self, task, result_message):
        logger.info("ProxiedSimpleTaskConsumer doing report_success...")
        params = {
            "ts": time.time(),
        }
        data = {
            "task": task,
            "aclkey": self.task_server_aclkey,
            "worker": self.executorName,
            "result_message": result_message,
        }
        logger.info("ProxiedSimpleTaskConsumer calling report_success api: url={0}, params={1}, data={2}".format(self.api_url_report_success, params, data))
        response = requests.post(self.api_url_report_success, params=params, json=data)
        logger.info("calling report_success api got response: content={}".format(response.content))
        return self.response_packer.unpack(response.content)

    def report_error(self, task, error_code, error_message):
        logger.info("ProxiedSimpleTaskConsumer doing report error...")
        params = {
            "ts": time.time(),
        }
        data = {
            "task": task,
            "aclkey": self.task_server_aclkey,
            "worker": self.executorName,
            "error_code": error_code,
            "error_message": error_message,
        }
        logger.info("ProxiedSimpleTaskConsumer calling report_error api: url={0}, params={1}, data={2}".format(self.api_url_report_error, params, data))
        response = requests.post(self.api_url_report_error, params=params, json=data)
        logger.info("ProxiedSimpleTaskConsumer calling report_error api got response: content={0}".format(response.content))
        result = self.response_packer.unpack(response.content)
        logger.info("ProxiedSimpleTaskConsumer unpack response content and got resul={0}".format(result))
        return result

class SimpleTaskService(threadutils.SimpleProducerConsumerServer):

    def __init__(self, **kwargs):
        executorName = sysutils.get_worker_id(self.__class__.__name__)
        producer_class_init_kwargs = kwargs.get("producer_class_init_kwargs", {})
        consumer_class_init_kwargs = kwargs.get("consumer_class_init_kwargs", {})
        kwargs["producer_class_init_kwargs"] = producer_class_init_kwargs
        kwargs["consumer_class_init_kwargs"] = consumer_class_init_kwargs
        producer_class_init_kwargs["executorName"] = executorName
        consumer_class_init_kwargs["executorName"] = executorName
        super().__init__(**kwargs)

    default_producer_class = SimpleTaskProducer
    default_consumer_class = SimpleTaskConsumer

class ProxiedSimpleTaskService(threadutils.SimpleProducerConsumerServer):

    def __init__(self, **kwargs):
        executorName = sysutils.get_worker_id(self.__class__.__name__)
        producer_class_init_kwargs = kwargs.get("producer_class_init_kwargs", {})
        consumer_class_init_kwargs = kwargs.get("consumer_class_init_kwargs", {})
        kwargs["producer_class_init_kwargs"] = producer_class_init_kwargs
        kwargs["consumer_class_init_kwargs"] = consumer_class_init_kwargs
        producer_class_init_kwargs["executorName"] = executorName
        consumer_class_init_kwargs["executorName"] = executorName
        super().__init__(**kwargs)

    default_producer_class = SimpleTaskProducer
    default_consumer_class = ProxiedSimpleTaskConsumer
