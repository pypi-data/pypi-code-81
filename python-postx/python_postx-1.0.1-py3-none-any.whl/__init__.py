import requests


class TransmissionError(Exception):
    """
    Raised when the service did not recieve a valid response.
    """


class BaseService():
    def __init__(self):
        pass

    def send(self, url, message):
        msg = self._build_message(message)
        self._send(url, msg)

    def _build_message(self, message):
        pass

    def _send(send, url, body):
        resp = requests.post(url, json=body)
        if resp.status_code == 200:
            return True
        else:
            raise TransmissionError


from . import teams_service    # noqa
from . import slack_service    # noqa