import inspect
import logging
import os
import re
import sys


class NonOverwriteDict(dict):
    def __setitem__(self, key, value):
        if self.__contains__(key):
            pass
        else:
            dict.__setitem__(self, key, value)


def varname(var):
    """
    https://stackoverflow.com/questions/592746/how-can-you-print-a-variable-name-in-python
    通过调用这个函数时traceback得到code_content，re到需要的var name
    Traceback(filename='<ipython-input-37-5fa84b05d0d4>', lineno=2, function='<module>', code_context=['b = varname(a)\n'], index=0)
    拿到varname(...)里的内容
    """
    for line in inspect.getframeinfo(inspect.currentframe().f_back)[3]:
        m = re.search(r'\bvarname\s*\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)', line)
    if m:
        return m.group(1)


def stdout_file_logger(
        name='root',
        log_path=None,
        log_level=logging.DEBUG,
        log_format='[%(asctime)s] - [%(name)s] - [%(levelname)s]\n%(message)s',
        reset_handlers=True
):
    logger = logging.getLogger(name)

    if len(logger.handlers) > 0:
        if reset_handlers:
            for h in logger.handlers:
                logger.removeHandler(h)
        else:
            return logger

    logger.setLevel(log_level)

    formatter = logging.Formatter(log_format)

    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    stdout_handler.setLevel(log_level)
    stdout_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)

    if log_path is not None:
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def load_py_file(file_path):
    file_dir = os.path.dirname(file_path)
    file_name = os.path.basename(file_path)
    file_name_no_suffix = os.path.splitext(os.path.basename(file_name))[0]
    sys.path.insert(-1, file_dir)
    content = {}
    try:
        exec(f'import py file {file_name}', {}, content)
    except ModuleNotFoundError:
        raise FileNotFoundError(f'Not find the input file {file_name} with basename {file_name_no_suffix} in {file_dir}')
    return content['content']
