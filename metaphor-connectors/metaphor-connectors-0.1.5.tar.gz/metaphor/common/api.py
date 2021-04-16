import logging
from dataclasses import dataclass
from typing import List

from dataclasses_json import dataclass_json
from requests import HTTPError, post

from .sink import Sink

logger = logging.getLogger()
logger.setLevel(logging.INFO)


@dataclass_json
@dataclass
class IngestionApiConfig:
    url: str
    api_key: str
    timeout: int = 3  # default 3 seconds timeout


class IngestionApi(Sink):
    """Ingestion API sink functions"""

    def __init__(self, config: IngestionApiConfig):
        self._url = config.url
        self._post_header = {"x-api-key": config.api_key}
        self._timeout = config.timeout

    def _sink(self, messages: List[dict]) -> None:
        """Post messages to Ingestion API"""
        for message in messages:
            response = None
            try:
                response = post(
                    self._url,
                    json=message,
                    headers=self._post_header,
                    timeout=self._timeout,
                )

                # If the response was successful, no Exception will be raised
                response.raise_for_status()
                logger.debug(f"POST response {response.text}")
            except HTTPError as http_error:
                logger.error(f"HTTP error {http_error}, response {response.text}")
            except Exception as error:
                logger.error(f"POST error: {error}, response {response.text}")

        logger.info(f"Posted {len(messages)} messages")
