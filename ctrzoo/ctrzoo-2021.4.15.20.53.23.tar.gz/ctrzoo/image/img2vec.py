#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MICTRZOO.
# @File         : image2vector
# @Time         : 2021/3/26 4:52 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  :
"""
1. 先做push封面图
2. 然后做流内封面图

"""

from meutils.pipe import *
from meutils.date_utils import date_difference
from meutils.aizoo import tf_io
from meutils.aizoo.image import img2vec

model = img2vec.Img2vec()


def url2vec(url):
    if url.startswith('http'):
        try:
            vec = model.encoder(url)[0].tolist() | xjoin
            return vec
        except Exception as e:
            logger.error(e)
            return '0' * 512 | xjoin
    else:
        return '0' * 512 | xjoin


if __name__ == '__main__':
    class Img2vec(Main):

        @args
        def main(self, **kwargs):
            date = kwargs.get('date', date_difference('%Y%m%d', days=1))
            input = kwargs.get(
                'input',
                '/user/h_data_platform/platform/feeds/biz/biz=push_click_item_dw',
            )
            output = kwargs.get(
                'output',
                '/user/h_data_platform/platform/feeds/biz/biz=push_click_item_imgvec_dw',
            )

            df = tf_io.read_hdfs(
                input,
                reader=lambda p: pd.read_csv(p, '\t', names=["itemid", "image_url"], usecols=(0, 2)),
            )

            df1 = df[df['image_url'].isnull()]
            logger.debug(f"### 无图片数量级：{df1.shape}")

            df2 = df[~df['image_url'].isnull()].assign(vector=lambda df: df['image_url'].apply(url2vec))

            df = pd.concat([df2, df1], ignore_index=True)
            tf_io.to_hdfs(df, f'{output}/df.tsv')


    Img2vec.cli()
