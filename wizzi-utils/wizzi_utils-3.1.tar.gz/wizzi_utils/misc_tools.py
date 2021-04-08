import os
import datetime
from timeit import default_timer as timer
from typing import Callable
import cProfile
import pstats
import io
import numpy as np
import random
import inspect
import sys
import time
import pickle
from itertools import combinations

LINES = '-' * 80
CONST_COLOR_MAP = {
    'ResetAll': "\033[0m",
    'Bold': "\033[1m",
    'Dim': "\033[2m",
    'Underlined ': "\033[4m",
    'Blink      ': "\033[5m",
    'Reverse    ': "\033[7m",
    'Hidden     ': "\033[8m",

    'ResetBold': "\033[21m",
    'ResetDim': "\033[22m",
    'ResetUnderlined': "\033[24m",
    'ResetBlink': "\033[25m",
    'ResetReverse': "\033[27m",
    'ResetHidden': "\033[28m",

    'Default': "\033[39m",
    'Black': "\033[97m",
    'Red': "\033[31m",
    'Green': "\033[32m",
    'Yellow': "\033[33m",
    'Blue': "\033[34m",
    'Magenta': "\033[35m",
    'Cyan': "\033[36m",
    'LightGray': "\033[37m",
    'DarkGray': "\033[90m",
    'LightRed': "\033[91m",
    'LightGreen': "\033[92m",
    'LightYellow': "\033[93m",
    'LightBlue': "\033[94m",
    'LightMagenta': "\033[95m",
    'LightCyan': "\033[96m",
    'White': "\033[30m",

    'BackgroundDefault': "\033[49m",
    'BackgroundBlack': "\033[107m",
    'BackgroundRed': "\033[41m",
    'BackgroundGreen': "\033[42m",
    'BackgroundYellow': "\033[43m",
    'BackgroundBlue': "\033[44m",
    'BackgroundMagenta': "\033[45m",
    'BackgroundCyan': "\033[46m",
    'BackgroundLightGray': "\033[47m",
    'BackgroundDarkGray': "\033[100m",
    'BackgroundLightRed': "\033[101m",
    'BackgroundLightGreen': "\033[102m",
    'BackgroundLightYellow': "\033[103m",
    'BackgroundLightBlue': "\033[104m",
    'BackgroundLightMagenta': "\033[105m",
    'BackgroundLightCyan': "\033[106m",
    'BackgroundWhite': "\033[40m"
}


def get_timer_delta(start_timer: float) -> datetime.timedelta:
    """
    :param start_timer: begin time
    :return:
    time = get_timer()
    print('Total run time {}'.format(get_timer_delta(start_timer=time)))
    "Total run time 0:00:00.000026"
    """
    end_timer = get_timer()
    d = datetime.timedelta(seconds=(end_timer - start_timer))
    return d


def get_timer() -> float:
    return timer()


def timer_action(seconds: int, action: str = '', tabs: int = 1) -> None:
    """ counts till seconds or block"""
    if seconds is None:
        input('{}Press "Enter" key for {}...'.format(tabs * '\t', action))
    else:
        time_in_future = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
        print('{}{} IN: {}'.format(tabs * '\t', action, seconds), end='', flush=True)
        while time_in_future > datetime.datetime.now():
            time.sleep(1)
            seconds -= 1
            print(' {}'.format(seconds), end='', flush=True)
        print('')
    return


def get_current_date_hour() -> str:
    """
    running start time - good for long programs
    :return:
    """
    now = datetime.datetime.now()
    current_time = now.strftime('%d-%m-%Y %H:%M:%S')
    return current_time


def get_pc_name() -> str:
    """
    :return: pc name as str
    """
    import platform
    return platform.uname()[1]


def get_mac_address(add_semi_colons: bool = True) -> str:
    """
    :return: pc mac as str
    print(get_mac_address(add_semi_colons=True)) # 70:4D:7B:8A:65:EE
    print(get_mac_address(add_semi_colons=False)) # 704D7B8A65EE
    """
    from uuid import getnode as get_mac
    mac = get_mac()
    mac = "{:X}".format(mac)  # turn to Hex
    if add_semi_colons:
        mac = ':'.join(mac[i:i + 2] for i in range(0, 12, 2))
    return mac


def get_cuda_version() -> str:
    """
    :return: cuda version if found on environment variables
    """
    if 'CUDA_PATH' in os.environ:
        cuda_v = os.path.basename(os.environ['CUDA_PATH'])
    else:
        cuda_v = 'No CUDA_PATH found'
    return cuda_v


def make_cuda_invisible() -> None:
    """
        disable(the -1) gpu 0
        TODO support hiding multiple gpus
    """
    os.environ['CUDA_VISIBLE_DEVICES'] = '-1, 0'
    return


def start_profiler() -> cProfile.Profile:
    """
    starts profiling
    :return: profiling object that is needed for end_profiler()
    """
    pr = cProfile.Profile()
    pr.enable()
    return pr


def end_profiler(pr: cProfile.Profile, rows: int = 10) -> str:
    """
    profiling output
    :param pr: object returned from start_profiler()
    :param rows: how many rows to print sorted by 'cumulative' run time
    :return:
    """
    pr.disable()
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    ps.print_stats(rows)
    return s.getvalue()


def set_seed(seed: int = 42) -> None:
    """
    :param seed: setting numpy and random seeds
    :return:
    """
    np.random.seed(seed)
    random.seed(seed)
    return


def get_tensorflow_version() -> str:
    import tensorflow as tf
    string = '* TensorFlow Version {}'.format(tf.__version__)
    return string


def main_wrapper(
        main_function: Callable,
        cuda_off: bool = False,
        torch_v: bool = False,
        tf_v: bool = False,
        cv2_v: bool = False,
        with_profiler: bool = False
) -> None:
    """
    :param main_function: the function to run
    :param cuda_off: make gpu invisible and force run on cpu
    :param torch_v: print torch version
    :param tf_v: print tensorflow version
    :param cv2_v: print opencv version
    :param with_profiler: run profiler
    :return:
    """
    print(LINES)
    start_timer = get_timer()

    # make_cuda_invisible()
    print('main_wrapper:')
    print('* Run started at {}'.format(get_current_date_hour()))
    print('* Python Version {}'.format(sys.version))
    print('* Working Dir: {}'.format(os.getcwd()))
    print('* Computer Name: {}'.format(get_pc_name()))
    print('* Computer Mac: {}'.format(get_mac_address()))
    cuda_msg = '* CUDA Version: {}'.format(get_cuda_version())
    if cuda_off:
        make_cuda_invisible()
        cuda_msg += ' (Turned off)'
    print(cuda_msg)

    if torch_v:
        try:
            from wizzi_utils.torch_tools import get_torch_version
            print(get_torch_version())
        except (ImportError, ModuleNotFoundError, NameError) as err:
            string = '* {}'.format(err)
            print(string)
    if tf_v:
        try:
            print(get_tensorflow_version())
        except (ImportError, ModuleNotFoundError, NameError) as err:
            string = '* {}'.format(err)
            print(string)
    if cv2_v:
        try:
            from wizzi_utils.open_cv_tools import get_cv_version
            print(get_cv_version())
        except (ImportError, ModuleNotFoundError, NameError) as err:
            string = '* {}'.format(err)
            print(string)

    print('Function {} started:'.format(main_function))
    print(LINES)
    pr = start_profiler() if with_profiler else None
    main_function()
    if with_profiler:
        print(end_profiler(pr))
    print(LINES)
    print('Total run time {}'.format(get_timer_delta(start_timer)))
    return


def add_data(var, data_chars: int, float_precision: int = 0) -> str:
    """
    Aux function for to_str()
    :param var:
    :param data_chars:
    :param float_precision:
    :return:
    """

    if isinstance(var, (float, int)):
        if isinstance(var, float) and float_precision > 0:
            data_str_raw = '{:,}'.format(round(var, float_precision))
        else:
            data_str_raw = '{:,}'.format(var)
    else:
        data_str_raw = str(var)
    data_str_raw = data_str_raw.replace('\n', '').replace('  ', '')
    if data_chars == 0:  # all data
        data_chars = len(data_str_raw) + 1
    elif data_chars < 0:  # no data
        data_chars = 0
    # else keep positive chars

    data_str = ': {}'.format(data_str_raw[:data_chars])
    if len(data_str_raw) > data_chars > 0:
        data_str += ' ...too long'
    return data_str


def to_str(var, title: str, data_chars: int = 100, float_precision: int = 2) -> str:
    """
    :param var: the variable
    :param title: the title (usually variable name)
    :param data_chars: how many char to print.
        -1: none
         0: all
        +0: maximum 'data_chars' (e.g. data_chars=50 and |str(var)|=100 - first 50 chars)
    :param float_precision: round number if possible(float, np array...). 0 for no rounding

    examples:
        print(to_str(var=32223123123123123, title='my_int'))
        print(to_str(var=3.2, title='my_float'))
        print(to_str(var=1234567890.223123123123123123, title='my_long_float', float_precision=3))
        print(to_str(var='a', title='my_str'))
        print(to_str(var=[], title='my_empty_list'))
        print(to_str(var=[112312312, 3, 4], title='1d list of ints'))
        print(to_str(var=[1, 3123123], title='1d list of ints no data', data_chars=-1))  # no data
        print(to_str(var=[11235] * 1000, title='1d long list'))
        print(to_str(var=(1239, 3, 9), title='1d tuple'))
        print(to_str(var=[[1231.2123123, 15.9], [3.0, 7.55]], title='2d list'))
        print(to_str(var=[(1231.2123123, 15.9), (3.0, 7.55)], title='2d list of tuples'))
        b = np.array([[1231.123122, 15.9], [3.0, 7.55]])
        print(to_str(var=b, title='2d np array'))
        cv_img = np.zeros(shape=[480, 640, 3], dtype=np.uint8)
        print(to_str(var=cv_img, title='cv_img'))
        print(to_str(var={'a': [1213, 2]}, title='dict of lists'))
        print(to_str(var={'a': [{'k': [1, 2]}, {'c': [7, 2]}]}, title='nested dict'))
    :return: informative string of the variable
    """

    type_s = str(type(var)).replace('<class \'', '').replace('\'>', '')  # clean type name
    string = '{}({})'.format(title, type_s)  # base: title and type

    if isinstance(var, (int, float, str)):
        if hasattr(var, "__len__"):
            string = string.replace(')', ',len={})'.format(var.__len__()))
        string += add_data(var, data_chars, float_precision)

    elif isinstance(var, (list, tuple)):
        string = string.replace(')', ',len={})'.format(var.__len__()))
        string += add_data(var, data_chars)
        if len(var) > 0:  # recursive call
            string += '\n\t{}'.format(to_str(var=var[0], title='{}[0]'.format(title), data_chars=data_chars))

    elif isinstance(var, np.ndarray):
        string = string.replace(')', ',shape={},dtype={})'.format(var.shape, var.dtype))
        if var.dtype == np.float64 and float_precision > 0:
            string += add_data(np.round(var, float_precision).tolist(), data_chars, float_precision=0)
        else:
            string += add_data(var.tolist(), data_chars, float_precision=0)
        if len(var) > 0:  # recursive call
            string += '\n\t{}'.format(to_str(var=var[0], title='{}[0]'.format(title), data_chars=data_chars))

    elif isinstance(var, dict):
        string = string.replace(')', ',len={},keys={})'.format(var.__len__(), list(var.keys())))
        string += add_data(var, data_chars)
        if len(var) > 0:  # recursive call
            first_key = next(iter(var))
            string += '\n\t{}'.format(
                to_str(var=var[first_key], title='{}[{}]'.format(title, first_key), data_chars=data_chars))

    else:  # all unidentified elements get default print (title(type): data)
        string += add_data(var, data_chars)
    return string


def save_np(t: np.array, path: str, ack_print: bool = True, tabs: int = 0):
    """
    to save a dict - see np.savez(path, name1=a, name2=b ... ) - loading the same
    :param t: numpy array
    :param path: suffix '.npy' added automatically
    :param ack_print:
    :param tabs:
    :return:
    """
    np.save(path, t)
    if ack_print:
        print('{}Saved to: {}'.format(tabs * '\t', path))
    return


def load_np(path: str, ack_print: bool = True, tabs: int = 0) -> np.array:
    """
    :param path:
    :param ack_print:
    :param tabs:
    :return: numpy array
    """
    t = np.load(path)
    if ack_print:
        print('{}Loaded: {}'.format(tabs * '\t', path))
    return t


def save_pkl(path: str, data_dict: dict, ack: bool = True, tabs: int = 0) -> None:
    file_obj = open(path, "wb")
    pickle.dump(data_dict, file_obj)
    file_obj.close()
    if ack:
        print('{}Saved to: {}'.format(tabs * '\t', path))
    return


def load_pkl(path: str, ack: bool = True, tabs: int = 0) -> dict:
    file_obj = open(path, "rb")
    data_dict = pickle.load(file_obj)
    file_obj.close()
    if ack:
        print('{}Loaded: {}'.format(tabs * '\t', path))
    return data_dict


def get_uniform_dist_by_dim(A):
    lows = np.min(A, axis=0)
    highs = np.max(A, axis=0)
    return lows, highs


def get_normal_dist_by_dim(A):
    means = np.mean(A, axis=0)
    stds = np.std(A, axis=0)
    return means, stds


def np_normal(shape: tuple, mius: list, stds: list) -> np.array:
    """
    e.g.
        d = 2
        A = np.zeros((3, d))
        A[0][0], A[0][1] = 0, 1000
        A[1][0], A[1][1] = 1, 2000
        A[2][0], A[2][1] = 5, 4000
        means, stds = get_normal_dist_by_dim(A)
        print(means, stds)
        A_2 = np_normal(shape=(500, d), mius=means, stds=stds)
        print(A_2.shape)
        print(get_normal_dist_by_dim(A_2))
    """
    ret = np.random.normal(loc=mius, scale=stds, size=shape)
    return ret


def np_uniform(shape: tuple, lows: [list, int], highs: [list, int]) -> np.array:
    """
    e.g.
        d=2
        A = np.zeros((3, d))
        A[0][0], A[0][1] = 0, 1000
        A[1][0], A[1][1] = 1, 2000
        A[2][0], A[2][1] = 5, 4000
        lows, highs = get_uniform_dist_by_dim(A)
        print(lows, highs)
        A_2 = np_uniform(shape=(10, d), lows=lows, highs=highs)
        print(A_2.shape)
        print(get_normal_dist_by_dim(A_2))
    """
    ret = np.random.uniform(low=lows, high=highs, size=shape)
    return ret


def np_random_integers(low: int, high: int, size: tuple) -> np.array:
    ret = np.random.random_integers(low=low, high=high, size=size)
    return ret


def augment_x_y_numpy(X: np.array, y: np.array) -> np.array:
    """ creates A=X|y """
    assert X.shape[0] == y.shape[0], 'row count must be the same'
    if len(X.shape) == 1:  # change x size()=[n,] to size()=[n,1]
        X = X.reshape(X.shape[0], 1)
    if len(y.shape) == 1:  # change y size()=[n,] to size()=[n,1]
        y = y.reshape(y.shape[0], 1)
    A = np.column_stack((X, y))
    return A


def de_augment_numpy(A: np.array) -> (np.array, np.array):
    """ creates X|y=A """
    if len(A.shape) == 1:  # A is 1 point. change from size (n) to size (1,n)
        A = A.reshape(1, A.shape[0])
    X, y = A[:, :-1], A[:, -1]
    if len(X.shape) == 1:  # change x size()=[n,] to size()=[n,1]
        X = X.reshape(X.shape[0], 1)
    if len(y.shape) == 1:  # change y size()=[n,] to size()=[n,1]
        y = y.reshape(y.shape[0], 1)
    return X, y


def nCk(n: int, k: int, as_int: bool = False):
    """
    n choose k
    :return: if as_int True: the result of nCk, else the combinations of nCk

    e.g.
    A = np.random.randint(low=-10, high=10, size=(3, 2))
    print('A={}'.format(A.tolist()))

    # let's iterate on every 2 different indices of A
    combs_count = utils.nCk(len(A), k=2, as_int=True)
    print('|A| choose 2={}:'.format(combs_count)) # result is 3

    combs_list = utils.nCk(len(A), k=2)  # result is [[0, 1], [0, 2], [1, 2]]
    for i, comb in enumerate(combs_list):
        print('\tcomb {}={}. A[comb]={}'.format(i, comb, A[comb].tolist()))
    """
    range_list = np.arange(0, n, 1)
    combs = list(combinations(range_list, k))
    combs = [list(comb) for comb in combs]
    if as_int:
        combs = len(combs)
    return combs


def redirect_std_start():
    """
    redirect all prints to summary_str
    e.g.
        old_stdout, summary_str = redirect_std_start()
        print('blablabla')
        string = redirect_std_finish(old_stdout, summary_str)
        print('captured output: {}'.format(string))
    :return:
    """
    old_stdout = sys.stdout
    sys.stdout = summary_str = io.StringIO()
    return old_stdout, summary_str


def redirect_std_finish(old_stdout, summary_str) -> str:
    """ redirect all prints back to std out and return a string of what was captured"""
    sys.stdout = old_stdout
    return summary_str.getvalue()


def get_line_number(depth: int = 1) -> str:
    ret_val = ''
    try:
        scope_1_back = inspect.stack()[depth]  # stack()[0] is this function
        ret_val = '{}'.format(scope_1_back.lineno)
    except IndexError:
        pass
    return ret_val


def get_function_name(depth: int = 1) -> str:
    ret_val = ''
    try:
        scope_1_back = inspect.stack()[depth]  # stack()[0] is this function
        ret_val = '{}'.format(scope_1_back.function)
    except IndexError:
        pass
    return ret_val


def get_file_name(depth: int = 1) -> str:
    ret_val = ''
    try:
        scope_1_back = inspect.stack()[depth]  # stack()[0] is this function
        ret_val = '{}'.format(scope_1_back.filename)
    except IndexError:
        pass
    return ret_val


def get_function_name_and_line(depth: int = 1) -> str:
    # +1 because of this function
    ret_val = '{} line {}'.format(get_function_name(depth + 1), get_line_number(depth + 1))
    return ret_val


def add_color(string: str, color: str = 'Red') -> str:
    """
    :param string:
    :param color: from color map
    # todo add option for combination (like bold, underlined ...)
    # todo change to lower case
    # todo color numbers maybe wrong
    e.g.
        my_str = 'hello colorful world!'
        print(my_str)
        print(add_color(my_str, color='Red'))
        print(add_color(my_str, color='Blue'))
        print(add_color(my_str, color='Bold'))
    to see all colors:
        for k, v in CONST_COLOR_MAP.items():
            print('{}{}{}'.format(v, k, CONST_COLOR_MAP['ResetAll']))
    """

    if color in CONST_COLOR_MAP:
        # concat (color, string, reset tag)
        string = '{}{}{}'.format(CONST_COLOR_MAP[color], string, CONST_COLOR_MAP['ResetAll'])
    return string


def init_logger(logger_path: str = None):
    """
    example:
        init_logger('./log.txt')
        log_print('line 1')
        flush_logger()
        log_print('line 2')
        log_print('line 3')
        close_logger()
    """
    global logger
    logger = open(file=logger_path, mode='w', encoding='utf-8') if logger_path is not None else None
    print(type(logger))
    return logger


def flush_logger() -> None:
    """ good for loops - writes every iteration if used """
    global logger
    if logger is not None:
        logger.flush()
    return


def log_print(string: str) -> None:
    global logger
    print(string)
    if logger is not None:
        logger.write('{}\n'.format(string))
    return


def log_print_dict(my_dict) -> None:
    for k, v in my_dict.items():
        log_print('\t{}: {}'.format(k, v))
    return


def close_logger() -> None:
    global logger
    if logger is not None:
        logger.close()
    return


def create_dir_if_not_exists(data_root: str, ack: bool = True, tabs: int = 1):
    if os.path.exists(data_root):
        if ack:
            print('{}{} exists'.format(tabs * '\t', data_root))
    else:
        os.mkdir(data_root)
        if ack:
            print('{}{} created'.format(tabs * '\t', data_root))
    return


def sleep(seconds: int):
    time.sleep(seconds)
    return


def reverse_tuple_or_list(orig: [tuple, list]) -> [tuple, list]:
    """
    :param orig: list or tuple
    :return: dst: reversed list or tuple
    e.g.
    my_tuple = (0, 0, 255)
    print(my_tuple)
    print(reverse_tuple_or_list(my_tuple))
    my_list = [0, 0, 255]
    print(my_list)
    print(reverse_tuple_or_list(my_list))
    """
    dst = orig[::-1]
    return dst


def get_time_stamp(format_s: str) -> str:
    """
    :param format_s:
    examples:
    "%Y_%m_%d_%H_%M_%S_%f" >>> 2020_07_19_13_36_24_597247
    "%Y_%m_%d" >>> 2021_04_07
    :return:
    """
    date_time_obj = datetime.datetime.now()
    timestamp_str = date_time_obj.strftime(format_s)
    return timestamp_str


def main():
    print(get_time_stamp("%Y_%m_%d_%H_%M_%S_%f"))
    print(get_time_stamp("%Y_%m_%d"))
    return


if __name__ == '__main__':
    main_wrapper(
        main_function=main,
        cuda_off=True,
        torch_v=True,
        tf_v=False,
        cv2_v=True,
        with_profiler=False
    )
