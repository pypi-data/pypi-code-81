import functools
import os
import subprocess

import fitlog
from loguru import logger

from fastutil.model.model_util import log_module_var

fitlog_config = """
[fit_settings]
watched_rules = *.py,*.sh,*.dic,*.dict,*.conf,*.config

[log_settings]
default_log_dir = ./fitlog
"""


def init_fitlog():
    is_exist_logs = os.path.exists('logs')
    is_exist_main = os.path.exists('main.py')
    cmd_res = subprocess.getoutput('fitlog init --no-git --hide')
    logger.info(cmd_res)
    if not is_exist_logs:
        os.remove('logs')
    if not is_exist_main:
        os.remove('main.py')
    os.mkdir('fitlog')
    with open('.fitlog/.fitconfig', 'w') as f:
        f.write(fitlog_config)


def fitlog_commit(msg=None):
    fitlog.commit(os.getcwd(), msg)
    fit_id = fitlog.get_fit_id(os.getcwd())
    logger.info('fit_id:{}'.format(fit_id))
    return fit_id


def fitlog_record(*, config_module=None, ver_dir):
    def wrapper(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            log_module_var(config_module, ver_dir)
            if config_module is not None:
                fitlog.add_hyper_in_file(config_module._file__)
            rng_seed = fitlog.set_rng_seed()
            logger.info('rng_seed:{}'.format(rng_seed))
            result = func(*args, **kwargs)
            fitlog.finish()
            return result

        return wrapped

    return wrapper
