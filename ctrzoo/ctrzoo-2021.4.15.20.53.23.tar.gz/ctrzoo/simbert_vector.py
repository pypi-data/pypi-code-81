#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : o2o_bert_vector
# @Time         : 2020/11/11 1:19 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : todo 所有的向量转化任务放一起
"""
转换速度 2w/m

这个作业即将废弃@张玮
"""

from meutils.pipe import *
from meutils.aizoo import tf_io
from meutils.np_utils import normalize
from meutils.date_utils import date_difference
from meutils.log_utils import logger4feishu

from bertzoo.SimBert import SimBert
from bertzoo.utils.bert4keras_utils import texts2seq

from ctrzoo.utils.io import tf_copy
from ctrzoo.utils import send_device

send_device(__file__)


class Config(BaseConfig):
    date = date_difference('%Y%m%d', days=1)  # 开始时间
    days = 1
    input = ''
    output = ''
    reader = ''
    writer = ''


cfg = Config.parse_zk("/mipush/common_cfg/simbert_vector")
input = cfg.input
output = cfg.output

# BERT
tf_copy(
    f'hdfs://zjyprc-hadoop/user/h_browser/algo/yuanjie/data/chinese_simbert_L-12_H-768_A-12/*',
    './data/chinese_simbert_L-12_H-768_A-12'
)
sb = SimBert('./data/chinese_simbert_L-12_H-768_A-12/vocab.txt')
sb.build_model()

tokenizer = sb.tokenizer
encoder = sb.encoder


def texts2vecs(texts=None):
    data = texts2seq(texts=texts, tokenizer=tokenizer)
    vecs = encoder.predict(data, batch_size=1000)
    return normalize(vecs[:, range(0, 768, 3)])  # 256维
    # return normalize(vecs[:, range(0, 768, 4)])  # 198维


# RUN
for i in range(cfg.days):
    date = date_difference('%Y%m%d', start_date=cfg.date, days=i)
    output_vecname = f'VECTOR_{time.time()}'

    __file__ = f"BERT向量化: {Path(input).name}/date={date}"

    # 下载数据
    logger4feishu(__file__, '下载数据')

    files = tf_copy(f'hdfs://zjyprc-hadoop{input}/date={date}/*.parquet', './data')

    df = pd.concat(map(pd.read_parquet, files)).reset_index(drop=True)

    logger4feishu(__file__, f'数据量: {df.shape}')
    logger4feishu('ls ./data', magic_cmd('ls ./data')[-1])

    # 转换向量
    logger4feishu(__file__, '转换向量')

    df['vector'] = texts2vecs(df['title'].astype(str)).tolist()

    df.to_parquet(output_vecname)
    # eval(cfg.writer)(df)

    # 上传数据
    logger4feishu(__file__, '上传数据')

    tf_io.cp(output_vecname, f'{output}/date={date}')

    logger4feishu(__file__, f'耗时: {(time.time() - START_TIME) // 60} m')
