import logging
from datetime import datetime

from requests import Response

from pvoutput_publisher.base.service import ResponseDataHandler, Service
from pvoutput_publisher.publisher import publish


class RateLimitService(Service):

    def __init__(self):
        super().__init__()
        self.headers["X-Rate-Limit"] = "1"

    @property
    def url(self):
        return "https://pvoutput.org/service/r2/getsystem.jsp"

    @property
    def data(self):
        return {}


class RateLimitResponse(ResponseDataHandler):
    def __init__(self):
        self._reset = None
        self._remaining = None
        self._limit = None

    @property
    def limit(self):
        return self._limit

    @property
    def remaining(self):
        return self._remaining

    @property
    def reset(self):
        return self._reset

    @property
    def reset_human(self):
        reset_datetime = datetime.fromtimestamp(self._reset)
        return "{} in {}".format(reset_datetime, (reset_datetime - datetime.now()))

    def handle(self, response: Response):
        self._limit = int(response.headers['X-Rate-Limit-Limit'])
        self._remaining = int(response.headers['X-Rate-Limit-Remaining'])
        self._reset = int(response.headers['X-Rate-Limit-Reset'])


def example(system_id: str, secret_api_key: str):
    logging.info("Example of rate limit service")
    rate_service = RateLimitService()
    rate_response = RateLimitResponse()
    rate_service.set_system(system_id=system_id, secret_api_key=secret_api_key)
    publish(rate_service, data_handler=rate_response)
    print(f"limit: {rate_response.limit}")
    print(f"remaining: {rate_response.remaining}")
    print(f"reset: {rate_response.reset}")
    print(f"reset human: {rate_response.reset_human}")
