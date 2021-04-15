#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : o2o_bert_vector
# @Time         : 2020/11/11 1:19 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :


from meutils.pipe import *
from meutils.aizoo import tf_io
from meutils.date_utils import date_difference
from meutils.log_utils import logger4feishu

from ctrzoo.utils import send_device
from ctrzoo.simbert.title2vec import texts2vecs

send_device(__file__)


class Task(BaseConfig):
    biz = ''
    start_date = date_difference('%Y%m%d', days=1)  # 开始时间
    days = 1

    input: str
    reader = "lambda p: pd.read_csv(p, '\t')"
    file_format = 'tsv'  # 'tsv', 'parquet'

    output: str
    output_dim = 198
    num_partition = 1


class Tasks(BaseConfig):
    tasks: List[Task]



for task in tqdm(Tasks.parse_zk("/mipush/common_cfg/simbert_transform").tasks):

    biz = f"{task.biz}向量化"
    logger4feishu(biz, '')

    for i in range(task.days):
        date = date_difference('%Y%m%d', start_date=task.start_date, days=i)
        reader = eval(task.reader)

        output_vecname = 'VECTOR'

        files = tf_io.cp(task.input.format(date=date), './data')
        df = pd.concat(map(reader, files)).reset_index(drop=True)

        logger4feishu(biz, f'{date} 数据量: {len(df)}, 预计耗时: {len(df) / 20000} m')

        df['vector'] = texts2vecs(df['title'].astype(str)).tolist()
        df['vector'] = df['vector'].map(lambda x: ' '.join(map(str, x)))
        df.to_csv(output_vecname)

        tf_io.cp(output_vecname, task.input.format(date=date))
        magic_cmd('rm output_vecname')
