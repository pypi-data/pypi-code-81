import logging
import os
import configparser
from loguru import logger

DEBUG = True
config = configparser.ConfigParser()


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def __init_scheduler_log():
    ap_lg = logging.getLogger('apscheduler.scheduler')
    if DEBUG:
        ap_lg.setLevel(logging.DEBUG)
    else:
        ap_lg.setLevel(logging.INFO)
    ap_lg.handlers.append(InterceptHandler())


def __init_log(log_path: str = None, enqueue=False, trace_id=False):
    if not log_path:
        raise Exception('log path is None')
    log_path = os.path.abspath(log_path)
    if log_path.endswith('.log'):
        log_error_path = log_path[:-4] + '_error' + '.log'
    else:
        log_error_path = log_path + '_error'
    logger.info('log path:{}', log_path)
    logger.info('log error path:{}', log_error_path)

    log_config = {'enqueue': enqueue, 'rotation': '00:00', 'retention': '2 weeks', 'compression': 'tar.gz'}
    if trace_id:
        extra_format = '{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {name}:{function}:{line} - [{extra[ID]}] {message}'
        log_config['format'] = extra_format
    if DEBUG:
        logger.add(log_path, level='DEBUG', **log_config)
    else:
        logger.remove()
        logger.add(log_path, level='INFO', **log_config)
    logger.add(log_error_path, level='ERROR', **log_config)
    __init_scheduler_log()


def __set_debug(debug_flag):
    if debug_flag is None:
        raise Exception('需要设置DEBUG环境变量，确定是否生产环境')
    global DEBUG
    if isinstance(debug_flag, str) and debug_flag == '0':
        DEBUG = False
    if isinstance(debug_flag, int) and debug_flag == 0:
        DEBUG = False
    if isinstance(debug_flag, bool):
        DEBUG = debug_flag
    logger.info(f'DEBUG:{DEBUG}')


def __init_config(conf_path):
    if not conf_path:
        raise Exception('conf path is None')
    conf_path = os.path.abspath(conf_path)
    logger.info('load config file:{}'.format(conf_path))
    config.read(conf_path, encoding='utf-8')


def init(log_path, conf_path=None, debug=None):
    __set_debug(debug)
    if conf_path:
        __init_config(conf_path)
    __init_log(log_path)
