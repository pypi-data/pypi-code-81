from logging import Handler

from applipy import Config

from newrelic_telemetry_sdk import (
    Log,
    LogClient,
)


class NewRelicLogHandler(Handler):

    _client: LogClient

    def __init__(self, client: LogClient, config: Config) -> None:
        super().__init__()
        self._client = client
        self._app_name = config.get('app.name')

    def emit(self, record):
        log = Log.from_record(record)
        log['app_name'] = self._app_name
        self._client.send(log).raise_for_status()
