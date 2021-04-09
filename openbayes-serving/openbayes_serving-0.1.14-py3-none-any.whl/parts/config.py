# -*- coding: utf-8 -*-

# -- stdlib --
import logging

# -- third party --
from flask import current_app

# -- own --

# -- code --
log = logging.getLogger('observing.parts.config')


class ConfigInit:
    @staticmethod
    def is_interested(tag):
        return tag == 'config'

    @staticmethod
    def register_parameters(parser):
        parser
        pass

    @staticmethod
    def resolve(tag):
        tag
        return Configurator()


class Configurator:

    def limit_concurrency(self, n):
        self
        log.info(f'最大并发数限制为 {n}，超过并发限制的请求会返回 503 Service Unavailable')
        current_app.config['OPENBAYES_SERVING_UVICORN_CONFIG']['limit_concurrency'] = n


INIT_ARG_HANDLERS = [ConfigInit]
