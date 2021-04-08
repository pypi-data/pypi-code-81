"""
任务计划工具
"""
import argparse
import datetime as dt
import time

import psutil
from loguru import logger
from fastutil.tool import gpu_util

parser = argparse.ArgumentParser(description='定时任务，使用示例：taskplan --pid 154 --gpu_num 2 && command')
parser.add_argument('--pids', type=int, nargs='*', help='等待结束的进程，支持多个')
parser.add_argument('--wait_min', type=int, help='等待的时长（分钟）')
parser.add_argument('--date', nargs=2, help='指定日期启动')
parser.add_argument('--cpu_rate', type=float, help='cpu使用率低于的阈值')
parser.add_argument('--cpu_memory', type=int, help='cpu内存要求（M）')
parser.add_argument('--gpu_num', type=int, help='gpu空闲数量')
parser.add_argument('--gpu_memory', type=int, default=None, help='显存要求（M）,指定gpu_memory,默认gpu_num=1')
args = parser.parse_args()


def is_pid_ok(pids):
    if pids is None:
        return True
    running_pids = [pid for pid in pids if pid in psutil.pids()]
    if len(running_pids) == 0:
        return True
    logger.info('running pids:{}'.format(pids))
    return False


def is_wait_ok(start_time, wait_duration):
    if wait_duration is None:
        return True
    wait_seconds = (dt.datetime.now() - start_time).total_seconds()
    if wait_seconds / 60 >= wait_duration:
        return True
    logger.info('current wait minute:{}'.format(wait_seconds / 60))
    return False


def is_date_ok(wait_date):
    if wait_date is None:
        return True
    if dt.datetime.now() > wait_date:
        return True
    logger.info('current date:{}'.format(dt.datetime.now()))
    return False


def is_cpu_rate_ok(cpu_rate):
    if cpu_rate is None:
        return True
    cur_cpu_rate = psutil.cpu_percent(interval=0.2)
    if cur_cpu_rate <= cpu_rate:
        return True
    logger.info('current cpu rate:{}'.format(cur_cpu_rate))
    return False


def is_cpu_memory_ok(cpu_memory):
    if cpu_memory is None:
        return True
    mem_stats = psutil.virtual_memory()
    cur_cpu_memory = mem_stats.available / 1024 / 1024
    if cur_cpu_memory >= cpu_memory:
        return True
    logger.info('current cpu memory:{}'.format(cur_cpu_memory))
    return False


def is_gpu_ok(gpu_num, gpu_memory):
    if gpu_num is None and gpu_memory is None:
        return True
    if gpu_num is None and gpu_memory > 0:
        gpu_num = 1
    if gpu_num is not None and gpu_memory is None:
        gpu_memory = 0
    gpu_list = gpu_util.check_gpu(gpu_memory)
    if len(gpu_list) >= gpu_num:
        return True
    logger.info('available gpus:{}'.format(gpu_list))
    return False


def start_plan():
    logger.info('plan start')
    params = {}
    for k, v in vars(args).items():
        if v is not None:
            params[k] = v
    logger.info('input params:{}'.format(params))

    # 循环判断状态
    start_time = dt.datetime.now()
    wait_date = None
    if args.date:
        wait_date = dt.datetime.strptime(' '.join(args.date), '%Y-%m-%d %H:%M:%S')
    while True:
        if is_pid_ok(args.pids) and is_wait_ok(start_time, args.wait_min) and is_date_ok(wait_date) \
                and is_cpu_rate_ok(args.cpu_rate) and is_cpu_memory_ok(args.cpu_memory) \
                and is_gpu_ok(args.gpu_num, args.gpu_memory):
            break
        time.sleep(60)

    logger.info('plan finish')
    time.sleep(1)
