#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MICTRZOO.
# @File         : push_click_item
# @Time         : 2021/3/15 3:57 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : HISTORY
from ctrzoo.simbert.title2vec import *

if __name__ == '__main__':
    class MitvPushClickItem2Vector(Main):
        send_device(__file__)

        @args
        def main(self, **kwargs):
            date = kwargs.get('date', date_difference('%Y%m%d', days=1))
            input = kwargs.get(
                'input',
                f'/user/h_data_platform/platform/feeds/biz_date/biz=push_click_item_dw/date={date}',
            )
            output = kwargs.get(
                'output',
                '/user/h_data_platform/platform/feeds/biz/biz=push_click_item_vec_dw',
            )

            df = tf_io.read_hdfs(
                input,
                reader=lambda p: pd.read_csv(p, '\t', names=["itemid", "title"], usecols=range(2)),
                max_workers=1
            )

            logger4feishu(self.__class__.__name__, f'{date} 数据量: {len(df) // 10000} w, 预计耗时: {len(df) // 20000} m')

            dfs = df_split(df, batch_size=100000)
            for i, df in tqdm(enumerate(dfs)):
                df['vector'] = texts2vecs(df['title'].astype(str)).tolist()
                df['vector'] = df['vector'].map(lambda x: ' '.join(map(str, x)))

                tf_io.to_hdfs(df, f'{output}/df{i}.tsv')

                # OOM
                del df
                gc.collect()


    MitvPushClickItem2Vector.cli()
