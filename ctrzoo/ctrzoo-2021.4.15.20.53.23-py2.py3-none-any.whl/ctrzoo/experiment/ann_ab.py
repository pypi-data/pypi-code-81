#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MICTRZOO.
# @File         : ann_ab
# @Time         : 2021/4/15 2:14 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  :
from meutils.pipe import *
from meutils.decorators.feishu import feishu_hook, feishu_catch
from meutils.aizoo import tf_io
from meutils.date_utils import date_difference
from meutils.hash_utils import murmurhash

if __name__ == '__main__':
    class AB(Main):
        @feishu_hook('ANN: AB-A包已生成', hook_url='垂类')
        @args
        def main(self, **kwargs):
            date = kwargs.get('date', date_difference('%Y%m%d', days=1))
            ann_path = kwargs.get(
                'out_path',
                f'/user/h_data_platform/platform/feeds/biz/biz=ann_profile/date={date}'  # todo: 垂类目录
            )
            zixun = kwargs.get(
                'args',
                f'/user/h_data_platform/platform/feeds/mitv_profile_push/date={date}/资讯'
            )

            df = (
                tf_io.read_hdfs(zixun, reader=lambda p: pd.read_csv(p, names=['userid']))
                [lambda df: df['userid'].map(lambda x: murmurhash(x, bins=2) == 0)]
            )

            tf_io.cp(zixun, f"{zixun}.bak")  # 复制历史垂类包备份.bak
            tf_io.rm(zixun)  # 删除旧包

            tf_io.to_hdfs(df.assign(itemid='raw'), f"{ann_path}/part-raw")
            tf_io.to_hdfs(df, zixun, batch_size=100000, file_start_index=100)


    AB().cli()
