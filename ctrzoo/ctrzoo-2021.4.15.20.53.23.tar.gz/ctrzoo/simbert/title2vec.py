#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MICTRZOO.
# @File         : title2vec
# @Time         : 2021/3/9 3:57 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.aizoo import tf_io
from meutils.np_utils import normalize
from meutils.pd_utils import df_split
from meutils.date_utils import date_difference
from meutils.log_utils import logger4feishu

from bertzoo.SimBert import SimBert
from bertzoo.utils.bert4keras_utils import texts2seq

from ctrzoo.utils import send_device


# 常量
OUTPUT = "OUTPUT"

# BERT
files = tf_io.cp(
    '/user/h_browser/algo/yuanjie/data/chinese_simbert_L-12_H-768_A-12'
)
vocab = [file for file in files if 'vocab.txt' in file][0]
sb = SimBert(vocab)
sb.build_model()

tokenizer = sb.tokenizer
encoder = sb.encoder
logger.debug("BERT加载成功")


def texts2vecs(texts=None, output_dim=768):
    data = texts2seq(texts=texts, tokenizer=tokenizer)
    vecs = encoder.predict(data, batch_size=1000)
    del data
    gc.collect()

    if output_dim == 198:
        return normalize(vecs[:, range(0, 768, 4)])
    elif output_dim == 256:
        return normalize(vecs[:, range(0, 768, 3)])
    else:
        return normalize(vecs)  # 768维


if __name__ == '__main__':

    class Title2Vec(Main):
        send_device(__file__)

        @args
        def main(self, **kwargs):
            date = kwargs.get('date', date_difference('%Y%m%d', days=1))
            input = kwargs.get(
                'input',
                f'/user/h_data_platform/platform/feeds/biz_date/biz=new_item_di/date={date}',
            )
            output = kwargs.get(
                'output',
                f'/user/h_data_platform/platform/feeds/biz_date/biz=new_item_vec_di/date={date}',
            )

            df = tf_io.read_hdfs(
                input,
                reader=lambda p: pd.read_csv(p, '\t', names=["itemid", "title"]),
                max_workers=1
            )

            logger4feishu(self.__class__.__name__, f'{date} 数据量: {len(df) // 1000} k, 预计耗时: {len(df) // 20000} m')

            dfs = df_split(df, batch_size=100000)
            for i, df in tqdm(enumerate(dfs)):
                df['vector'] = texts2vecs(df['title'].astype(str)).tolist()
                df['vector'] = df['vector'].map(lambda x: ' '.join(map(str, x)))

                tf_io.to_hdfs(df, f'{output}/df{i}.tsv', with_success=False)

                # OOM
                del df['vector']
                gc.collect()


            tf_io.process_success(output)


    Title2Vec.cli()
