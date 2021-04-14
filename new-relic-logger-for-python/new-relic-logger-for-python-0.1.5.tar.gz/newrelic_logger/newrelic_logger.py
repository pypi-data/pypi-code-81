import logging
import os
import queue
from logging.handlers import QueueListener

import newrelic.agent

from newrelic_logger.handlers import NewRelicLogHandler, NewRelicQueueHandler


class NewRelicLogger:
    def __init__(
        self,
        app_id: int = 0,
        app_name: str = None,
        license_key: str = None,
        region: str = "US",
        log_level=logging.INFO,
    ):
        app_id = int(os.environ.get("NEW_RELIC_APP_ID", app_id))
        app_name = os.environ.get("NEW_RELIC_APP_NAME", app_name)
        license_key = os.environ.get("NEW_RELIC_LICENSE_KEY", license_key)
        region = os.environ.get("NEW_RELIC_REGION", region)

        # instantiate queue & attach it to handler
        log_queue = queue.Queue(-1)
        queue_handler = NewRelicQueueHandler(log_queue)

        # Instantiate a new log handler
        remote_handler = NewRelicLogHandler(
            app_id=app_id,
            app_name=app_name,
            license_key=license_key,
            region=region,
            level=log_level,
        )

        # instantiate listener
        remote_listener = QueueListener(
            log_queue, remote_handler, respect_handler_level=True
        )

        # Instantiate the log formatter and add it to the log handler
        remote_handler.setFormatter(newrelic.agent.NewRelicContextFormatter())

        # Get the root logger and add the handler to it
        logging.getLogger().addHandler(queue_handler)
        logging.getLogger().setLevel(log_level)
        # start the listener
        remote_listener.start()
