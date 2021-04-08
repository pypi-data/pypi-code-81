import logging
from dataclasses import dataclass

import requests
from requests import Response
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from pvoutput_publisher.services.common.common import SystemDetails, Data
from pvoutput_publisher.services.service_factory import create_service

logger = logging.getLogger(__name__)


@dataclass
class PvRequest:
    params: dict
    service_name: str


@dataclass
class PvResponse:
    response: Response


def _publish(params: dict, url: str, system: SystemDetails) -> Response:
    headers = {'X-Pvoutput-SystemId': system.system_id,
               'X-Pvoutput-Apikey': system.api_key}

    init_retry_behaviour()
    logger.info("Publishing to %s: %s", url, str(params))
    resp = requests.post(url, data=params, headers=headers)
    if resp.ok:
        return resp
    else:
        logger.warning("")
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


def publish_data(service_name: str, data: Data, system: SystemDetails, url: str) -> Data:
    service = create_service(service_name)
    params = service.create_request(data, url, system)
    response = _publish(params, url, system)
    return service.parse_response(response.text, response)
