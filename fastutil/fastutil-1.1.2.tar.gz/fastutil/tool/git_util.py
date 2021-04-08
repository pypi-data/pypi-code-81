import datetime as dt
import subprocess

import loguru


def commit():
    status, res = subprocess.getstatusoutput('git commit -m "auto"')
    if status == 0 and 'file changed' in res:
        return True
    return False


def is_git_commit():
    status, res = subprocess.getstatusoutput('git status')
    if status == 0 and 'nothing to commit' in res:
        return True
    return False


def get_git_tag():
    status, res = subprocess.getstatusoutput('git rev-parse HEAD')
    if status != 0:
        loguru.logger.warning('git status return:{},msg:{}'.format(status, res))
        return -1
    if 'Not a git repository' in res:
        loguru.logger.warning('git status return:{},msg:{}'.format(status, res))
        return -1
    return res


def get_ver_id(raise_exception=True):
    """
    获取git版本号
    :param raise_exception: git不存在或者git未提交是否抛出异常
    :return:
    """
    if not is_git_commit():
        if raise_exception:
            raise Exception('git is not commit')
        else:
            return None
    tag_res = get_git_tag()
    if tag_res == -1:
        if raise_exception:
            raise Exception('ver id is None')
        else:
            return None
    return tag_res[:8]


def get_date_ver_id(raise_exception=True):
    """
    获取日期+git版本号
    :param raise_exception: git不存在或者git未提交是否抛出异常
    :return:
    """
    git_tag = get_ver_id(raise_exception)
    if git_tag is None:
        return None
    now_date = dt.datetime.now().strftime('%Y%m%d_%H%M%S')
    _date_ver_id = now_date + '_' + git_tag
    return _date_ver_id


def ver_id():
    print(get_ver_id())


def date_ver_id():
    print(get_date_ver_id())
