#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MICTRZOO.
# @File         : check_hdfs
# @Time         : 2021/4/8 12:49 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  :
from meutils.pipe import *
from meutils.aizoo import tf_io
from meutils.decorators.feishu import *

if __name__ == '__main__':
    class CheckHdfs(Main):

        @feishu_hook('个性化垂类包', hook_url=get_zk_config('/mipush/bot')['垂类'])
        @args
        def main(self, **kwargs):
            path = kwargs.get('path', None)
            if tf_io.check_path(path):
                return '个性化垂类包已准备好，可进行下发'


    CheckHdfs.cli()
