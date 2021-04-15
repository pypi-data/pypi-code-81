"""Flask Logging Request

"""

import logging


class FlaskRequestLogFormatter(logging.Formatter):

    def __init__(self, *args, **kwargs):
        super(FlaskRequestLogFormatter, self).__init__(*args, **kwargs)

    def init_app(self, app):
        conf = app.config.get('FLASK_REQUEST_LOGGING', {})

    def format(self, record):
        return super(FlaskRequestLogFormatter, self).format(record)

