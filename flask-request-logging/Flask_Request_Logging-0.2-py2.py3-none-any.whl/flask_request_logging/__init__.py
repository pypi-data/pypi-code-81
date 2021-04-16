"""Flask Logging Request

"""

import logging
from logging import getLogger, StreamHandler, Formatter, getLoggerClass, DEBUG, ERROR
from uuid import uuid4
from flask import g, request


REQUEST_LOG_FORMAT = '[%(request_id)s] %(levelname)s in %(module)s: %(message)s'


class RequestIDHandler(StreamHandler):
    def emit(self, record):
        record.request_id = g.request_id
        StreamHandler.emit(self, record)


def prepare_request_log(app):
    @app.before_request
    def request_log():
        g.request_id = request.headers.get(app.config['REQUEST_LOGGING_HEADER_ID_NAME'], uuid4().hex)

    request_handler = RequestIDHandler()
    request_handler.setLevel(DEBUG)
    request_handler.setFormatter(Formatter(REQUEST_LOG_FORMAT))

    del app.logger.handlers[:]
    app.logger.addHandler(request_handler)


def init_app(app):
    if app.config.get('REQUEST_LOGGING_OPEN', False):
        prepare_request_log(app)
    
    app.config['REQUEST_LOGGING_FORMAT']