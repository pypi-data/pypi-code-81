#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : notice
# @Time         : 2021/4/2 3:46 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import *
from meutils.zk_utils import get_zk_config


def feishu_hook(title='Task Done', text=None, hook_url=get_zk_config('/mipush/bot')['logger']):
    """装饰器里不可变参数

    :param title:
    :param text: 如果为空，用函数返回值填充
    :param hook_url:
    :return:
    """

    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        s = time.time()
        r = wrapped(*args, **kwargs)
        e = time.time()

        mins = (e - s) // 60

        logger.info(f"{title} done in {mins} m")

        if text is None:  # text没法直接赋值
            body = {"title": title, "text": str(r) + f"\n耗时 {mins} m"}
        else:
            body = {"title": title, "text": text + f"\n耗时 {mins} m"}

        requests.post(hook_url, json=body).json()

        return r

    return wrapper


def feishu_catch(more_info=True, hook_url=get_zk_config('/mipush/bot')['logger']):
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        try:
            wrapped(*args, **kwargs)
        except Exception as e:
            text = traceback.format_exc() if more_info else e

            body = {"title": f"Exception: {wrapped.__name__}", "text": text}
            requests.post(hook_url, json=body).json()

        return wrapped(*args, **kwargs)

    return wrapper


if __name__ == '__main__':
    @feishu_hook('catch hook')
    # @feishu_catch()
    def f():
        1 / 0.1
        # return 'RES'


    f()
    # ff()
