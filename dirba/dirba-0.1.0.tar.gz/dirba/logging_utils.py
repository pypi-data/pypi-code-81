import logging

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration


def configure_logging(enable_additional_debug=True):
    """
    Отключает дебаг информацию для библиотек, при необходимости
    """
    while len(logging.root.handlers) > 0:
        logging.root.removeHandler(logging.root.handlers[-1])

    logging.getLogger('AdditionalDebug').info('enabled')
    if not enable_additional_debug:
        logging.getLogger('websockets.protocol:server').setLevel(logging.ERROR)
        logging.getLogger('websockets.protocol').setLevel(logging.ERROR)
        logging.getLogger('databases').setLevel(logging.ERROR)
        logging.getLogger('sqlalchemy.engine.base.Engine').setLevel(logging.ERROR)
        logging.getLogger('aiokafka.consumer.group_coordinator').setLevel(logging.ERROR)
        logging.getLogger('aiokafka.consumer.group_coordinator').setLevel(logging.ERROR)
        logging.getLogger('aiokafka.consumer.group_coordinator').setLevel(logging.ERROR)
        logging.getLogger('aiokafka.conn').setLevel(logging.ERROR)
        logging.getLogger('aiokafka.consumer.fetcher').setLevel(logging.ERROR)
    else:
        logging.getLogger('sqlalchemy.engine.base.Engine').setLevel(logging.INFO)


def set_logging(level=logging.DEBUG, enable_additional_debug: bool = True,
                sentry_url: str = None, environment: str = 'TEST_LOCAL', sample_rate: float = 1.0):
    """
    Устанавливает конфигурацию для логиирования.

    Необходимо вызывать как можно раньше
    :param level: уровень выводимых логов
    """

    configure_logging(enable_additional_debug=enable_additional_debug)
    logging.basicConfig(level=level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    if sentry_url:
        sentry_logging = LoggingIntegration(
            level=level,
            event_level=logging.ERROR
        )

        sentry_sdk.init(
            sentry_url,
            traces_sample_rate=sample_rate,
            environment=environment,
            integrations=[sentry_logging]
        )
