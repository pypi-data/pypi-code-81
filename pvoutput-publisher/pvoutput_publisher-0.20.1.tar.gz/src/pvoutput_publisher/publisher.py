import logging

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from pvoutput_publisher.base.service import ResponseDataHandler, Service

logger = logging.getLogger(__name__)


def publish(service: Service, data_handler: ResponseDataHandler):
    logger.info(f"Publishing url:{service.url}, data:{service.data}")
    resp = requests.post(service.url, data=service.data, headers=service.headers)
    if resp.ok:
        logger.info(f"Publish returned successful status code {resp.status_code}")
        data_handler.handle(resp)
        return resp
    else:
        logger.error(f"Error publishing {resp.status_code} {resp.reason}")
        resp.raise_for_status()


def init_retry_behaviour():
    retry_strategy = Retry(
        total=3,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS", "POST"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)
