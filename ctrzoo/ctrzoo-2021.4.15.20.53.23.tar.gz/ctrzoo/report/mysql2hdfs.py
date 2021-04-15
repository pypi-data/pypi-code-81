#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MICTRZOO.
# @File         : mysql2hdfs
# @Time         : 2021/3/25 4:48 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  :

from ctrzoo.utils import *
from ctrzoo.simbert.profile2vec import *

from meutils.pipe import *
from meutils.aizoo import tf_io
from meutils.date_utils import date_difference

if __name__ == '__main__':
    class Mysql2Hdfs(Main):
        send_device(__file__)

        @args
        def main(self, **kwargs):
            days = kwargs.get('days', 1)
            date = date_difference('%Y%m%d', days=days)

            output = kwargs.get(
                'output',
                f'/user/h_data_platform/platform/feeds/biz_date/biz=mivideo_push_history/date={date}',
            )

            df = profile_push_his(days).assign(date=date)

            df.to_csv('DATA', '\t', index=False, header=False)

            tf_io.cp('DATA', output)


    Mysql2Hdfs().cli()
