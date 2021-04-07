import time
import logging
import os
import numpy as np
import pandas as pd
import random
import glob
from functools import wraps
from multiprocessing import cpu_count
from pathos.multiprocessing import ProcessingPool as Pool


class RunningTimeDecorator:
    """실행 시간 표시 데코레이터
    """

    def __init__(self, logger=None, show_section: bool = True, show_pid: bool = True):
        """init

        Args:
            logger ([type], optional): 사용할 logger. Defaults to None.
            show_section (bool, optional): 해당 함수의 실행 시작과 끝을 표시할 것인지. Defaults to True.
            show_pid (bool, optional): 해당 함수가 실행되는 process ID를 표시할 것인지. Defaults to True.
        """

        self.__param = logger
        self.__show_section = show_section
        self.__show_pid = show_pid

    def __call__(self, func):
        """call

        Args:
            func ([type]): 실행 시간을 표시할 함수
        """

        def printLog(str_arg: str):
            """로그 출력
            logger가 존재하면 logger에 str_arg 출력
            존재하지 않으면 print로 str_arg 출력

            Args:
                str_arg (str): 출력할 문자열
            """

            if isinstance(self.__param, logging.Logger):
                logger = logging.getLogger(self.__param.name)
                logger.info(str_arg)
            else:
                print(str_arg)

        @wraps(func)
        def decorator(*args, **kwargs):
            """decorator

            Returns:
                [type]: 실행시간을 표시할 함수의 리턴 값
            """

            str_current_pid = ""

            if self.__show_section:
                if self.__show_pid:
                    str_current_pid = "(PID:" + str(os.getpid()) + ")"
                str_start = "{0}{1} Started.".format(func.__name__, str_current_pid)
                printLog(str_start)

            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()

            if self.__show_section:
                if self.__show_pid:
                    str_current_pid = "(PID:" + str(os.getpid()) + ")"
                str_finish = "{0}{1} Finished.".format(func.__name__, str_current_pid)
                printLog(str_finish)
            str_log = "{0}{1} Elapsed Time : {2:.2f} seconds".format(
                func.__name__, str_current_pid, end_time - start_time
            )
            printLog(str_log)
            return result

        return decorator


def get_last_path(dir: str, type: str = "dir", by: str = "name"):
    """디렉토리 내림차순 정렬로 가장 마지막 디렉토리 경로 리턴

    Args:
        dir (str): 검색할 디렉토리 경로
        type (str): 검색할 유형 설정
            "dir": 디렉토리
            "file": 파일
            "all": 디렉토리 + 파일
            "확장자": 해당 확장자를 가진 파일
        by (str, optional): Defaults to "name".
            "name": 이름
            "mtime": 수정 시간
            "ctime": 생성 시간
            "atime": 액세스 시간

    Returns:
        str: 마지막 경로
    """

    if type == "dir":
        dir_list = list(filter(os.path.isdir, glob.glob(dir + "/*")))
    elif type == "file":
        dir_list = list(filter(os.path.isfile, glob.glob(dir + "/*")))
    elif type == "all":
        dir_list = glob.glob(dir + "/*")
    else:
        dir_list = glob.glob(dir + "/*" + type)

    last_path = ""

    if len(dir_list) > 0:
        if by == "mtime":
            sort_by = os.path.getmtime
        elif by == "ctime":
            sort_by = os.path.getctime
        elif by == "atime":
            sort_by = os.path.getatime
        elif by == "name":
            return max(dir_list)

        last_path = max(dir_list, key=sort_by)
    return last_path


def parallelize_dataframe(func, df: pd.DataFrame):
    """데이터프레임을 분할해서 cpu 병렬처리
    multi process

    Args:
        func ([type]): cpu 병렬처리에 사용할 함수
        df (pd.DataFrame): 분할할 데이터프레임

    Returns:
        pd.DataFrame: cpu 병렬처리된 데이터프레임
    """

    num_cores = cpu_count() - 1
    pool = Pool(num_cores)

    df_split = np.array_split(df, num_cores)

    len_df = len(df_split)
    if len_df < num_cores:
        num_cores = len_df

    df = pd.concat(pool.map(func, df_split))

    pool.close()
    pool.join()
    pool.clear()
    return df


def parallelize_dataframe_with_args(func, df: pd.DataFrame, *args):
    """데이터프레임을 분할해서 cpu 병렬처리(func에 인자값이 필요한 경우)
    multi process

    Args:
        func ([type]): cpu 병렬처리에 사용할 함수
        df (pd.DataFrame): 분할할 데이터프레임
        args: func에 들어갈 인자값

    Returns:
        pd.DataFrame: cpu 병렬처리된 데이터프레임
    """

    num_cores = cpu_count() - 1
    pool = Pool(num_cores)

    df_split = np.array_split(df, num_cores)

    len_df = len(df_split)
    if len_df < num_cores:
        num_cores = len_df

    list_tuple_args = []
    list_args = list(args)

    for item in df_split:
        each_list = [item]
        each_list.append(list_args)
        list_tuple_args.append(tuple(each_list))
    df = pd.concat(pool.map(lambda x: func(*x), list_tuple_args))
    pool.close()
    pool.join()
    pool.clear()
    return df


def string_to_boolean(arg_str: str):
    """str을 boolean으로 변환
        문자열이 "true", "1", "yes" 이면 True,
        문자열이 "false", "0", "no" 이면 False,
        그 외엔 np.NaN 리턴

    Args:
        arg_str (str): 변환할 문자열

    Returns:
        bool or np.NaN: 변환된 값
    """

    list_true = ["true", "1", "yes"]
    list_false = ["false", "0", "no"]

    if arg_str.lower() in list_true:
        return True
    if arg_str.lower() in list_false:
        return False
    return np.NaN


def set_random_seed(seed: int = 47):
    """랜덤 시드 초기화

    Args:
        seed (int, optional): 랜덤 시드 초기화 값. Defaults to 47.
    """

    np.random.seed(seed)
    random.seed(seed)
    # tf.set_random_seed(seed)
    # tf.random.set_seed(seed)


def list_chunk(lst: list, n_item: int):
    """리스트를 주어진 개수의 item 단위로 분할

    Args:
        lst (list): 분할할 리스트
        n_item (int): 분할할 각각의 item개수

    Returns:
        list: 분할된 리스트
    """
    return [lst[i : i + n_item] for i in range(0, len(lst), n_item)]


def unnesting(df: pd.DataFrame, explode_columns: list):
    """멀티컬럼 explode

    Args:
        df (pd.DataFrame): explode할 데이터프레임
        explode_columns (list): explode할 컬럼

    Returns:
        pd.DataFrame: explode된 데이터프레임
    """

    list_columns = df.columns
    idx = df.index.repeat(df[explode_columns[0]].str.len())
    df1 = pd.concat([pd.DataFrame({x: np.concatenate(df[x].values)}) for x in explode_columns], axis=1)
    df1.index = idx
    result = df1.join(df.drop(explode_columns, 1), how="left").reset_index(drop=True)
    result = result[list_columns]
    return result
