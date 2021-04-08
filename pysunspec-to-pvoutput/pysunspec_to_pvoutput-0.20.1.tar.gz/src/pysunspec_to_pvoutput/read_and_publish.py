import logging

from pvoutput_publisher.services.status.add_status_service import AddStatus
from pysunspec_read.read_to_output import read_with_clean
from requests import HTTPError
from sunspec2.modbus.modbus import ModbusClientError
from tenacity import retry, retry_if_exception_type, stop_after_attempt
from typing import Callable

from pysunspec_to_pvoutput.add_status import publish, basic_add_status
from pysunspec_to_pvoutput.config import Config, PvOutputOptions

logger = logging.getLogger(__name__)


@retry(stop=stop_after_attempt(2), retry=retry_if_exception_type(ModbusClientError))
def read_with_retry(config: Config):
    read_with_clean(config.connect_options, config.output_options)


@retry(stop=stop_after_attempt(2), retry=retry_if_exception_type(HTTPError))
def publish_with_retry(add_status_creator, config: Config):
    publish(add_status_creator, config)


def read_and_publish_add_status(config: Config,
                                add_status_creator: Callable[[dict, PvOutputOptions], AddStatus]
                                = basic_add_status(101, "W", "WH", "PhVphA")):
    try:
        read_with_retry(config)
    except ModbusClientError as e:
        logger.error("Error reading from device: %s", e)

    # there may be cached files still to upload so even if read failed we still want to progress to publishing
    try:
        publish_with_retry(config=config, add_status_creator=add_status_creator)
    except HTTPError as e:
        logger.error("Error publishing to pvoutput: %s", e.response.content)
        raise

