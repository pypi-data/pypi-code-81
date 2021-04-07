"""
Logging configuration management.
"""
import logging
import logging.config
from pathlib import Path
from big.utils.strutil import trim_to_lower
from .config import load_config_from_file

INI_FILE_FORMAT = '.ini'
SUPPORTED_FORMATS = {'.yaml', '.yml', '.json', '.ini'}


def configure_logging(config_file_path, disable_existing_loggers=True):
    """
    Configures the logging subsystem using the JSON configuration provided in the specified file.

    :param config_file_path: a full (absolute) path of the configuration file.
    :param disable_existing_loggers: if False, loggers which exist when this call is made are left enabled.
    """
    logging.basicConfig(level="INFO")
    cfg_logger = logging.getLogger('config')
    cfg_logger.info('*** Initializing logging subsystem configuration')

    if not config_file_path:
        raise ValueError('Configuration file path is a required argument')

    ext = trim_to_lower(Path(config_file_path).suffix)
    if ext not in SUPPORTED_FORMATS:
        raise ValueError(f'Unknown extension [{ext}]. Must be one of {SUPPORTED_FORMATS}')

    cfg_logger.info('*** Logging configuration will be read from the [%s] file', config_file_path)
    if ext == INI_FILE_FORMAT:
        logging.config.fileConfig(config_file_path, disable_existing_loggers=disable_existing_loggers)
    else:
        cfg_dict = load_config_from_file(config_file_path)
        cfg_logger.info('*** Logging configuration loaded successfully')
        core_dict = cfg_dict.get('logging') or cfg_dict
        core_dict['disable_existing_loggers'] = disable_existing_loggers
        logging.config.dictConfig(core_dict)

    cfg_logger.info('*** Logging subsystem configured ***')
