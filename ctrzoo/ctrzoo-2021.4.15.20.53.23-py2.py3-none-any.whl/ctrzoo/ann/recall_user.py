#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MICTRZOO.
# @File         : recall_user
# @Time         : 2021/4/6 3:57 下午
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
from meutils.decorators.feishu import *

magic_cmd("kinit -k -t ./data/s_feeds.keytab s_feeds@XIAOMI.HADOOP")

# r = get_zk_config(
#     '/data/services/recommend/engine/mitvpushmaster/conf/files/mitv_profile.conf',
#     'tjwqstaging.zk.hadoop.srv:2181',
#     mode=''
# )
#
# profile2path = {
#     x[0]: x[2].replace('"', '') for x in (r.strip().split()[6:-2] | xgroup)
#     if x[0] == 'docid'
# }

docid = get_zk_config('/mipush/ann_profile')


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



if __name__ == '__main__':
    class RecallUser(Main):

        @feishu_hook('个性化垂类包', hook_url=get_zk_config('/mipush/bot')['垂类'])
        @feishu_catch()
        @args
        def main(self, **kwargs):
            date = kwargs.get('date', date_difference('%Y%m%d', days=1))
            part = kwargs.get('part', 0)

            user_vec_path = kwargs.get(
                'user_vec_path',
                f'/user/h_data_platform/platform/feeds/biz/biz=mitv_user_embedding/date={date}'
            )
            output = f"/user/h_data_platform/platform/feeds/mitv_profile_push/date={date}/ann"

            vec = get_vec(docid)
            for file in tf_io.cp(user_vec_path, filter_fn=lambda p: int(Path(p).name[5:10]) % 10 == part):
                df = recall_topk(vec, pd.read_parquet(file))
                tf_io.to_hdfs(df[0], f'{output}/part-{Path(file).name[:10]}', with_success=False)

            return self.__class__.__name__


    RecallUser.cli()
