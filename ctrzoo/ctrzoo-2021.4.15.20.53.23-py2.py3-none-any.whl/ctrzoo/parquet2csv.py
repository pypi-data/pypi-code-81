#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MICTRZOO.
# @File         : parquet2csv
# @Time         : 2021/3/5 5:59 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from ctrzoo.utils.io import ZJY, DATA, tf_copy

files = tf_copy(
    "/user/h_data_platform/platform/browser/push_data/data/br/feed_item_with_bert_embedding_di/date=20210304/VECTOR*"
)

df = pd.read_parquet(files[0])

df['vector'] = df['vector'].map(lambda x: ' '.join(map(str, x)))

output = f"{DATA}/vec.tsv"

print(output)

df.to_csv(output, index=False, sep="\t")
tf_copy(
    output,
    "/user/h_data_platform/platform/browser/push_data/data/br/feed_item_with_bert_embedding_di/TEST"
)


