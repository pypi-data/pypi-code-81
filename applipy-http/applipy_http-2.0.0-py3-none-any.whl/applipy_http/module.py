import logging

from aiohttp import web

from applipy import Config, LoggingModule, Module
from applipy_inject import with_names
from applipy_http.config import ServerConfig
from applipy_http.server import HttpServer


def _app_runner_wrapper(name, logging_conf):
    def _builder(app: web.Application, logger: logging.Logger) -> web.AppRunner:
        if name is None:
            infix = ''
        else:
            infix = f'.{name}'
        server_logger = logger.getChild(f'http{infix}.aiohttp.server')
        if 'server.level' in logging_conf:
            server_logger.setLevel(logging_conf['server.level'])

        access_logger = logger.getChild(f'http{infix}.aiohttp.access')
        if 'access.level' in logging_conf:
            access_logger.setLevel(logging_conf['access.level'])

        return web.AppRunner(app,
                             logger=server_logger,
                             access_log=access_logger,
                             access_log_format=logging_conf.get('access.format', web.AccessLogger.LOG_FORMAT))
    return _builder


def _aiohttp_application_builder(name):
    def _builder(logger: logging.Logger) -> web.Application:
        if name is None:
            infix = ''
        else:
            infix = f'.{name}'
        return web.Application(logger=logger.getChild(f'http{infix}.aiohttp.server'))

    return _builder


class HttpModule(Module):

    def __init__(self, config: Config):
        self.config = config

    def configure(self, bind, register):
        for server in self.config.get('http.servers', []):
            name = server.get('name')
            host = server['host']
            port = server['port']
            logging_conf = server.get('logging', {})
            bind(_aiohttp_application_builder(name), name=name)
            bind(web.AppRunner,
                 with_names(_app_runner_wrapper(name, logging_conf), {'app': name}),
                 name=name)
            bind(ServerConfig, ServerConfig(name, host, port), name=name)

            register(with_names(HttpServer, {'app_runner': name,
                                             'apis': name,
                                             'config': name}))

    @classmethod
    def depends_on(cls):
        return LoggingModule,
