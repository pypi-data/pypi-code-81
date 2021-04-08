"""
日志设置
装饰器：@logger.catch(logger.exception) @log_print @log_in_out
添加额外信息：extra参数 logger.bind logger.patch,format="{extra[ip]}"
日志统计分析：logger.parse 日志传输和邮件：nb_log
协程函数内需要调用logger.complete,tqdm兼容：logger.add(lambda msg: tqdm.write(msg, end=""))
"""
import logging
import os
from loguru import logger
import functools
import time
import contextlib
from fastutil.tool import message_util
import datetime as dt

LOGURU_EXTRA_FORMAT = '{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {name}:{function}:{line} - [{extra[ID]}] {message}'


def add_path(log_path: str = None, enqueue=False, trace_id=False):
    debug = os.environ.get('DEBUG')
    if not log_path:
        raise Exception('log path is None')
    log_path = os.path.abspath(log_path)
    if log_path.endswith('.log'):
        log_error_path = log_path[:-4] + '_error' + '.log'
    else:
        log_error_path = log_path + '_error'
    logger.info('log_path:{}'.format(log_path))
    logger.info('log_error_path:{}'.format(log_error_path))

    log_config = {'enqueue': enqueue, 'rotation': '00:00', 'retention': '2 weeks', 'compression': 'zip'}
    if trace_id:
        log_config['format'] = LOGURU_EXTRA_FORMAT
        logger.configure(patcher=lambda record: record['extra'].update(
            ID=os.getpid()) if not record['extra'].get('ID') else None)

    if debug and int(debug) != 0:
        logger.add(log_path, level='DEBUG', **log_config)
    else:
        logger.remove()
        logger.add(log_path, level='INFO', **log_config)
    logger.add(log_error_path, level='ERROR', **log_config)


def add_email(title, to, level='ERROR', interval=None):
    logger.add(EmailHandler(title, to, interval), level=level.upper())


# 重定向print
class StreamToLogger:
    def __init__(self, level="INFO"):
        self._level = level

    def write(self, buffer):
        for line in buffer.rstrip().splitlines():
            logger.opt(depth=1).log(self._level, line.rstrip())

    def flush(self):
        pass


stream = StreamToLogger()


def log_print():
    def wrapper(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            with contextlib.redirect_stdout(stream):
                result = func(*args, **kwargs)
            return result

        return wrapped

    return wrapper


# 记录输入、输出和耗时
def log_in_out(*, log_time=True, log_in=True, log_out=True, level="INFO"):
    """
    转移print输出到loguru
    """

    def wrapper(func):
        name = func.__name__

        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            logger_ = logger.opt(depth=1)
            if log_in:
                logger_.log(level, '{} input: args={}, kwargs={}', name, args, kwargs)
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            if log_out:
                logger_.log(level, "{} output: {}", name, result)
            if log_time:
                logger_.log(level, "{} cost: {}", name, end_time - start_time)
            return result

        return wrapped

    return wrapper


class InterceptHandler(logging.Handler):
    """
    转移logging的日志到loguru
    """

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


# 邮件发送
class EmailHandler:
    def __init__(self, title, to, interval_min=None, line_num=50):
        self.title = title
        self.interval_min = interval_min
        self.cur_date = dt.datetime.now()
        self.send_ct = 0
        self.to = to
        self.info_list = []
        self.line_num = line_num

    def write(self, message):
        if self.interval_min:
            self.info_list.append(str(message))
            if len(self.info_list) > self.line_num:
                self.info_list.pop(0)
            total_minutes = (dt.datetime.now() - self.cur_date).total_seconds() / 60
            if total_minutes / self.interval_min < self.send_ct:
                return
            info_msg = '\n'.join(self.info_list)
            message_util.send_email(self.title, info_msg, self.to)
            self.send_ct += 1
            self.info_list = []
        else:
            message_util.send_email(self.title, message, self.to)
