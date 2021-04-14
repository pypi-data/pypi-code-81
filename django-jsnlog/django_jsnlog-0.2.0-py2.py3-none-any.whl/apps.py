# -*- coding: utf-8
import logging

from django.apps import AppConfig


class DefaultJSNLogConfig(AppConfig):
    logger = None
    name = 'jsnlog'
    verbose_name = 'JSNLog'


class LoggerJSNLogConfig(DefaultJSNLogConfig):
    def ready(self):
        self.logger = logging.getLogger(self.name)
