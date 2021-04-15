#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MICTRZOO.
# @File         : check_zk
# @Time         : 2021/4/8 1:39 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.zk_utils import *
from meutils.decorators.feishu import *

if __name__ == '__main__':
    class CheckZK(Main):

        @feishu_hook('个性化垂类包', hook_url=get_zk_config('/mipush/bot')['垂类'])
        @args
        def main(self):
            zk_watcher('/mipush/ann_profile')

            old = ZKConfig.info
            while 1:
                time.sleep(60)
                if old != ZKConfig.info:  # 当值改变了就终止监控
                    return '正在准备个性化垂类包'


    CheckZK.cli()
