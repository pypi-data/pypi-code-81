import functools
import os
import signal
from loguru import logger
from ..tool import git_util, file_util
import shutil


def log_module_var(module):
    print('param-----------------------------------------------param')
    param_list = []
    if isinstance(module, str):
        with open(module) as f:
            for line in f:
                param_list.append(line)
    else:
        for k, v in vars(module).items():
            if k.startswith('__'):
                continue
            if isinstance(v, (int, float, bool, str, dict, tuple, list, set)):
                print('{}:{}'.format(k, v))
                param_list.append('{}:{}'.format(k, v))
    print('param-----------------------------------------------param')
    return param_list


def log_record(config_module=None, config_file=None, save_dir=None,
               trace_log_name=None, trace_email=None, trace_interval_min=120,
               debug=False):
    """
    记录配置文件到日志和保存目录，创建或清理保存的目录
    """

    def clean_file():
        if debug:
            if os.path.exists(save_dir):
                shutil.rmtree(save_dir)
            ver_id = git_util.get_ver_id(raise_exception=False)
            data_ver_id = git_util.get_date_ver_id(raise_exception=False)
            file_list = file_util.get_log_file(os.getpid(), ver_id)
            file_list.extend(file_util.get_log_file(os.getpid(), data_ver_id))
            for file_path in file_list:
                if os.path.exists(file_path):
                    os.system('rm {}'.format(file_path))
        elif os.path.exists(save_dir) and len(os.listdir(save_dir)) == 0:
            os.rmdir(save_dir)

    def clean_handler(signum, frame):
        clean_file()
        exit()

    signal.signal(signal.SIGINT, clean_handler)
    signal.signal(signal.SIGQUIT, clean_handler)
    signal.signal(signal.SIGTERM, clean_handler)
    signal.signal(signal.SIGHUP, clean_handler)

    def wrapper(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            check_commit = not debug
            if check_commit and not git_util.is_git_commit():
                raise Exception('git is not committed'.format(save_dir))
            if os.path.exists(save_dir) and len(os.listdir(save_dir)) > 0:
                raise Exception('save_dir:{} is not empty'.format(save_dir))
            logger.info('pid:{}'.format(os.getpid()))
            logger.info('save_dir:{}'.format(save_dir))
            if not os.path.exists(save_dir):
                os.mkdir(save_dir)
            try:
                param_list = log_module_var(config_module or config_file)
                if trace_log_name and trace_email:
                    file_util.start_trace_log([trace_log_name], send_to=trace_email, interval_min=trace_interval_min)
                    logger.info('trace log started')
                func(*args, **kwargs)
                with open(os.path.join(save_dir, 'param.txt'), 'w') as param_f:
                    param_f.write('\n'.join(param_list))

                ver_id = git_util.get_ver_id(raise_exception=False)
                if ver_id:
                    log_file = 'log/{}.log'.format(ver_id)
                    if check_commit and os.path.exists(log_file):
                        shutil.copyfile(log_file, save_dir)
            except Exception as ex:
                clean_file()
                raise ex
            except (KeyboardInterrupt, SystemExit):
                clean_file()

        return wrapped

    return wrapper
