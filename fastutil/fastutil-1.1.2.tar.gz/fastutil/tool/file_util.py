import argparse
import os
import threading
import re

import psutil
from fastutil.tool import message_util
import time
from loguru import logger
import math


def search_file_pid(file_path):
    """
    找出和文件关联的进程
    """
    rel_pids = []

    cur_pid = psutil.Process()
    cur_username = cur_pid.username()
    pid_list = psutil.pids()
    for pid in pid_list:
        try:
            p = psutil.Process(pid)
            if p.pid == cur_pid.pid:
                continue
            # 如果不是root，而且当前进程的用户不是当前用户，跳过
            if cur_username != "root" and p.username() != cur_username:
                continue
            file_list = p.open_files()
            for file in file_list:
                if os.path.samefile(file.path, file_path):
                    rel_pids.append(pid)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return list(set(rel_pids))


def get_log_file(pid, filter_name):
    p = psutil.Process(pid)
    file_list = p.open_files()
    log_path_list = []
    for f in file_list:
        file_name = os.path.basename(f.path)
        if file_name.startswith(filter_name):
            if file_name.endswith('.log') or file_name.endswith('.out'):
                log_path_list.append(f.path)
    return log_path_list


def get_last_line(filename, read_last_num):
    """
    获取末尾指定行数
    """
    file_size = os.path.getsize(filename)
    if file_size == 0:
        return []
    with open(filename, 'rb') as f:
        offset = -read_last_num * 50
        while -offset < file_size:
            f.seek(offset, 2)
            lines = f.readlines()
            if len(lines) >= read_last_num + 1:
                lines = lines[-read_last_num:]
                break
            offset *= 2
        if -offset > file_size:
            f.seek(0)
            lines = f.readlines()
    lines = [line.decode() for line in lines]
    return ''.join(lines)


eta_re = re.compile(r'(\d+/\d+.+?)')
eta_num_re = re.compile(r'(\d+)/\d+.+?')


def get_eta_groups(lines):
    lines = [line.decode() for line in lines]
    eta_list = eta_re.findall(''.join(lines))
    if not eta_list:
        return [], 0
    eta_num = eta_num_re.search(eta_list[0]).group(1)
    return eta_list, int(eta_num)


def get_eta_log(filename, read_last_num):
    """
    处理keras和tensorflow打印的eta日志
    """
    file_size = os.path.getsize(filename)
    if file_size == 0:
        return ''
    with open(filename, 'rb') as f:
        f.seek(-1000, 2)
        _, eta_num = get_eta_groups(f.readlines())
        if eta_num == 0:
            f.seek(0)
            lines = [line.decode() for line in f.readlines()]
            return ''.join(lines)
        eta_interval = math.ceil(eta_num / 1000)
        total_num = read_last_num * eta_interval
        offset = -total_num * 100
        while -offset < file_size:
            f.seek(offset, 2)
            eta_list, eta_num = get_eta_groups(f.readlines())
            if len(eta_list) >= total_num + 1:
                lines = eta_list[-total_num:]
                break
            offset *= 2
        if -offset > file_size:
            f.seek(0)
            lines, _ = get_eta_groups(f.readlines())
    lines = [line for idx, line in enumerate(lines) if (idx + 1) % eta_interval == 0]
    return '\n'.join(lines)


def _is_log_finish(log_path_list):
    pid_list = []
    for log_path in log_path_list:
        pid_list.extend(search_file_pid(log_path))
    if len(pid_list) == 0:
        return True
    return False


@logger.catch()
def send_log(log_path_list, send_num, send_title, send_to, interval_min, is_eta):
    while True:
        for log_path in log_path_list:
            if is_eta:
                msg = get_eta_log(log_path, send_num)
            else:
                msg = get_last_line(log_path, send_num)
            if send_title and send_to and msg:
                msg = 'log_path: {}\nmsg:\n{}'.format(log_path, msg)
                message_util.send_email(send_title, msg, send_to)
        if _is_log_finish(log_path_list):
            break
        for i in range(interval_min):
            time.sleep(60)
            if _is_log_finish(log_path_list):
                break


def start_trace_log(log_path_list, trace_num=10, send_title='日志监控', send_to='', interval_min=300):
    t = threading.Thread(target=send_log, args=(log_path_list, trace_num, send_title, send_to, interval_min, True))
    t.setDaemon(True)
    t.start()


def trace_log():
    parser = argparse.ArgumentParser(description='日志跟踪')
    parser.add_argument('--log_path', nargs='*', required=True, help='跟踪日志名称，可以多个')
    parser.add_argument('--trace_num', type=int, default=10, help='邮件发送内容行数')
    parser.add_argument('--is_eta', action='store_true', default=True, help='keras打印的eta日志')
    parser.add_argument('--send_title', default='日志监控', help='邮件标题')
    parser.add_argument('--send_to', required=True, help='邮件接收地址')
    parser.add_argument('--interval_min', type=int, required=True, help='发送间隔')
    args = parser.parse_args()
    send_log(args.log_path, args.trace_num, args.send_title, args.send_to, args.interval_min, args.is_eta)


def get_parent_dir(path, top_num=1):
    """
    获取父目录
    :param path: 当前文件路径，传入__file__
    :param top_num: 第几层父目录
    :return:
    """
    parent_path = os.path.abspath(path)
    for i in range(top_num):
        parent_path = os.path.dirname(parent_path)
    return parent_path
