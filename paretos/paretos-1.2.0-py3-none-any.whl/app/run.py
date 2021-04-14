import logging
import multiprocessing
from os import name as os_name

from ..config import Config
from .create_app import create_app


def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


def import_application():
    import paretos.app.src.Application as app

    return app


def run(config: Config):
    data_source = config.get_data_source_name()
    app = create_app(data_source)

    # TODO Gunicorn needs python package fcntl which is not available on windows
    if os_name == "nt":
        app.run()
    else:
        logger = config.get_logger()
        options = {
            "bind": "%s:%s"
            % (config.get_dashboard_host(), config.get_dashboard_port()),
            "workers": number_of_workers(),
            "loglevel": logging.getLevelName(logger.getEffectiveLevel()),
        }
        application_module = import_application()

        application = application_module.Application(app, options)
        application.run()
