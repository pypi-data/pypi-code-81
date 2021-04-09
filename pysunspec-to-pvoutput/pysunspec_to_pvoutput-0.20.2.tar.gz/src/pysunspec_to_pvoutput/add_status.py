import logging
from pathlib import Path
from typing import List, Callable

from pvoutput_publisher.services.add_batch_status import AddBatchStatus, publish_add_batch_status
from pvoutput_publisher.services.add_status import AddStatus, publish_add_status

from pysunspec_to_pvoutput.config import PvOutputOptions, Config
from pysunspec_to_pvoutput.file_utils.file_cache import FileProcessCache, move_to_completed
from pysunspec_to_pvoutput.file_utils.json_utils import read_json_dict_from_file, get_reading_date, get_model_value

logger = logging.getLogger(__name__)


def basic_add_status(model_id: int, power_id: str, energy_id: str, voltage_id: str) \
        -> Callable[[dict, PvOutputOptions], AddStatus]:
    def add_status(reading: dict, options: PvOutputOptions) -> AddStatus:
        date, time = get_reading_date(reading)
        status = AddStatus(date=date,
                           time=time,
                           power_generation=max(0, get_model_value(model_id, power_id, reading)),
                           energy_generation=get_model_value(model_id, energy_id, reading),
                           voltage=get_model_value(model_id, voltage_id, reading),
                           cumulative_flag=options.cumulative_flag
                           )
        return status

    return add_status


def convert_to_batch(reading_files: List[Path],
                     options: PvOutputOptions,
                     add_status_creator: Callable[[dict, PvOutputOptions], AddStatus]):
    statuses = AddBatchStatus()
    for reading_file in reading_files:
        reading_json = read_json_dict_from_file(reading_file)
        status = add_status_creator(reading_json, options)
        statuses.add_status(status)
    return statuses


def publish(add_status_creator, config: Config):
    publish_config = config.pvoutput_publish_options
    api_key = publish_config.secret_api_key
    system_id = str(publish_config.system_id)
    is_donation_mode = publish_config.is_donation_mode
    cache = FileProcessCache(determine_cache_path(config))
    reading_files = cache.load()

    if cache.size() > 1:
        readings_batch = reading_files[:publish_config.publish_limit]
        logger.info("Multiple readings found in cache directory, processing batch of {}".format(len(readings_batch)))
        for f in readings_batch:
            logger.info(f"Batch File {f}")
        statuses = convert_to_batch(readings_batch, publish_config, add_status_creator)
        response = publish_add_batch_status(system_id, api_key, statuses, is_donation_mode)
        for reading in response.reading_responses:
            print("response date {} time {} result {}".format(reading.reading_date, reading.reading_time,
                                                              reading.status_added))
        move_to_completed(readings_batch, cache)
    elif cache.size() == 1:
        logger.info(f"Single reading found in cache directory {reading_files[0]}")
        reading_json = read_json_dict_from_file(reading_files[0])
        status = add_status_creator(reading_json, publish_config)
        publish_add_status(system_id, api_key, status, is_donation_mode)
        logger.info("Single reading was published")
        move_to_completed([reading_files[0]], cache)
    else:
        logger.info(f"No readings in cache location, all caught up, cache: {publish_config.cache_path}")


def determine_cache_path(config):
    maybe_cache_dir = config.output_options.output_file_path
    if ".json" in maybe_cache_dir.name:
        return maybe_cache_dir.parent
    else:
        return maybe_cache_dir
