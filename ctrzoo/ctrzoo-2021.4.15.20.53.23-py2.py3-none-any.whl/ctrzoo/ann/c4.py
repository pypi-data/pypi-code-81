#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MICTRZOO.
# @File         : c4
# @Time         : 2021/4/7 4:40 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  :

import gensim
import tensorflow as tf
from meutils.pipe import *
from meutils.aizoo import tf_io
from meutils.pd_utils import df_split
from meutils.date_utils import date_difference
from meutils.log_utils import logger4feishu
from meutils.http_utils import results
from meutils.zk_utils import get_zk_config
from meutils.decorators import hdfs_flag
from meutils.decorators.feishu import feishu_catch

# magic_cmd("kinit -k -t ./data/s_feeds.keytab s_feeds@XIAOMI.HADOOP")

r = get_zk_config(
    '/data/services/recommend/engine/mitvpushmaster/conf/files/mitv_profile.conf',
    'tjwqstaging.zk.hadoop.srv:2181',
    mode=''
)

profile2path = {
    x[0]: x[2].replace('"', '') for x in (r.strip().split()[6:-2] | xgroup)
    if x[0] == 'docid'
}


@feishu_catch()
def get_vec(docid):
    title = results.get_ac(docid)['title']
    vec = results.get_simbert_vectors(title)
    return vec[0]


@feishu_catch()
def recall_topk(vec, df, topK=10000):
    # df = pd.read_parquet(path)[['userId', 'vector']]

    ann = gensim.models.KeyedVectors(768)
    ann.add(df['userId'], np.row_stack(df['vector']), True)
    ann.init_sims(replace=True)
    r = ann.wv.similar_by_vector(vec, topK)
    return pd.DataFrame(r)  # id, score


vec = get_vec(profile2path['docid'])

for i, file in tqdm(enumerate(Path('/home/work/yuanjie/ann/user_vec').glob('part-*'))):
    df = recall_topk(vec, pd.read_parquet(file))

    df[0].to_csv(f'/home/work/yuanjie/ann/result/part-{i}.tsv', index=False, header=False)
