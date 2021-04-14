import json
import logging
import time
from logging.handlers import QueueHandler

import newrelic.agent
import requests


class NewRelicQueueHandler(QueueHandler):
    def prepare(self, record):
        self.format(record)

        record.msg = record.message
        record.args = newrelic.agent.get_linking_metadata()
        record.exc_info = None
        return record


class NewRelicLogHandler(logging.Handler):
    """
    A class which sends records to a New Relic via its API.
    """

    def __init__(
        self, level, app_id: int, app_name: str, license_key: str, region: str = "US"
    ):
        """
        Initialize the instance with the region and license_key
        """
        logging.Handler.__init__(self, level=level)
        self.app_id = app_id
        self.app_name = app_name
        self.host_us = "log-api.newrelic.com"
        self.host_eu = "log-api.eu.newrelic.com"
        self.url = "/log/v1"
        self.region = region.upper()
        self.license_key = license_key

    def emit(self, record):
        """
        Emit a record.
        Send the record to the New Relic API
        """
        try:
            import urllib.parse

            print(f"{record.getMessage()}")
            data_formatted_dict = json.loads(self.format(record))
            data = {
                **data_formatted_dict,
                "appId": self.app_id,
                "labels": {"app": self.app_name},
                **record.args,
            }

            self.send_log(data=data)

        except Exception:
            self.handleError(record)

    def send_log(self, data: {}):
        host = self.host_us if self.region == "US" else self.host_eu
        resp = requests.post(
            url="https://" + host + self.url,
            headers={"X-License-Key": self.license_key},
            json=data,
        )
        if not resp.ok:
            if resp.status_code == 429:
                print(f"New Relic API Response: Retry-After")
                time.sleep(1)
                self.send_log(data=data)
                return
            print(f"Error sending log to new relic")
            print(f"Status Code: {resp.status_code}")
            print(f"url: {resp.request.url}")
            print(resp.json())
            print(f"data: {resp.request.body}")
